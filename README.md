# Firmware Rehosting

This is a part of firmware analysis done at the University of Birmingham using raspberry-pi 2040. The task was divided into three parts, look for README.md, where in each task it was required to find flags in a particular format. The idea behind this activity was to understand the concept of SPI, UART, and firmware rehosting.

## Summary of Assignment

After showing your skills in security via automation, fuzzing, and vulnerability reporting, EvilCorp has a new task for you: Help them to recover key information about their legacy hardware security token, hosted on the Raspberry Pi Pico!

Unfortunately, the engineer who originally created the token left the company and documentation is missing. You will need to probe the different communication interface and recover the Pin code to unlock the device.

For this assignment, you will receive hardware (1 set per group). Please make sure to return this after you finished the assignment.

## Assignment

You are in the role of an external cybersecurity consultant and your assignment is divided into two parts: protocol reverse engineering and rehosting.

Please refer to the assignment introduction slides or recording for additional information on the hardware.

For Part 2, you are also given a set of files to carry out your task: `assignment2.zip`.

---

# Part 1: Protocol Reverse Engineering

### Notes

Throughout this assignment, you are asked to retrieve different "flags". In this assignment, these are human-readable strings, following the format:

```text
sshs{$random_string}
```

Please include the retrieved flags in your submission.

### Goals

#### Preparation

- Obtain the set of hardware from the lecturers or TAs (1 set per group).
- Flash the target firmware on the device.
- Download the Saleae Logic 2 software for your operating system.
- Make sure you can communicate with your Raspberry Pi Pico via USB, using for instance:
  - Minicom on Mac/Linux
  - Putty on Windows

#### UART Identification

- Use the menu of the Pico firmware to send a message via UART.
- The message is sent once every time the menu entry is selected.
- Attach the logic analyzer to the right pins and capture the traffic using the Logic 2 software.
- Decode the UART message using the corresponding protocol decoder with the right parameters.

#### SPI Identification

- Use the menu of the Pico firmware to send a message via SPI.
- The message is sent once every time the menu entry is selected.
- Probe different pins with the logic analyzer to find the pins on which the message is transmitted.
- Decode the SPI message using the corresponding protocol decoder with the right parameters.

### Hints

- If you are stuck connecting to your Pico, a look at the Raspberry Pi Pico getting started guide may help.
- When connected to the Pico and not seeing any output, try typing a number and press Enter.
- The Logic 2 software has some nice features that can help you inspect signals and even decode them.
- If you observe framing errors, your UART decoder settings are not 100% correct. Try looking at the signal and the lecture slides and figure out why you encounter these errors.
- The SPI signal in this exercise uses 4 wires.
- If the Logic 2 tool reports that it cannot keep up with the selected sample rate, consider reducing the sample rate.
- Each pin has a limited set of functions it can be used for. Find the datasheet for the Raspberry Pi Pico and check the pinout carefully.

---

# Part 2: Rehosting

### Note

For this part of the assignment, you receive a dump from the Raspberry Pi Pico, at the entry point of the function `assignment_2B_rehost`.

This dump contains:

- `regs.txt`
- `fw.bin`
- `rom.bin`
- `sram.bin`

Additionally, you receive `sshs.elf`, a compiled version of the firmware with symbols. You can load this file in Ghidra to aid your reverse engineering during this assignment.

### Goals

Create a Dockerfile which copies over the provided files and sets up Unicorn and all its dependencies.

Rehost the function `assignment_2B_rehost` using Unicorn and retrieve the PIN:

- Initialize Unicorn, including register state and memory regions.
- Identify functions which need to be skipped and create corresponding hooks.
- Identify functions for output and provide corresponding hooks.
- Identify the function reading the input and provide a hook writing the input to the right location in memory.
- Execute your rehosted function in a loop, using a different guess for the PIN on each iteration.
- If guessed successfully, you will see the flag in the output.

### Hints

- You can choose a language of your choice for interacting with Unicorn. Python is recommended.
- Unicorn for Python can be installed using:

```bash
python3 -m pip install unicorn
```

- Unicorn includes samples which can be used as reference. For Python, `test_arm.py` can be used as a basis for your rehosting script.
- To skip a full function, create a code hook at the entry point of the function. Then write the contents of the link register to the program counter register and exit the hook.
- The valid PIN is in the range:

```text
[0,9999]
```

- Make sure your addresses include the Thumb bit.
- Try to make your rehosting efficient. Installing hooks on specific addresses is more efficient than using a global hook.
- Do not try to reverse engineer the `decrypt_rehosting_flag` function. Let the rehosting do the work.

---

# Deliverables

A brief PDF report (maximum 2 pages) containing:

- The 3 flags
- A screenshot containing the correct UART settings
- A screenshot containing the correct SPI settings
- A textual explanation of how you managed to find the UART settings
- A textual explanation of how you managed to find the pins and the SPI settings
- A textual explanation of the functions you had to hook/intercept to solve the rehosting challenge

Additional files:

- Rehosting script and auxiliary files it relies on
- Dockerfile
- run.sh

## Submission Requirements

The `run.sh` file must successfully execute the Dockerfile with the rehosting program.

The container should run on a standard Linux machine with Docker installed.

Specifically:

1. Download the submission.
2. Navigate to the appropriate directory.
3. Execute:

```bash
./run.sh
```

No additional files will be added and no modifications will be made to the environment.

### Additional Requirements

- Containers should not take more than 5 minutes to build, excluding base image download time.
- Avoid using rolling, development, or latest Docker images.
- Name the submission:

```text
assignment2-teamXX.zip
```

- The submitted zip should be less than or equal to 5 MB unless clearly justified.
- The report should contain team member names and optionally email addresses.
- Do not include student IDs or unnecessary personal information.
