#!/usr/bin/env python3

digits = [ 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b ]

eeprom_data = bytearray(2048)

def writeEEPROM(address, data):
  eeprom_data[address] = data

def to_unsigned(val):
    return (val + 256) % 256

def take_digit(val, div):
    return int(abs(value / div)) % 10

print("Programming ones place")
for value in range(256):
    writeEEPROM(value, digits[take_digit(value, 1)])

print("Programming tens place")
for value in range(256):
    writeEEPROM(value + 256, digits[take_digit(value, 10)])

print("Programming hundreds place")
for value in range(256):
    writeEEPROM(value + 512, digits[take_digit(value, 100)])

print("Programming sign")
for value in range(256):
    writeEEPROM(value + 768, 0)

print("Programming ones place (twos complement)")
for value in range(-128, 128):
    writeEEPROM(to_unsigned(value) + 1024, digits[take_digit(value, 1)])

print("Programming tens place (twos complement)")
for value in range(-128, 128):
    writeEEPROM(to_unsigned(value) + 1280, digits[take_digit(value, 10)])

print("Programming hundreds place (twos complement)")
for value in range(-128, 128):
    writeEEPROM(to_unsigned(value) + 1536, digits[take_digit(value, 100)])

print("Programming sign (twos complement)")
for value in range(-128, 128):
    if value < 0:
        writeEEPROM(to_unsigned(value) + 1792, 0x01)
    else:
        writeEEPROM(value + 1792, 0)

with open("display.bin", "wb") as f:
    f.write(eeprom_data)