# Firmware Security and Rehosting

## Overview
This repository documents a firmware security project focused on analysing, reverse engineering,
and rehosting a legacy hardware security token deployed on a Raspberry Pi Pico.

The work was carried out from the perspective of an external security consultant tasked with
recovering protected secrets from undocumented firmware. The project combines **hardware-level
protocol analysis** with **firmware rehosting and emulation**, demonstrating how security
mechanisms can be bypassed without access to source code or original documentation.

---

## Project Scope
The assignment consists of two tightly coupled components:

1. **Protocol Reverse Engineering on Physical Hardware**
2. **Firmware Rehosting and Emulation using Unicorn**

Both parts were required to recover the protected PIN and associated flags fully.

---

## Part 1: Hardware Protocol Reverse Engineering

### Hardware Setup
- Target device: **Raspberry Pi Pico**
- Interfaces analysed: **UART** and **SPI**
- Tools used:
  - Logic Analyzer (Saleae Logic)
  - Serial terminal (e.g., Tera Term/minicom)
  - Raspberry Pi Pico datasheet and pinout

The firmware provides a menu-driven interface over USB serial, allowing specific actions
to trigger communication over different hardware buses.

---

### UART Identification and Decoding
To identify the UART interface:

1. The firmware menu was used to trigger UART output repeatedly.
2. A logic analyzer was connected to candidate GPIO pins.
3. Digital signals were captured and inspected using Logic 2 software.
4. UART decoding parameters were adjusted iteratively until valid ASCII output was observed.

Through analysis of signal timing and framing, the correct UART parameters were identified:
- Baud rate: 9600
- Data bits: 8
- Parity: None
- Stop bits: 1
- Bit order: LSB first
- Polarity: Idle high

Once correctly configured, the decoded UART output revealed the first flag.

---

### SPI Identification and Decoding
For SPI analysis:

1. Firmware menu options were used to trigger SPI communication.
2. GPIO pins were probed to locate clock, data, and chip-select lines.
3. Four-wire SPI signalling was identified (SCK, MOSI, MISO, CS).
4. Logic analyzer captures were decoded using different SPI mode configurations.

By analysing clock polarity, phase, and data ordering, the correct SPI settings were determined:
- SPI mode: CPOL = 0, CPHA = 0
- Bit order: MSB first
- Data width: 8 bits
- Chip select: Active low

Adjustments to analyzer timing (holdoff and grouping) were required to reconstruct
full SPI transactions correctly. Successful decoding revealed the second flag.

---

## Part 2: Firmware Rehosting and Emulation

### Objective
The goal of the rehosting phase was to execute a firmware function
(`assignment_2B_rehost`) outside the original hardware environment in order to
recover the protected PIN and final flag.

---

### Rehosting Strategy
The firmware was rehosted using the **Unicorn CPU emulator**, following this approach:

1. **Memory Reconstruction**
   - Flash, ROM, and SRAM regions were mapped into the emulator
   - Memory contents were loaded from the provided binary dumps

2. **CPU State Initialisation**
   - Register state was restored from a snapshot taken at function entry
   - Execution was started in ARM Thumb mode at the correct address

3. **Hardware Abstraction via Hooks**
   - Hardware-dependent functions (e.g., delays, I/O) were intercepted
   - Non-essential functions were skipped to allow execution to continue
   - Output functions were hooked to capture program output

4. **Input Injection**
   - PIN values were written directly into the expected memory locations
   - This simulated user input without requiring physical peripherals

5. **Automated Brute-Force Execution**
   - The rehosted function was executed in a loop
   - PIN values in the range [0–9999] were tested
   - Successful validation resulted in the firmware revealing the final flag

---

## Results
By combining hardware protocol analysis and firmware rehosting:

- UART communication was successfully decoded, and the first flag was recovered
- SPI communication was successfully decode,d and the second flag was recovered
- The firmware was fully rehosted in an emulated environment
- The correct PIN was identified via automated execution
- The final protected flag was recovered without physical interaction

This demonstrates that firmware relying solely on hardware isolation can still be
analysed and bypassed through careful emulation and reverse engineering.

---

## Repository Contents
- `rehost.py` – Python-based Unicorn rehosting and automation script
- `regs.txt` – CPU register snapshot at function entry
- `fw.bin` – Firmware image from flash memory
- `rom.bin` – Raspberry Pi Pico ROM dump
- `sram.bin` – SRAM memory dump
- `sshs.elf` – ELF binary with symbols for static analysis
- `sshs.uf2` – Firmware image used on the physical device
- `Dockerfile` – Containerised environment for reproducible execution
- `run.sh` – Builds and runs the rehosting workflow automatically
- `rehost_report.pdf` – Detailed technical report with screenshots and explanations

---

## How to Run (Rehosting)

```bash
./run.sh
```
---

## Technologies Used
- ARM Cortex-M (Thumb mode)
- Unicorn Engine (CPU emulation)
- Python
- Ghidra (static analysis)
- Docker (reproducible execution)
- UART & SPI (hardware communication protocols)
- Logic Analyzer (hardware signal inspection)

