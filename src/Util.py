#!/usr/bin/python3
# -*- coding: utf-8 -*-


# function that convert an int value into a hexa
# n = int
# str(hexk) = hexa
def int2str_hexa(n):
    hexk = hex(n).replace('\'', '').replace('0x', '', 1)
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


# function that xor 2 list of binary str value
# bin_str0 = list of str
# bin_str1 = list of str
# result = str
def xor_bytes(bin_str0, bin_str1):
    result = str(bin(int(bin_str0, 2) ^ int(bin_str1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


# function that xor 2 lists
# list0 = list
# list1 = list
# output = list
def xor_lists(list0, list1):
    output = []
    for i in range(0, len(list0)):
        result = list0[i] ^ list1[i]
        output.append(result)
    return output


# function that add 2 list of binary str value
# bin_str0 = list of str
# bin_str1 = list of str
# result = str
def add_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) + int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result


# function that substract 2 list of binary str value
# bin_str0 = list of str
# bin_str1 = list of str
# result = str
def subtract_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) - int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


# function that modular add 2 lists
# data_list = tab of list
# tab_keys = tab of list
# output = tab of list
def add_list_64bits(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output


# function that modular substract 2 lists
# data_list = tab of list
# tab_keys = tab of list
# output = tab of list
def subtract_list_64bits(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i]) % 2 ** 64
        output.append(result)
    return output


def bezout(a, b):
    (r, u, v, r1, u1, v1) = (a, 1, 0, b, 0, 1)
    while r1 != 0:
        q = int(r / r1)
        (r, u, v, r1, u1, v1) = (r1, u1, v1, r - q * r1, u - q * u1, v - q * v1)
    return r, u, v


def inv(a, mod):
    (r, u, v) = bezout(a, mod)
    return u % mod


# function that do a right rotation
# bin_str = list of string
# rot = int
# bin_str2int(rot_array) = int
def rotate_right(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[(array_len - rot):array_len] + bin_str[0:(array_len - rot)]
    return bin_str2int(rot_array)


# function that do a left rotation
# bin_str = list of string
# rot = int
# bin_str2int(rot_array) = int
def rotate_left(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[rot:array_len] + bin_str[0:rot]
    return bin_str2int(rot_array)


def pad(m, len):
    return m
