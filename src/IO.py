import os
import random

# function that rename a file
# input0 = str
# input1 = boolean
# output = nothing
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

# function that read the key in a file
# input = str
# output = str
def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data

def read_tab_keys():
    with open("../data/pass.txr", 'r') as kfile:
        data = kfile.readlines()
        return data

# Takes a bytearray as input and write it in a file
def write_tab_keys(data):
    with open("../../data/pass.txt", 'w') as kfile:
        kfile.writelines(data)

# function that read a file with binary method and can do padding if the last word
# does not match wih the blck length
# input0 = str
# input1 = int (256, 512 or 1024)
# input2 = boolean
# output = list
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
    last_bloc_pos =  int(bloc_bytes_len * n_bloc_nopad)
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
# input0 = str
# input1 = str
def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)

# function that write a tab of list data into a file
# input0 = str
# input1 = tab of list
def writefilelist(fichier, data):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)

# function that write the tab of list data into a file and remove the padding
# input0 = str
# input1 = tab of list
# input2 = int
def write_file_list_pad(fichier, data, val_last_data):
    with open(fichier, 'wb') as wfile:
        # write all the data except the last list in the tab, because there is padding
        for i in range(0, len(data) - 1):
            for j in data[i]:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)
        # last list
        last_list = data[len(data) - 1]
        # write all except the last int of 64bits (int where the padding is)
        for i in range(0, len(last_list) - 1):
            wdata = last_list[i].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        if val_last_data == 8:
            wdata = last_list[len(last_list) - 1].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        else:
            wdata = last_list[len(last_list) - 1].to_bytes((8 - val_last_data), byteorder='little', signed=False)
            wfile.write(wdata)

# function that organised a list into a tab of list of L_block / 64
# input0 = list
# input1 = int (256,512 or 1024)
# ouput = tab of list
def organize_data_list(data_list, L_bloc):
    l = int(L_bloc / 64)
    datalistorder = []
    for i in range(0, len(data_list), l):
        datalistorder.append(data_list[i:(i + l)])
    return datalistorder

# function that add padding data if the tab of list last list length is not enought
# input0 = tab of list
# input1 = int (256,512 or 1024)
# output = tab of list
def ajout_padding(datalistorder, Length_chif_bloc, len_bloc):
    last_list = datalistorder[len(datalistorder) - 1]
    # if the last list length match with (4, 8 or 16) then do padding
    if len(last_list) == int(Length_chif_bloc / 64):
        # a list of N(4, 8, 16) - 1 random int is add
        new_last_list = []
        for i in range(0, int(Length_chif_bloc / 64) - 1):
            new_last_list.append(random.getrandbits(len_bloc))
        pad_info = random.getrandbits(len_bloc - 8)
        nbr_pad = int(Length_chif_bloc / 64)
        # convertion in byte of the random (N - 8) bits int
        pad_info = pad_info.to_bytes(int((len_bloc - 8) / 8), byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        # info add in new list
        new_last_list.append(pad_info)
        # add new list in datalistorder
        datalistorder.append(new_last_list)
    else:
        # if only one word need to be add in the last list
        if len(last_list) + 1 == int(Length_chif_bloc / 64):
            nbr_rand = random.getrandbits(len_bloc - 8)
            pad_info = nbr_rand.to_bytes(int((len_bloc - 8) / 8), byteorder='little', signed=False)
            pad_info = pad_info + bytes([1])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            # last int add in last list
            last_list.append(pad_info)
        else:
            lenght_last_list = int(Length_chif_bloc / 64) - len(last_list)
            for i in range(0, (int(Length_chif_bloc / 64) - len(last_list)) - 1):
                last_list.append(random.getrandbits(len_bloc))
            nbr_rand = random.getrandbits(len_bloc - 8)
            pad_info = nbr_rand.to_bytes(int((len_bloc - 8) / 8), byteorder='little', signed=False)
            pad_info = pad_info + bytes([lenght_last_list])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            last_list.append(pad_info)
    return datalistorder

# function that remove padding information in a list
# input0 = tab of list
# input1 = int (256, 512 or 1024)
# output = tab of list
def remove_padding_list(data, Length_chif_bloc, len_bloc):
    # last list of the tab
    data_pad_list = data[len(data) - 1]
    # last element of the last list of the tab
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # last element in byte
    data_pad = data_pad.to_bytes(int(len_bloc / 8), byteorder='little', signed=False)
    # value of the pading
    data_pad_nbr = int(data_pad[int((len_bloc - 8) / 8)])
    # if padding est is last list then we delete it
    if data_pad_nbr == int(Length_chif_bloc / 64):
        del data[len(data) - 1]
    else:
        data_pad = data_pad_list[:len(data_pad_list) - data_pad_nbr]
        del data[len(data) - 1]
        data.append(data_pad)
    return data

# function that remove padding of an int in a list
# input0 = tab of list
# input1 = int (256, 512 or 1024)
# output = tab of list
def remove_padding_data(data, bloc_len):
    bloc_byte_len = int(bloc_len / 8)
    # last list of the tab
    data_pad_list = data[len(data) - 1]
    # last element of the last list of the tab
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # last element in byte
    data_pad = data_pad.to_bytes(bloc_byte_len, byteorder='little', signed=False)
    # value of the pading
    data_pad_nbr = int(data_pad[len(data_pad) - 1])
    if data_pad_nbr == bloc_byte_len:
        # last element of the last list deleted
        del data_pad_list[len(data_pad_list) - 1]
    else:
        # remove padding
        data_pad_remove = data_pad[(data_pad_nbr - 1):(bloc_byte_len - 1)]
        # convertion of the new data in int
        new_data = int.from_bytes(data_pad_remove, byteorder='little', signed=False)
        # last element of the last list deleted
        del data_pad_list[len(data_pad_list) - 1]
        data_pad_list.append(new_data)
    return data, data_pad_nbr
