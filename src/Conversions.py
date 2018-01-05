#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binascii


# convert an int value into a hexa value
# input :
#   n = int
# output = hexa
def int2hex(n):
    hexk = hex(n).replace('0x', '', 1)
    return str(hexk)


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


# convert a 64 bits int value into a bin_str
# input :
#   to_convert = int
# output = str
def int2bin_str_v2(to_convert):
    return bin(to_convert)


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


# convert a str value into a bin_str value
# input :
#   to_convert = str
# output = bin_str
def str2bin_str(to_convert):
    return bin(str2int(to_convert))


# convert an int value into a str value
# input :
#   to_convert = int
# output = str
def int2str(to_convert):
    h = hex(to_convert)[2:]
    b = binascii.unhexlify(h)
    return b.decode('utf-8')


# function that convert a list of str into an 64bits int
# input :
#   to_convert = list of str
# output :
#   int(convert, 2) = int
def bin_str_list2int(to_convert):
    convert = "".join(to_convert)
    return int(convert, 2)


# function that convert a str value into an int value
# input :
#   to_convert = str
# output :
#   int(to_convert, 2) = int
def bin_str2int(to_convert):
    return int(to_convert, 2)
