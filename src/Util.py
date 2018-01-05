#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
import src.Conversions as Conv
import src.Hash as Hh
import src.IO as IO
from src import ThreeFish as Tf

# print key len and hexa key to the user
# key_len = int
# key = str
def print_key(key_len, key):
    print("Voici votre clé symétrique sur ", key_len, "bits :",
          "\t\n######################################\t\n",
          key,
          "\t\n######################################")


# function that cipher a key with CBC method
# Inputs:
#   password = string that will serve as key in the cipher
#   key = a list of ints to cipher with cbc
# Outputs:
#   The key encoded with CBC and 512 bit blocks
def cipher_key(password, key):
    pass_hash = Hh.blake_hash(password, 64)
    formatted_hash = format_int_listv0([pass_hash], 64)
    turn_keys = Tf.keygenturn(formatted_hash)
    formatted_key = format_key(key)
    return Tf.cbc_threefish_cipher(formatted_key, turn_keys, 512)


def format_key(key):
    formatted_key = format_int_listv0(key, 64)
    formatted_key = IO.organize_data_list(formatted_key, 8)
    formatted_key = IO.ajout_padding_v2(formatted_key, 8, 8)
    return formatted_key


def deformat_key(formatted_key):
    key = IO.remove_padding_listv2(formatted_key, 8, 8)
    key = IO.desorganize_datalistorder(key)
    key = deformat_int_listv1(key)
    return key


# This function format the key in a list of 64 bit integers.
# Each integer is encoded as follows :
# | Flag (optional) | Payload | Payload_Size | Last |
# Inputs:
#   list = a list of big integers
#   bit_len = the bit length of each formatted int
# Outputs:
#   formatted_list = a list of formatted bits integers
def format_int_listv0(int_list, bit_len):
    size_len = len(bin(bit_len)[2:])
    payload_len = bit_len - size_len - 1
    formatted_list = []

    def add_complete_payload(b, b_len):
        size = pad_bin(bin(b_len)[2:], size_len)
        len_rand_bits = payload_len - b_len
        rand_bits = getrandbits(len_rand_bits)
        payload = b + pad_bin(bin(rand_bits)[2:], len_rand_bits)
        last = '1'
        formatted_list.append(int(payload + size + last, 2))

    def add_incomplete_payload(b):
        size = '1' * (size_len - 1)
        payload = b
        last = '0'
        flag = '1'
        formatted_list.append(int(flag + payload + size + last, 2))

    for i in int_list:
        bin_i = bin(i)[2:]
        bin_len_i = len(bin_i)
        if bin_len_i <= payload_len:
            add_complete_payload(bin_i, bin_len_i)
        else:
            payload_num = bin_len_i // payload_len
            for j in range(payload_num):
                add_incomplete_payload(bin_i[j:j+payload_len])

            remaining_bits = bin_i[payload_num:]

            if len(remaining_bits) > 0:
                add_complete_payload(remaining_bits, len(remaining_bits))

        return formatted_list


def format_int_listv1(int_list):
    formatted_list = []
    for i in int_list:
        b = bin(i)[2:]
        b_len = len(b)

        def add_singlebloc(bloc_bits, bloc_len):
            pad_len = 64 - bloc_len
            pad_bits = pad_bin(bin(getrandbits(pad_len))[2:], pad_len)
            next_int = int(bloc_bits + pad_bits, 2)
            formatted_list.append(next_int)

        if b_len <= 64:
            len_bloc = pad_bin(bin(b_len)[2:], 6)
            rand_bits = pad_bin(bin(getrandbits(56))[2:], 56)
            # We force the first bit to 1 so we ensure the int to be on 64 bits
            # The second bit is a boolean which indicates if the next_int is encoded
            # on a single bloc or not
            format_len = '11' + rand_bits + len_bloc
            formatted_list.append(int(format_len, 2))
            add_singlebloc(b, b_len)
        else:
            num_full_bloc = b_len // 63
            num_bloc_bin = pad_bin(bin(num_full_bloc)[2:], 56)
            len_last_bloc = b_len % 63
            has_last_bloc = False
            if len_last_bloc > 0:
                has_last_bloc = True
            len_last_bloc = pad_bin(bin(len_last_bloc)[2:], 6)
            format_len = '10' + num_bloc_bin + len_last_bloc
            formatted_list.append(int(format_len, 2))
            for j in range(num_full_bloc):
                formatted_list.append(int('1' + b[j*63:(j+1)*63], 2))
            if has_last_bloc:
                last_bloc = '1' + b[num_full_bloc*63:]
                add_singlebloc(last_bloc, len(last_bloc))

    return formatted_list


def deformat_int_listv1(formatted_list):
    int_list = []
    pos = 0
    len_list = len(formatted_list)
    while pos < len_list - 1:
        format_len = bin(formatted_list[pos])[2:]
        pos += 1
        next_int_bits = bin(formatted_list[pos])[2:]
        pos += 1
        is_single_bloc = format_len[1]
        if is_single_bloc == '1':
            b_len = int(format_len[58:], 2)
            print(b_len)
            next_int = int(next_int_bits[:b_len], 2)
            print(next_int)
            int_list.append(next_int)
        else:
            num_full_block = int(format_len[2:58], 2)
            len_last_block = int(format_len[58:], 2)
            next_int_bin = next_int_bits[1:]
            for j in range(num_full_block):
                print(pos)
                b = bin(formatted_list[pos])[2:]
                pos += 1
                next_int_bin += b[1:]
            if len_last_block > 0:
                b = bin(formatted_list[pos])[2:]
                pos += 1
                last_bin = b[:len_last_block+1]
                next_int_bin += last_bin
            int_list.append(int(next_int_bin, 2))
    return int_list


def pad_bin(bin_str, size):
    length = len(bin_str)
    if length < size:
        bin_str = '0' * (size - length) + bin_str
    return bin_str


# function that do a right rotation
# bin_str = list of string
# rot = int
# bin_str2int(rot_array) = int
def rotate_right(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[(array_len - rot):array_len] + bin_str[0:(array_len - rot)]
    return Conv.bin_str2int(rot_array)


# function that do a left rotation
# bin_str = list of string
# rot = int
# bin_str2int(rot_array) = int
def rotate_left(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[rot:array_len] + bin_str[0:rot]
    return Conv.bin_str2int(rot_array)
