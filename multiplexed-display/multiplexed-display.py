#!/usr/bin/env python3

digits = [ 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b ]

eeprom_data = bytearray(2048)

def to_unsigned(val):
    return (val + 256) % 256

def take_digit(val, div):
    return int(abs(value / div)) % 10

ONES_OFFSET = 0
TENS_OFFSET = ONES_OFFSET + 256
HUND_OFFSET = TENS_OFFSET + 256
SIGN_OFFSET = HUND_OFFSET + 256

TWO_COMP_OFFSET = 256 * 4

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

with open("display.bin", "wb") as f:
    f.write(eeprom_data)