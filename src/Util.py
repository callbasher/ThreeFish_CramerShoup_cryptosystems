#!/usr/bin/python3
# -*- coding: utf-8 -*-


# function that convert an int value into a hexa
# input = int
# output = hexa
def int2str_hexa(n):
    hexk = hex(n).replace('\'', '').replace('0x', '', 1)
    return str(hexk)


# function that convert a 64 bits int value into a list of str
# intput = int
# output = list of str
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
# input = list of str
# output = int
def bin_str_list2int(to_convert):
    convert = "".join(to_convert)
    return int(convert, 2)


# function that convert a str value into an int value
# input = str
# output = int
def bin_str2int(to_convert):
    return int(to_convert, 2)


# function that xor 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def xor_bytes(bin_str0, bin_str1):
    result = str(bin(int(bin_str0, 2) ^ int(bin_str1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


# function that xor 2 lists
# input0 = list
# input1 = list
# output = list
def xor_lists(list0, list1):
    output = []
    for i in range(0, len(list0)):
        result = list0[i] ^ list1[i]
        output.append(result)
    return output


# function that add 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def add_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) + int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result


# function that substract 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def subtract_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) - int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


# function that modular add 2 lists
# input0 = tab of list
# input1 = tab of list
# output = tab of list
def add_list_64bits(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output


# function that modular substract 2 lists
# input0 = tab of list
# input1 = tab of list
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
# input = list of string
# output = int
def rotate_right(b_array, rot):
    array_len = len(b_array)
    rot_array = b_array[(array_len - rot):array_len] + b_array[0:(array_len - rot)]
    # return an int value
    return bin_str2int(rot_array)


# function that do a left rotation
# input = list of string
# output = int
def rotate_left(b_array, rot):
    array_len = len(b_array)
    rot_array = b_array[rot:array_len] + b_array[0:rot]
    # return an int value
    return bin_str2int(rot_array)


def pad(m, len):
    return m
