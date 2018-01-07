#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.Hash as Hh
import src.Util as Util
from src import ThreeFish as Tf


# print key len and hexa key to the user
# key_len = int
# key = hexa string
def print_key(key_len, key):
    print("Voici votre clé symétrique sur ", key_len, "bits :",
          "\t\n######################################\t\n",
          key,
          "\t\n######################################")


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
        n = int(hexa[i:i + 16], 16)
        flattened_key.append(n)
    formatted_key = Util.organize_data_list(flattened_key, 8)
    return formatted_key


# Function that cipher a key with CBC method
# Inputs:
#   password = string that will serve as key in the cipher
#   key = a list of ints to cipher with cbc
# Outputs:
#   The key encoded with CBC and 512 bit blocks
def cipher_key(password, key):
    pass_hash = Hh.blake_hash(password, 64)
    formatted_hash = Util.encode_int_list([pass_hash])
    turn_keys = Tf.keygenturn(formatted_hash)
    formatted_key = format_key(key)
    ciph_key = Tf.cbc_threefish_cipher(formatted_key, turn_keys, 512)
    ciph_key = Util.desorganize_datalistorder(ciph_key)
    return format_key(ciph_key)


# Function that decipher a key with CBC method
# Inputs:
#   password = string that will serve as key in the cipher
#   key = a 2D tab of ints to decipher with cbc
# Outputs:
#   The key decoded with CBC
def decipher_key(password, ciphered_key):
    pass_hash = Hh.blake_hash(password, 64)
    formatted_hash = Util.encode_int_list([pass_hash])
    turn_keys = Tf.keygenturn(formatted_hash)
    ciphered_key = deformat_key(ciphered_key)
    ciphered_key = Util.organize_data_list(ciphered_key, 8)
    formatted_key = Tf.cbc_threefish_decipher(ciphered_key, turn_keys, 512)
    return deformat_key(formatted_key)


# Function that format list of integers into an organized list of 8 words of strict 64 bits integers.
# It serves to format a key before being ciphered with cbc
def format_key(key):
    formatted_key = Util.encode_int_list(key)
    formatted_key = Util.organize_data_list(formatted_key, 8)
    formatted_key = Util.add_padding_v2(formatted_key, 8, 64)
    return formatted_key


# Function that reverses the formatting of a key
# It serves to deformat a key before being deciphered with cbc
def deformat_key(formatted_key):
    key = Util.remove_padding_listv2(formatted_key, 8, 64)
    key = Util.desorganize_datalistorder(key)
    key = Util.decode_int_list(key)
    return key
