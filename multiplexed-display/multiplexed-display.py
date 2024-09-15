#!/usr/bin/env python3

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
        ]

DIGIT_BLANK = 0
DIGIT_MINUS = SEG_BIT_G


# The size of 28C16 EEPROM is 2 KiB
EEPROM_SIZE = 2048

# Offsets, where different parts of a number are stored
ONES_OFFSET = 0
TENS_OFFSET = ONES_OFFSET + 256
HUND_OFFSET = TENS_OFFSET + 256
SIGN_OFFSET = HUND_OFFSET + 256

# Two's complement starts
TWO_COMP_OFFSET = 256 * 4

# Array where to accumulate the bytes before writing them out
eeprom_data = bytearray(EEPROM_SIZE)

def to_unsigned(val):
    """ Convert signed single-byte integer to unsigned. Equivalent of casting to uint8_t in C language.
        Positive values are unchanged, negative ones are converted to their bit-equivalent positive ones.
        For example: -1 (0b11111111) is converted to 255 (which also is 0b11111111).
    """
    return (val + 256) % 256

def take_digit(val, div):
    """ Extract digit from a number. The value of divisor (1, 10 or 100) specifies which one to get.
        Works for both positive and negative numbers.
    """
    return int(abs(value / div)) % 10


print("Programming ones place")
for value in range(256):
    eeprom_data[value + ONES_OFFSET] = digits[take_digit(value, 1)]

print("Programming tens place")
for value in range(256):
    eeprom_data[value + TENS_OFFSET] = digits[take_digit(value, 10)]

print("Programming hundreds place")
for value in range(256):
    eeprom_data[value + HUND_OFFSET] = digits[take_digit(value, 100)]

print("Programming sign")
for value in range(256):
    eeprom_data[value + SIGN_OFFSET] = DIGIT_BLANK

print("Programming ones place (twos complement)")
for value in range(-128, 128):
    eeprom_data[to_unsigned(value) + ONES_OFFSET + TWO_COMP_OFFSET] = digits[take_digit(value, 1)]

print("Programming tens place (twos complement)")
for value in range(-128, 128):
    eeprom_data[to_unsigned(value) + TENS_OFFSET + TWO_COMP_OFFSET] = digits[take_digit(value, 10)]

print("Programming hundreds place (twos complement)")
for value in range(-128, 128):
    eeprom_data[to_unsigned(value) + HUND_OFFSET + TWO_COMP_OFFSET] = digits[take_digit(value, 100)]

print("Programming sign (twos complement)")
for value in range(-128, 128):
    if value < 0:
        eeprom_data[to_unsigned(value) + SIGN_OFFSET + TWO_COMP_OFFSET] = DIGIT_MINUS
    else:
        eeprom_data[value + SIGN_OFFSET + TWO_COMP_OFFSET] = DIGIT_BLANK

print("Saving to 'display.bin' file")
with open("display.bin", "wb") as f:
    f.write(eeprom_data)