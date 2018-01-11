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


# do a xor between 2 lists of int
# input :
#   list0 = list
#   list1 = list
# output :
#   output = list
def xor_lists(list0, list1):
    output = []
    for i in range(0, len(list0)):
        result = list0[i] ^ list1[i]
        output.append(result)
    return output


# do an add between 2 list of binary str value
# input :
#   bin_str0 = list of str
#   bin_str1 = list of str
# output :
#   result = str
def add_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) + int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result



# do a substract between 2 list of binary str value
# input :
#   bin_str0 = list of str
#   bin_str1 = list of str
# output :
#   result = str
def subtract_64bits(bin_str0, bin_str1):
    result = str(bin((int(bin_str0, 2) - int(bin_str1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


# do a modular add between 2 2D array of int
# input :
#   data_list = 2D array of int
#   tab_keys = 2D array of int
# output :
#   output = 2D array of int
def add_list_64bits(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output


# do a modular substract between 2 2D array of int
# input :
#   data_list = 2D array of int
#   tab_keys = 2D array of int
# output :
#   output = 2D array of int
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

# find the reverse value of an int with an int modular value
# input :
#   a = int
#   mod = int
# output = int
def inv(a, mod):
    (r, u, v) = bezout(a, mod)
    return u % mod
