#!/usr/bin/env python

from unicorn import *
from unicorn.arm_const import *


test_data = {"pin": None, "found": False, "flag": None}
ARM_CODE = b"\x37\x00\xa0\xe3\x03\x10\x42\xe0"

def read_string(uc, address):
    string = b""
    while True:
        char = uc.mem_read(address, 38)
        if char == b"\x00": #end of string

            break
        # print(char.decode("ascii", errors=""))
        string = char 
        address += 1
        # return str(string)
        # return string.decode("ascii", errors="ignore")
        # string += char #concatenates string; data in single byte
        try: 
        # print("string is:", string.decode("ascii", errors="ignore"))
            
            # print(string.decode())
            return str(string)
        
        except:
            return None



def hook_printf(uc, address,size,user_data):
    if uc.reg_read(UC_ARM_REG_PC) == 0x10000432:
        uc.reg_write(UC_ARM_REG_PC, (address+size)|1)
    # print(hex(uc.reg_read(UC_ARM_REG_PC)))



def hook_scanf(uc,address,size, user_data):
    if uc.reg_read(UC_ARM_REG_PC) == 0x1000043c:
        addr = uc.reg_read(UC_ARM_REG_R1)
        uc.mem_write(addr, user_data["pin"].to_bytes(2, "little"))
        uc.reg_write(UC_ARM_REG_R0, 1)
        uc.reg_write(UC_ARM_REG_PC, 0x1000045c  | 1)

        # print("scan pc :", hex(uc.reg_read(UC_ARM_REG_PC)))


def hook_sleep_ms(uc,address,size, user_data):
    if uc.reg_read(UC_ARM_REG_PC) == 0x10000442:
        uc.reg_write(UC_ARM_REG_PC, 0x10000456 | 1)



def hook_puts(uc,address,size, user_data):
    if uc.reg_read(UC_ARM_REG_PC) ==  0x10000492:

        string_ptr = uc.reg_read(UC_ARM_REG_R0)
        flag = read_string(uc, string_ptr)
        uc.reg_write(UC_ARM_REG_PC, 0x10000496 | 1) #puts
        if flag == None:
            
            print("{} : Invalid Flag".format(test_data["pin"]))
        else:
            print(f"Flag: {flag}")
            test_data["flag"] = flag
            if "sshs" in flag:
                test_data["flag"] = flag
                test_data["found"] = True





with open("fw.bin", "rb") as f:
    firmware_data = f.read()
with open("sram.bin", "rb") as f:
    sram_data = f.read()
with open("rom.bin", "rb") as f:
    srom_data = f.read()


def mapping(mu):
    
    mu.mem_map(0x10000000, 0x220000)
    mu.mem_map(0x20000000, 0x100000)
    mu.mem_map(0x0, len(srom_data))

    mu.mem_write(0x10000000, firmware_data)
    mu.mem_write(0x20000000, sram_data)
    mu.mem_write(0x0, srom_data)

    print("Firmware Mapped...")
    mu.reg_write(UC_ARM_REG_R0, 0x13 )
    mu.reg_write(UC_ARM_REG_R1, 0x0 )
    mu.reg_write(UC_ARM_REG_R2, 0x0 )
    mu.reg_write(UC_ARM_REG_R3, 0x3)
    mu.reg_write(UC_ARM_REG_R4, 0x20041DE8)
    mu.reg_write(UC_ARM_REG_R5, 0x1000D398)
    mu.reg_write(UC_ARM_REG_R6, 0x1000D394)
    mu.reg_write(UC_ARM_REG_SP, 0x20041de0)
    mu.reg_write(UC_ARM_REG_LR, 0x10000a83)
    mu.reg_write(UC_ARM_REG_PC, 0x1000042c)
    mu.reg_write(UC_ARM_REG_APSR, 0xFFFFFFFF | 1)
    print("Registers Mapped...")

def bruteforce_pin():
    mu = unicorn.Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    mapping(mu)
    

    try:
        for i in range(10000):
            pin= f'{i:04d}'
            test_data["pin"] = int(f'{i:04d}')
            

            # test_data["pin"] = i
            # pin=i
            # mu.hook_add(UC_HOOK_CODE, hook_all, test_data, begin=0x1000042c)
            mu.hook_add(UC_HOOK_CODE, hook_printf, test_data, begin=0x1000042e, end=0x1000043a)
            mu.hook_add(UC_HOOK_CODE, hook_scanf, test_data, begin=0x1000043c, end=0x10000440)
            mu.hook_add(UC_HOOK_CODE, hook_sleep_ms, test_data, begin=0x10000442, end=0x10000456)
            mu.hook_add(UC_HOOK_CODE, hook_puts, test_data, begin=0x10000492, end=0x10000498)
            # print("hooks addes")
            # print("PC at", hex(mu.reg_read(UC_ARM_REG_PC)))
            mu.emu_start(0x1000042c | 1, 0x10000498) #pop
            print("Testing Pin: {}".format(pin))
            if test_data["found"] == True:
                print("flag found = {}".format(test_data["flag"]))
                break
    except UcError as e:
        print("Unicorn Error:", e)
        print("Error code:", e.errno)



if __name__ == "__main__":
    bruteforce_pin()