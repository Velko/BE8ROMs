#!/usr/bin/env python3

# The size of 28C16 EEPROM is 2 KiB, adjust this for larger EEPROMs
EEPROM_SIZE = 2048

HLT = 0b1000000000000000  # Halt clock
MI  = 0b0100000000000000  # Memory address register in
RI  = 0b0010000000000000  # RAM data in
RO  = 0b0001000000000000  # RAM data out
IO  = 0b0000100000000000  # Instruction register out
II  = 0b0000010000000000  # Instruction register in
AI  = 0b0000001000000000  # A register in
AO  = 0b0000000100000000  # A register out
EO  = 0b0000000010000000  # ALU out
SU  = 0b0000000001000000  # ALU subtract
BI  = 0b0000000000100000  # B register in
OI  = 0b0000000000010000  # Output register in
CE  = 0b0000000000001000  # Program counter enable
CO  = 0b0000000000000100  # Program counter out
J   = 0b0000000000000010  # Jump (program counter in)
FI  = 0b0000000000000001  # Flags in

# combinations of flag bits
FLAGS_Z0C0 = 0b00
FLAGS_Z0C1 = 0b01
FLAGS_Z1C0 = 0b10
FLAGS_Z1C1 = 0b11

# opcode numbers of conditional jump instructions
JC = 0b0111
JZ = 0b1000

# marker for conditional jump microstep, defaults to not-jump
CJMP = 0

UCODE_TEMPLATE = [
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 0000 - NOP
    [ MI|CO,  RO|II|CE,  IO|MI,  RO|AI,  0,           0, 0, 0 ], # 0001 - LDA
    [ MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|FI,    0, 0, 0 ], # 0010 - ADD
    [ MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|SU|FI, 0, 0, 0 ], # 0011 - SUB
    [ MI|CO,  RO|II|CE,  IO|MI,  AO|RI,  0,           0, 0, 0 ], # 0100 - STA
    [ MI|CO,  RO|II|CE,  IO|AI,  0,      0,           0, 0, 0 ], # 0101 - LDI
    [ MI|CO,  RO|II|CE,  IO|J,   0,      0,           0, 0, 0 ], # 0110 - JMP
    [ MI|CO,  RO|II|CE,  CJMP,   0,      0,           0, 0, 0 ], # 0111 - JC
    [ MI|CO,  RO|II|CE,  CJMP,   0,      0,           0, 0, 0 ], # 1000 - JZ
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 1001
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 1010
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 1011
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 1100
    [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ], # 1101
    [ MI|CO,  RO|II|CE,  AO|OI,  0,      0,           0, 0, 0 ], # 1110 - OUT
    [ MI|CO,  RO|II|CE,  HLT,    0,      0,           0, 0, 0 ], # 1111 - HLT
]

# Array where to accumulate the bytes before writing them out
# Pre-filled with 0xFF, to match state of a blank EEPROM
eeprom_data = bytearray(b'\xFF') * EEPROM_SIZE

import copy

def initUCode():
    ucode = {}

    # make copies of the microcode template and patch them
    # for conditional jumps by replacing appropiate CJMP markers
    # with a step that loads new value in PC

    # ZF = 0, CF = 0
    ucode[FLAGS_Z0C0] = copy.deepcopy(UCODE_TEMPLATE)

    # ZF = 0, CF = 1
    ucode[FLAGS_Z0C1] = copy.deepcopy(UCODE_TEMPLATE)
    ucode[FLAGS_Z0C1][JC][2] = IO|J

    # ZF = 1, CF = 0
    ucode[FLAGS_Z1C0] = copy.deepcopy(UCODE_TEMPLATE)
    ucode[FLAGS_Z1C0][JZ][2] = IO|J

    # ZF = 1, CF = 1
    ucode[FLAGS_Z1C1] = copy.deepcopy(UCODE_TEMPLATE)
    ucode[FLAGS_Z1C1][JC][2] = IO|J
    ucode[FLAGS_Z1C1][JZ][2] = IO|J

    return ucode


def prepare_eeprom():
    ucode = initUCode()

    # Program data bytes
    print("Programming EEPROM")

    # Program the bits of microcode into the EEPROM
    for address in range(1024):
        # Extract address bits according to their purpose:
        # FF C IIII SSS
        flags       = (address & 0b1100000000) >> 8  # FF
        chip_sel    = (address & 0b0010000000) >> 7  # C
        instruction = (address & 0b0001111000) >> 3  # IIII
        step        = (address & 0b0000000111)       # SSS

        if chip_sel:
            eeprom_data[address] = ucode[flags][instruction][step] & 0xFF
        else:
            eeprom_data[address] = ucode[flags][instruction][step] >> 8

def save_to_file():
    print("Saving to 'microcode-eeprom-with-flags.bin' file")
    with open("microcode-eeprom-with-flags.bin", "wb") as f:
        f.write(eeprom_data)

if __name__ == "__main__":
    prepare_eeprom()
    save_to_file()
