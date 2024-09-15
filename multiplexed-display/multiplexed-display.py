#!/usr/bin/env python3

digits = [ 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b ]

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
    eeprom_data[value + SIGN_OFFSET] = 0

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
        eeprom_data[to_unsigned(value) + SIGN_OFFSET + TWO_COMP_OFFSET] = 0x01
    else:
        eeprom_data[value + SIGN_OFFSET + TWO_COMP_OFFSET] = 0

print("Saving to 'display.bin' file")
with open("display.bin", "wb") as f:
    f.write(eeprom_data)