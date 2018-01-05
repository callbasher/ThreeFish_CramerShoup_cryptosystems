#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


# function that rename a file
# path_fichier = str
# option_remove_encrypt_extension = boolean
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


# function that read a file with binary method and can do padding if the last word
# does not match wih the blck length
# fichier = str
# bloc_len = int (256, 512 or 1024)
# has_padding = boolean
# datalist = list
def readfile(fichier, bloc_len, has_padding):
    taille_fich = os.stat(fichier).st_size
    bloc_bytes_len = int(bloc_len / 8)
    n_bloc_nopad = int(taille_fich / bloc_bytes_len)
    last_bloc_len = taille_fich - bloc_bytes_len * n_bloc_nopad
    last_bloc_pos = int(bloc_bytes_len * n_bloc_nopad)
    datalist = []

    for i in range(0, (taille_fich - last_bloc_len), bloc_bytes_len):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            data = rfile.read(bloc_bytes_len)
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)

    # do padding if the file length / L_block_bytes != int
    if last_bloc_len != 0:
        with open(fichier, 'rb') as rfile:
            rfile.seek(last_bloc_pos)
            data = rfile.read(last_bloc_len)
            nbr_byte_pad = bloc_bytes_len - len(data)
            # add padding data in byte in the end of the block to inform how much padding byte has been add
            data = (nbr_byte_pad - 1) * b'0' + data + bytes([nbr_byte_pad])
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)
    elif has_padding == 1:
        pad_last_byte = bytes([bloc_bytes_len])
        data_pad = b'0' * (bloc_bytes_len - 1) + pad_last_byte
        data_pad = int.from_bytes(data_pad, byteorder='little', signed=False)
        datalist.append(data_pad)
    return datalist


# function that write str data in a file
# fichier = str
# data = str
def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)


# function that write a tab of list data into a file
# fichier = str
# data = tab of list
# bloc_byte_len = int
def writefilelist(fichier, data, bloc_byte_len):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(bloc_byte_len, byteorder='little', signed=False)
                wfile.write(j)


# function that write the tab of list data into a file and remove the padding
# fichier = str
# data = tab of list
# bloc_byte_len = int
# val_last_data = list
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
