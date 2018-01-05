#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binascii


# function that convert an int value into a hexa
# n = int
# str(hexk) = hexa
def int2hex(n):
    hexk = hex(n).replace('0x', '', 1)
    return str(hexk)


# function that convert a 64 bits int value into a list of str
# to_convert = int
# result = list of str
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


# function that convert a 64 bits int value into a list of str
# to_convert = int
# result = list of str
def int2bin_str_v2(to_convert):
    return bin(to_convert)


def str2int(to_convert):
    b = to_convert.encode('utf-8')
    return int(binascii.hexlify(b), 16)


def str2bytes(to_convert=""):
    return to_convert.encode('utf-8')


def str2bin_str(to_convert):
    return bin(str2int(to_convert))


def int2str(to_convert):
    h = hex(to_convert)[2:]
    b = binascii.unhexlify(h)
    return b.decode('utf-8')


# function that convert a list of str into an 64bits int
# to_convert = list of str
# int(convert, 2) = int
def bin_str_list2int(to_convert):
    convert = "".join(to_convert)
    return int(convert, 2)


# function that convert a str value into an int value
# to_convert = str
# int(to_convert, 2) = int
def bin_str2int(to_convert):
    return int(to_convert, 2)
