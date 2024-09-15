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
           SEG_BIT_A | SEG_BIT_B | SEG_BIT_C | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,             # A
           SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                         # B
           SEG_BIT_A | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F,                                     # C
           SEG_BIT_B | SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_G,                         # D
           SEG_BIT_A | SEG_BIT_D | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                         # E
           SEG_BIT_A | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G,                                     # F
        ]

DIGIT_BLANK = 0
CHAR_MINUS = SEG_BIT_G
CHAR_h = SEG_BIT_C | SEG_BIT_E | SEG_BIT_F | SEG_BIT_G
CHAR_o = SEG_BIT_C | SEG_BIT_D | SEG_BIT_E | SEG_BIT_G


# The size of 28C16 EEPROM is 2 KiB, adjust this for larger EEPROMs
EEPROM_SIZE = 2048

# Offsets, where different parts of a number are stored
ONES_OFFSET = 0
TENS_OFFSET = ONES_OFFSET + 256
HUND_OFFSET = TENS_OFFSET + 256
SIGN_OFFSET = HUND_OFFSET + 256

# Space on EEPROM occupied by each "mode"
MODE_SIZE = 256 * 4

# Array where to accumulate the bytes before writing them out
eeprom_data = bytearray(EEPROM_SIZE)

def to_unsigned(val):
    """ Convert signed single-byte integer to unsigned. Equivalent of casting to uint8_t in C language.
        Positive values are unchanged, negative ones are converted to their bit-equivalent positive ones.
        For example: -1 (0b11111111) is converted to 255 (which also is 0b11111111).
    """
    return (val + 256) % 256

def take_digit(value, div, base):
    """ Extract digit from a number. The value of divisor (1, 10 or 100) specifies which one to get.
        Works for both positive and negative numbers.
    """
    return int(abs(value / div)) % base


def write_decimal_unsigned(start):
    print("Programming unsigned decimal")
    for value in range(256):
        eeprom_data[value + ONES_OFFSET + start] = digits[take_digit(value, 1, 10)]
        eeprom_data[value + TENS_OFFSET + start] = digits[take_digit(value, 10, 10)]
        eeprom_data[value + HUND_OFFSET + start] = digits[take_digit(value, 100, 10)]
        eeprom_data[value + SIGN_OFFSET + start] = DIGIT_BLANK

def write_decimal_signed(start):
    print("Programming signed decimal (twos complement)")
    for value in range(-128, 128):
        eeprom_data[to_unsigned(value) + ONES_OFFSET + start] = digits[take_digit(value, 1, 10)]
        eeprom_data[to_unsigned(value) + TENS_OFFSET + start] = digits[take_digit(value, 10, 10)]
        eeprom_data[to_unsigned(value) + HUND_OFFSET + start] = digits[take_digit(value, 100, 10)]
        eeprom_data[to_unsigned(value) + SIGN_OFFSET + start] = CHAR_MINUS if value < 0 else DIGIT_BLANK

def write_hex(start):
    print("Programming hex")
    for value in range(256):
        eeprom_data[value + ONES_OFFSET + start] = digits[take_digit(value, 0x1, 16)]
        eeprom_data[value + TENS_OFFSET + start] = digits[take_digit(value, 0x10, 16)]
        eeprom_data[value + HUND_OFFSET + start] = DIGIT_BLANK
        eeprom_data[value + SIGN_OFFSET + start] = CHAR_h

def write_oct(start):
    print("Programming oct")
    for value in range(256):
        eeprom_data[value + ONES_OFFSET + start] = digits[take_digit(value, 0o1, 8)]
        eeprom_data[value + TENS_OFFSET + start] = digits[take_digit(value, 0o10, 8)]
        eeprom_data[value + HUND_OFFSET + start] = digits[take_digit(value, 0o10, 8)]
        eeprom_data[value + SIGN_OFFSET + start] = CHAR_o


def store_to_file():
    print("Saving to 'display.bin' file")
    with open("display.bin", "wb") as f:
        f.write(eeprom_data)


if __name__ == "__main__":
    write_decimal_unsigned(MODE_SIZE * 0)
    write_decimal_signed(MODE_SIZE * 1)

    # Larger EEPROM is required for more display modes
    #write_hex(MODE_SIZE * 2)
    #write_oct(MODE_SIZE * 3)

    store_to_file()
