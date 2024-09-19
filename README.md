# EEPROM image generators for Ben Eater's 8-bit computer

This collection of scripts are Python re-implementation of Ben Eater's [Arduino EEPROM programmer](https://github.com/beneater/eeprom-programmer/),
with a difference that it outputs .bin files instead.

Generated binary files should be written to EEPROMs using a programmer device, like TL866II, T48, [TommyPROM](https://github.com/TomNisbet/TommyPROM) or any other.

This code is [MIT licensed](http://en.wikipedia.org/wiki/MIT_License).

Original code (from which some parts might be copied over):
* Copyright 2017 Ben Eater

Python adaptation, extra configuration options, readability improvements and explanations:
* Copyright 2024 Jurģis Brigmanis

## Why?

Quite often a question pops up on [r/beneater](https://www.reddit.com/r/beneater/): "I have TL866 programmer and do not want to build the Arduino one. Do anybody have the EEPROM image files?"

There are copies of binaries available, but these are just "stock" images without an option to customize them. More advanced builders generally have written their own scripts to create EEPROM images, but their projects have moved beyound the "stock" stage already.

The goal is to provide scripts that create EEPROM images identical to original ones initially, and can be used as a starting point for customizations.

If you're just looking for the binary images to download, head over to [`/releases`](https://github.com/Velko/BE8ROMs/releases/latest) section.

## Contents

There are four different Python scripts that correspond to Arduino sketches in Ben Eater's [Arduino EEPROM programmer](https://github.com/beneater/eeprom-programmer/) repository.

Provided scripts produce the same byte-by-byte content as original sketches, but they can be easily adjusted if some aspect of targeted hardware differs. See comments in each script.

### 1. Single-digit display

The code in [`/single-digit-display`](/single-digit-display) corresponds to [Basic programmer](https://github.com/beneater/eeprom-programmer/?tab=readme-ov-file#1-basic-programmer), which in fact writes bytes to decode 4-bit values and drive a common-anode 7-segment display.

The script can be adjusted in case display segments are wired to different data pins, for use with common-cathode display or for different sizes of EEPROM.

### 2. Multiplexed display

The code in [`/multiplexed-display`](/multiplexed-display) corresponds to [8-bit decimal display](https://github.com/beneater/eeprom-programmer/?tab=readme-ov-file#2-8-bit-decimal-display), used to decode 8-bit values and drive a 4-digit 7-segment display.

The script can be adjusted in case display segments are wired to different data pins or for different sizes of EEPROM. Additionally, there are 2 extra
display modes provided: hexadecimal and octal. These are not enabled by default, as there is no space for them on 28C16 EEPROM. One should use larger
chip and adjust the script accordingly.

### 3. 8-bit computer microcode

The code in [`/microcode-eeprom`](/microcode-eeprom) corresponds to [8-bit computer microcode](https://github.com/beneater/eeprom-programmer/?tab=readme-ov-file#3-8-bit-computer-microcode), used by a pair of EEPROMs to serve as an instruction decoder for an 8-bit breadboard computer.

The script can be adjusted for different sizes of EEPROMs, additional instructions or if control signals are wired to different data pins.

### 4. 8-bit computer microcode with flags

The code in [`/microcode-eeprom-with-flags`](/microcode-eeprom-with-flags) corresponds to [8-bit computer microcode with flags register](https://github.com/beneater/eeprom-programmer/?tab=readme-ov-file#4-8-bit-computer-microcode-with-flags-register), adding the functionality of conditional jumps.
