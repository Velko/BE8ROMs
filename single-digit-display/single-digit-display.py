#!/usr/bin/env python3

# The size of 28C16 EEPROM is 2 KiB, adjust this for larger EEPROMs
EEPROM_SIZE = 2048

# Supported display types
COMMON_CATHODE = 0x00
COMMON_ANODE = 0xFF

# Choose display type (COMMON_CATHODE or COMMON_ANODE)
DISPLAY_TYPE = COMMON_ANODE


# Re-arrange the segment bits, if display is wired differently
SEG_BIT_DOT = 1 << 7
SEG_BIT_A   = 1 << 6
SEG_BIT_B   = 1 << 5
SEG_BIT_C   = 1 << 4
SEG_BIT_D   = 1 << 3
SEG_BIT_E   = 1 << 2
SEG_BIT_F   = 1 << 1
SEG_BIT_G   = 1 << 0


# Segments:
#   +-- a --+
#   |       |
#   f       b
#   |       |
#   +-- g --+
#   |       |
#   e       c
#   |       |
#   +-- d --+


digits = [ SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F,             # 0
           SEG_BIT_B | SEG_BIT_C,                                                             # 1
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_D | SEG_BIT_E | SEG_BIT_G,                         # 2
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_G,                         # 3
           SEG_BIT_B | SEG_BIT_C | SEG_BIT_F | SEG_BIT_G,                                     # 4
           SEG_BIT_A | SEG_BIT_C | SEG_BIT_D | SEG_BIT_F | SEG_BIT_G,                         # 5
           SEG_BIT_A | SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,             # 6
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C,                                                 # 7
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G, # 8
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_F | SEG_BIT_G,             # 9
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,             # A
           SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                         # B
           SEG_BIT_A | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F,                                     # C
           SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_G,                         # D
           SEG_BIT_A | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                         # E
           SEG_BIT_A | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                                     # F
        ]

# Array where to accumulate the bytes before writing them out
# Pre-filled with 0xFF, to match state of a blank EEPROM
eeprom_data = bytearray(b'\xFF') * EEPROM_SIZE

def store_to_file():
    print("Saving to 'single-digit-display.bin' file")
    with open("single-digit-display.bin", "wb") as f:
        f.write(eeprom_data)

def write_digits():
    print("Preparing digit patterns")
    for i in range(16):
        eeprom_data[i] = digits[i] ^ DISPLAY_TYPE

if __name__ == "__main__":
    write_digits()
    store_to_file()
