import os
from random import getrandbits


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


# print key len and hexa key to the user
# key_len = int
# key = str
def print_key(key_len, key):
    print("Voici votre clé symétrique sur ", key_len, "bits :",
          "\t\n######################################\t\n",
          key,
          "\t\n######################################")


# function that read the key in a file
# fichier = str
# data = str
def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data


def read_tab_keys():
    with open("../data/pass.txr", 'r') as kfile:
        data = kfile.readlines()
        return data


# Takes a bytearray as input and write it in a file
# data =
def write_tab_keys(data):
    with open("../../data/pass.txt", 'w') as kfile:
        kfile.writelines(data)


# function that read a file with binary method and can do padding if the last word
# does not match wih the blck length
# fichier = str
# bloc_len = int (256, 512 or 1024)
# has_padding = boolean
# datalist = list
def readfile(fichier, bloc_len, has_padding):
    # file length information
    taille_fich = os.stat(fichier).st_size
    # conversion of L_block in byte
    bloc_bytes_len = int(bloc_len / 8)
    # nbr of blocks without padding
    n_bloc_nopad = int(taille_fich / bloc_bytes_len)
    # length of last block
    last_bloc_len = taille_fich - bloc_bytes_len * n_bloc_nopad
    # last_bloc is where the last block start
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
        # last list
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


# function that organised a list into a tab of list of L_block / 64
# data_list = list
# word_len = int (256,512 or 1024)
# datalistorder = tab of list
def organize_data_list(data_list, word_len):
    # permet de mettre les données dans un tableau de list de n mots de 64bits
    datalistorder = []
    for i in range(0, len(data_list), word_len):
        datalistorder.append(data_list[i:(i + word_len)])
    return datalistorder


# function that add padding data if the tab of list last list length is not enought
# datalistorder = tab of list
# ciph_bloc_len = int (256,512 or 1024)
# len_bloc = int
# datalistorder = tab of list
def ajout_padding(datalistorder, ciph_bloc_len, len_bloc):
    len_bloc_bytes = int(len_bloc / 8)
    last_list = datalistorder[len(datalistorder) - 1]
    # if the last list length match with (4, 8 or 16) then do padding
    if len(last_list) == int(ciph_bloc_len / 64):
        # a list of N(4, 8, 16) - 1 random int is add
        new_last_list = []
        for i in range(0, int(ciph_bloc_len / 64) - 1):
            new_last_list.append(getrandbits(len_bloc))
        pad_info = getrandbits(len_bloc - 8)
        nbr_pad = int(ciph_bloc_len / 64)
        # convertion en byte du randint de 56 bits
        pad_info = pad_info.to_bytes(len_bloc_bytes - 1, byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        # info add in new list
        new_last_list.append(pad_info)
        # add new list in datalistorder
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


# function that remove padding information in a list
# data = tab of list
# ciph_bloc_len = int (256, 512 or 1024)
# len_bloc = int
# data = tab of list
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


# function that remove padding of an int in a list
# data = tab of list
# bloc_len = int (256, 512 or 1024)
# data = tab of list
# pad_len = int
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
