#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.Util as Util


# function that read the key in a file
# input :
#   fichier = str
# output :
#   data = str
def read_key(keypath):
    with open(keypath, 'r') as rfile:
        hexa_key = rfile.read()

    return hex2key(hexa_key)


def write_key(keypath, name, formatted_key):
    hexa_key = key2hex(formatted_key)
    with open(keypath + name, 'w') as kfile:
        kfile.write(hexa_key)


# function that converts a list of int into a single hex
# the formatted key contains only strict 64 bit integers
# Every int will be encoded in 16 hexa characters
# input :
#   data_list = list of int
# output :
#   hexa : a string hexadecimal
def key2hex(formatted_key):
    flattened_key = Util.desorganize_datalistorder(formatted_key)
    hexa = '0x'
    for i in flattened_key:
        hexa += hex(i)[2:]
    return hexa


def hex2key(hexa):
    flattened_key = []
    hexa = hexa[2:]
    for i in range(0, len(hexa), 16):
        flattened_key.append(int(hexa[i:i + 16], 16))

    formatted_key = Util.organize_data_list(flattened_key, 8)
    return formatted_key
