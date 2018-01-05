#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
import src.Hash as Hh
from src import ThreeFish as Tf


# print key len and hexa key to the user
# key_len = int
# key = hexa string
def print_key(key_len, key):
    print("Voici votre clé symétrique sur ", key_len, "bits :",
          "\t\n######################################\t\n",
          key,
          "\t\n######################################")


# Function that cipher a key with CBC method
# Inputs:
#   password = string that will serve as key in the cipher
#   key = a list of ints to cipher with cbc
# Outputs:
#   The key encoded with CBC and 512 bit blocks
def cipher_key(password, key):
    pass_hash = Hh.blake_hash(password, 64)
    formatted_hash = encode_int_list([pass_hash])
    turn_keys = Tf.keygenturn(formatted_hash)
    formatted_key = format_key(key)
    return Tf.ecb_threefish_cipher(formatted_key, turn_keys)


# Function that decipher a key with CBC method
# Inputs:
#   password = string that will serve as key in the cipher
#   key = a 2D tab of ints to decipher with cbc
# Outputs:
#   The key decoded with CBC
def decipher_key(password, ciphered_key):
    pass_hash = Hh.blake_hash(password, 64)
    formatted_hash = encode_int_list([pass_hash])
    turn_keys = Tf.keygenturn(formatted_hash)
    formatted_key = Tf.ecb_threefish_decipher(ciphered_key, turn_keys)
    return deformat_key(formatted_key)


# Function that format a key into an organized list of 8 words of 64 bits
# It serves to format a key before being ciphered with cbc
def format_key(key):
    formatted_key = encode_int_list(key)
    formatted_key = organize_data_list(formatted_key, 8)
    formatted_key = add_padding_v2(formatted_key, 8, 8)
    return formatted_key


# Function that reverses the formatting of a key
# It serves to deformat a key before being deciphered with cbc
def deformat_key(formatted_key):
    key = remove_padding_listv2(formatted_key, 8, 8)
    key = desorganize_datalistorder(key)
    key = decode_int_list(key)
    return key


# function that organise a list into a 2D list with a certain number of words.
# Inputs:
#   data_list = list of elements
#   num_word = number of colums or words per line desired
# Outputs:
#   datalistorder = 2D organized list of elements
def organize_data_list(data_list, num_word):
    datalistorder = []
    for i in range(0, len(data_list), num_word):
        datalistorder.append(data_list[i:(i + num_word)])
    return datalistorder


# function that flattens a 2D list into a 1D list of elements
# Inputs:
#   datalistorder = the 2D list to flatten
# Outputs:
#   data_list = a 1D flattened list
def desorganize_datalistorder(datalistorder):
    data_list = []
    for l in datalistorder:
        for w in l:
            data_list.append(w)
    return data_list


# Function that add padding data to the data list
# If some words are missing in the last line, these words are padded
# If no words is missing, a complete new line is added with padded words
# The information about the number of padded words is contained in the last 8 bits
# of the last padded word
# Inputs:
#   datalistorder = 2D array of integers.
#   num_word = number of words wanted in each row of the array
#   len_word = size of the words in bytes
# Outputs:
#   datalistorder = a padded 2D array
def add_padding_v2(datalistorder, num_word, len_word):
    last_list = datalistorder[len(datalistorder) - 1]
    num_to_pad = num_word - len(last_list)

    # If the last line is complete, we add a full new line of padded words
    pad_list = []
    if num_to_pad == 0:
        num_to_pad = num_word
    else:
        pad_list = last_list
        datalistorder.remove(last_list)

    for i in range(1, num_to_pad):
        pad_list.append(getrandbits(len_word << 3))
    last_word = getrandbits((len_word-1) << 3).to_bytes(len_word-1, byteorder='little', signed=False)
    last_word += bytes([num_to_pad])
    pad_list.append(int.from_bytes(last_word, byteorder='little', signed=False))
    datalistorder.append(pad_list)

    return datalistorder


# Function that removes padding of an organized list. It reverses the operation of "add_padding"
# Inputs:
#   data = 2D organized list with padding
#   num_words = number of words per line in the list
#   word_len = size of the words in bytes
# Outputs:
#   data = 2D organized list without padding
def remove_padding_listv2(data, num_words, word_len):
    # last list of the tab contains the padding
    last_list = data[len(data) - 1]
    last_elem = last_list[num_words - 1]
    last_elem_bytes = last_elem.to_bytes(word_len, byteorder='little', signed=False)
    num_pad_words = last_elem_bytes[word_len - 1]
    if num_pad_words == num_words:
        del data[len(data) - 1]
    else:
        to_keep = last_list[:num_words - num_pad_words]
        del data[len(data) - 1]
        data.append(to_keep)
    return data


# Remove padding of an int in a list
# input :
#   data = 2D array of int
#   bloc_len = int (256, 512 or 1024)
# output :
#   data = 2D array of int
#   pad_len = int
def remove_padding_data(data, bloc_len):
    bloc_byte_len = int(bloc_len / 8)
    pad_list = data[len(data) - 1]
    last_elem = pad_list[len(pad_list) - 1]
    last_elem_bytes = last_elem.to_bytes(bloc_byte_len, byteorder='little', signed=False)
    pad_len = int(last_elem_bytes[len(last_elem_bytes) - 1])
    if pad_len == bloc_byte_len:
        del pad_list[len(pad_list) - 1]
    else:
        bytes_to_keep = last_elem_bytes[(pad_len - 1):(bloc_byte_len - 1)]
        to_keep = int.from_bytes(bytes_to_keep, byteorder='little', signed=False)
        del pad_list[len(pad_list) - 1]
        pad_list.append(to_keep)
    return data, pad_len


# Add padding data if the 2D array of int last list length is not enought
# input :
#   datalistorder = 2D array of int
#   ciph_bloc_len = int (256,512 or 1024)
#   len_bloc = int
# output :
#   datalistorder = 2D array of int
def ajout_padding(datalistorder, ciph_bloc_len, len_bloc):
    last_list = datalistorder[len(datalistorder) - 1]
    len_bloc_bytes = int(len_bloc / 8)
    # if the last list length match with (4, 8 or 16) then do padding
    if len(last_list) == int(ciph_bloc_len / 64):
        # a list of N(4, 8, 16) - 1 random int is add
        new_last_list = []
        for i in range(0, int(ciph_bloc_len / 64) - 1):
            new_last_list.append(getrandbits(len_bloc))
        pad_info = getrandbits(len_bloc - 8)
        nbr_pad = int(ciph_bloc_len / 64)
        pad_info = pad_info.to_bytes(len_bloc_bytes - 1, byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        new_last_list.append(pad_info)
        datalistorder.append(new_last_list)
    else:
        # if only one word need to be add in the last list
        if len(last_list) + 1 == int(ciph_bloc_len / 64):
            nbr_rand = getrandbits(len_bloc - 8)
            pad_info = nbr_rand.to_bytes(len_bloc_bytes - 1, byteorder='little', signed=False)
            pad_info = pad_info + bytes([1])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            # last int add in last list
            last_list.append(pad_info)
        else:
            last_list_len = int(ciph_bloc_len / 64) - len(last_list)
            for i in range(0, last_list_len - 1):
                last_list.append(getrandbits(len_bloc))
            nbr_rand = getrandbits(len_bloc - 8)
            pad_info = nbr_rand.to_bytes(len_bloc_bytes - 1, byteorder='little', signed=False)
            pad_info = pad_info + bytes([last_list_len])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            last_list.append(pad_info)
    return datalistorder


# removes padding of an organized list. It reverses the operation of "ajout_padding"
# intput :
#   data = 2D array of int
#   ciph_bloc_len = int (256, 512 or 1024)
#   len_bloc = int
# output :
#   data = 2D array of int
def remove_padding_list(data, ciph_bloc_len, len_bloc):
    len_bloc_bytes = int(len_bloc / 8)
    # last list of the tab contains the padding
    pad_list = data[len(data) - 1]
    last_elem = pad_list[len(pad_list) - 1]
    last_elem_bytes = last_elem.to_bytes(len_bloc_bytes, byteorder='little', signed=False)
    pad_len = int(last_elem_bytes[len_bloc_bytes - 1])
    if pad_len == int(ciph_bloc_len / 64):
        del data[len(data) - 1]
    else:
        to_keep = pad_list[:len(pad_list) - pad_len]
        del data[len(data) - 1]
        data.append(to_keep)
    return data


# This function encode a list of int in a list of strict 64 bit integers, in such
# a way that they can be retrieve by the inverse function "decode_int_list"
# An integer is encoded as follows:
#   - A 64 bits word for storing the information relative to the next encoded int
#   - n * 64 bit words to store the bits of the int being encoded
# The first word contains the information about the int and is formatted as follows:
#
#           | 1 |  Word number (57 bits) | Last Word Len (6 bits) |
#
# The first bit is set to 1 so the conversion to an int always gives a 64-bit integer.
# The word number corresponds to the number of words used to encode the int
# The last word might be padded with random bits, so Last Word Len corresponds to the number of bits
# containing information in the last word
# Each integer is encoded as follows :
#                           | 1 | Payload (63 bits) |
# The first bit is set to 1 so we ensure that a word is always on 64 bits.
# Inputs:
#   list = a list of integers of whatever size
# Outputs:
#   formatted_list = a list of 64 bit encoded integers
def encode_int_list(int_list):
    formatted_list = []
    for i in int_list:
        b = bin(i)[2:]
        b_len = len(b)

        if b_len == 0:
            raise ValueError("Cannot encode an empty int")

        def add_word(bloc_bits, start, bloc_len):
            # If the int is already 64 bit
            if bloc_len == 64:
                next_int = int(bloc_bits[start:start+64], 2)
            # If we don't need to pad
            elif bloc_len == 63:
                next_int = int('1' + bloc_bits[start:start+63], 2)
            else:
                pad_len = 64 - bloc_len - 1
                pad_bits = pad_bin(bin(getrandbits(pad_len))[2:], pad_len)
                next_int = int('1' + bloc_bits[start:start+bloc_len] + pad_bits, 2)

            formatted_list.append(next_int)

        # If the int can be encoded in one word
        if b_len <= 64:
            num_word = 0
            num_word_bin = pad_bin('0', 57)
            # Reduce the bit length of 1 so 64 can be encoded on 6 bits
            len_last_bloc = pad_bin(bin(b_len-1)[2:], 6)
        else:
            num_word = b_len // 63
            num_word_bin = pad_bin(bin(num_word)[2:], 57)
            b_len = b_len % 63
            len_last_bloc = pad_bin(bin(b_len)[2:], 6)

        format_len = '1' + num_word_bin + len_last_bloc
        formatted_list.append(int(format_len, 2))

        for j in range(num_word):
            add_word(b, j*63, 63)

        if b_len > 0:
            add_word(b, num_word*63, b_len)

    return formatted_list


# This function reverses the encoding done with encode_int_list
# Inputs:
#   formatted_list = a list of formatted 64 bit integers
# Outputs:
#   int_list = the list of restored integers
def decode_int_list(formatted_list):
    int_list = []
    pos = 0
    len_list = len(formatted_list)

    def next_bin_int(i):
        bin_int = bin(formatted_list[i])[2:]
        i += 1
        return i, bin_int

    while pos < len_list - 1:
        pos, format_len = next_bin_int(pos)
        num_words = int(format_len[1:58], 2)
        if num_words == 0:
            pos, b = next_bin_int(pos)
            b_len = int(format_len[58:], 2) + 1
            if b_len == 64:
                n = int(b, 2)
            else:
                n = int(b[1:1+b_len], 2)
            int_list.append(n)
        else:
            len_last_block = int(format_len[58:], 2)
            next_bin = ''
            for j in range(num_words):
                pos, b = next_bin_int(pos)
                next_bin += b[1:]
            if len_last_block > 0:
                pos, b = next_bin_int(pos)
                last_bin = b[1:1+len_last_block]
                next_bin += last_bin
            int_list.append(int(next_bin, 2))
    return int_list


# Add padding information of a bin_str value
# do a left padding
# input :
#   bin_str = bin_str
#   size = int
def pad_bin(bin_str, size):
    length = len(bin_str)
    if length < size:
        bin_str = '0' * (size - length) + bin_str
    return bin_str


# Do a right rotation of a bin_str value
# input :
#   bin_str = list of string
#   rot = int
# output = int
def rotate_right(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[(array_len - rot):array_len] + bin_str[0:(array_len - rot)]
    return int(rot_array, 2)


# Do a left rotation of a bin_str value
# input :
#   bin_str = list of string
#   rot = int
# output = int
def rotate_left(bin_str, rot):
    array_len = len(bin_str)
    rot_array = bin_str[rot:array_len] + bin_str[0:rot]
    return int(rot_array, 2)
