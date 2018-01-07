#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


# Rename a file after it was been cipher or before it will be decipher
# basically rename a file with ".encrypt" extension when it is a cipher text
# or remove ".encrypt" extension if the file is decipher
# input :
#   path_fichier = str
#   option_remove_encrypt_extension = boolean
def rename_file(path_fichier, option_remove_encrypt_extension):
    rep = path_fichier.split("/")
    fichier = rep[len(rep) - 1]
    if option_remove_encrypt_extension == 0:
        enc = ".encrypt"
        fichier = fichier + enc
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    else:
        fichier = fichier[:(len(fichier) - 8)]
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    os.rename(path_fichier, new_fichier)


# Read a file with binary method and can do padding if the last word
# does not match wih the bloc length
# convert the binary into int value
# input :
#   fichier = str
#   bloc_len = int (256, 512 or 1024)
#   has_padding = boolean
# output :
#   datalist = list
def readfile(file, word_len, has_padding):
    file_size = os.stat(file).st_size
    word_len_bytes = int(word_len / 8)
    n_bloc_nopad = int(file_size / word_len_bytes)
    last_word_len = file_size - word_len_bytes * n_bloc_nopad
    last_bloc_pos = int(word_len_bytes * n_bloc_nopad)
    datalist = []

    for i in range(0, (file_size - last_word_len), word_len_bytes):
        with open(file, 'rb') as rfile:
            rfile.seek(i)
            data = rfile.read(word_len_bytes)
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)

    # do padding if the file length / L_block_bytes != int
    if last_word_len != 0:
        with open(file, 'rb') as rfile:
            rfile.seek(last_bloc_pos)
            data = rfile.read(last_word_len)
            nbr_byte_pad = word_len_bytes - len(data)
            # add padding data in byte in the end of the block to inform how much padding byte has been add
            data = (nbr_byte_pad - 1) * b'0' + data + bytes([nbr_byte_pad])
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)
    elif has_padding == 1:
        pad_last_byte = bytes([word_len_bytes])
        data_pad = b'0' * (word_len_bytes - 1) + pad_last_byte
        data_pad = int.from_bytes(data_pad, byteorder='little', signed=False)
        datalist.append(data_pad)
    return datalist


def read_bytes(file):
    with open(file, "rb") as rfile:
        data = rfile.read()
    return data


# Write str data in a file
# input :
#   fichier = str
#   data = str
def write_bytes(filepath, data):
    with open(filepath, 'wb') as wfile:
        wfile.write(data)


# Write a 2D array of int data into a file
# the int data are convert into binary data and write them in the file
# input :
#   fichier = str
#   data = tab of list
#   bloc_byte_len = int
def write_list(filepath, data, bloc_byte_len):
    with open(filepath, 'wb') as wfile:
        for i in data:
            b = i.to_bytes(bloc_byte_len, byteorder='little', signed=False)
            wfile.write(b)


# Write a 2D array of int data into a file
# the int data are convert into binary data and write them in the file
# input :
#   fichier = str
#   data = tab of list
#   bloc_byte_len = int
def write_2D_list(fichier, data, bloc_byte_len):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(bloc_byte_len, byteorder='little', signed=False)
                wfile.write(j)


# Write the 2D array of int data into a file and remove the padding of the last int
# input :
#   fichier = str
#   data = tab of list
#   bloc_byte_len = int
#   val_last_data = list
def write_file_list_pad(fichier, data, bloc_byte_len, val_last_data):
    with open(fichier, 'wb') as wfile:
        # write all the data except the last list in the tab, because there is padding
        for i in range(0, len(data) - 1):
            for j in data[i]:
                j = j.to_bytes(bloc_byte_len, byteorder='little', signed=False)
                wfile.write(j)
        last_list = data[len(data) - 1]
        # write all except the last int of 64bits (int where the padding is)
        for i in range(0, len(last_list) - 1):
            wdata = last_list[i].to_bytes(bloc_byte_len, byteorder='little', signed=False)
            wfile.write(wdata)
        if val_last_data == bloc_byte_len:
            wdata = last_list[len(last_list) - 1].to_bytes(bloc_byte_len, byteorder='little', signed=False)
            wfile.write(wdata)
        else:
            wdata = last_list[len(last_list) - 1].to_bytes((bloc_byte_len - val_last_data),
                                                           byteorder='little', signed=False)
            wfile.write(wdata)
