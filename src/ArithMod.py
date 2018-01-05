#!/usr/bin/python3
# -*- coding: utf-8 -*-


# function that xor 2 list of binary str value
# bin_str0 = list of str
# bin_str1 = list of str
# result = str
def xor_bin_str(bin_str0, bin_str1):
    result = bin(int(bin_str0, 2) ^ int(bin_str1, 2))[2:]
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
    result = bin((int(bin_str0, 2) + int(bin_str1, 2)) % 2**64)[2:]
    if len(result) < 64:
        result = '0' * (64 - len(result)) + result
    return result


# function that substract 2 list of binary str value
# bin_str0 = list of str
# bin_str1 = list of str
# result = str
def subtract_64bits(bin_str0, bin_str1):
    result = bin((int(bin_str0, 2) - int(bin_str1, 2)) % 2**64)[2:]
    if len(result) < 64:
        result = '0' * (64 - len(result)) + result
    return result


# function that modular add 2 lists
# data_list = tab of list
# tab_keys = tab of list
# output = tab of list
def add_list_64bits(data_list, tab_keys):
    output = []
    mod = 2**64
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % mod
        output.append(result)
    return output


# function that modular substract 2 lists
# data_list = tab of list
# tab_keys = tab of list
# output = tab of list
def subtract_list_64bits(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i])
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
