#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binascii


# convert a 64 bits int value into a list of str
# input :
#   to_convert = int
# output :
#   result = list of str
def int2bin_str(to_convert):
    to_convert = int(to_convert)
    output = []
    result = []
    int_bytes = 8
    mask = 0xFF

    for i in range(0, int_bytes):
        output.insert(0, to_convert & mask)
        to_convert >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        result.append(i)
    result = "".join(result)
    result = str(result)
    return result


# convert a str value into an int value
# input :
#   to_convert = str
# output = int
def str2int(to_convert):
    b = to_convert.encode('utf-8')
    return int(binascii.hexlify(b), 16)


# convert a str value into a byte value
# input :
#   to_convert = str
# output = byte
def str2bytes(to_convert=""):
    return to_convert.encode('utf-8')


# function that convert a str value into an int value
# input :
#   to_convert = str
# output :
#   int(to_convert, 2) = int
def bin_str2int(to_convert):
    return int(to_convert, 2)


def bytes2int_list(to_convert, byte_len):
    int_list = []
    for i in range(0, len(to_convert), byte_len):
        b = to_convert[i:i+byte_len]
        n = int.from_bytes(b, byteorder='little', signed=False)
        int_list.append(n)

    return int_list


def int_list2bytes(to_convert, byte_len):
    bytes = b''
    last = len(to_convert) - 1
    for i in range(last):
        bytes += to_convert[i].to_bytes(byte_len, byteorder='little', signed=False)

    last_int = to_convert[last]
    hex_len = len(hex(last_int)[2:])
    last_byte_len = hex_len >> 1
    if hex_len % 8 != 0:
        last_byte_len += 1
    bytes += last_int.to_bytes(last_byte_len, byteorder='little', signed=False)

    return bytes
