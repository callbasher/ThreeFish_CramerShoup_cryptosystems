#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


def int2hexa(n):
    hexk = hex(n)
    hexk = hexk.replace('\'', '')
    hexk = hexk.replace('0x', '', 1)
    hexk = str(hexk)
    return hexk


def intToByteArray(to_convert):
    to_convert = int(to_convert)
    output = []
    result = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, to_convert & mask)
        to_convert >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        result.append(i)
    result = "".join(result)
    result = str(result)
    return result


def strToInt(to_convert):
    return (int(to_convert, 2))


def xor_function(Barray0, Barray1):
    result = str(bin(int(Barray0, 2) ^ int(Barray1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


def additionMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) + int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result


def soustracMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) - int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result


def bytearrayToInt(to_convert):
    convert = "".join(to_convert)
    convert = int(convert, 2)
    return convert


def addition_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output


def soustraction_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i]) % 2 ** 64
        output.append(result)
    return output


def xor_2_lists(list1, list2):
    output = []
    for i in range(0, len(list1)):
        result = list1[i] ^ list2[i]
        output.append(result)
    return output
