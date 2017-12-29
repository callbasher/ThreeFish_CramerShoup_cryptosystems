import os
from random import getrandbits


def rename_fichier(path_fichier, option):
    rep = path_fichier.split("/")
    fichier = rep[len(rep) - 1]
    if option == 0:
        enc = ".encrypt"
        fichier = fichier + enc
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    else:
        fichier = fichier[:(len(fichier) - 8)]
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    os.rename(path_fichier, new_fichier)


def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data


# Début lecture fichier a chiffrer
# but de la fonction est de lire L_Block du fichier et de les chiffrer puis d'écrire dans un nouveau fichier
def readfile(fichier, L_block, do_padding):
    # information sur la taille du fichier
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    # conversion de L_block en octets
    L_block_bytes = int(L_block / 8)
    # nbr de blocks sans padding
    nbr_block_nopad = int(tailleFich / L_block_bytes)
    # taille du dernier block
    last_bloc_length = tailleFich - L_block_bytes * nbr_block_nopad
    # last_bloc détermine l'endroit ou commence le dernier bloc
    last_bloc =  int(L_block_bytes * nbr_block_nopad)
    # list avec la valeur des int du fichier
    datalist = []

    for i in range(0, (tailleFich - last_bloc_length), L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            # L_block bits de data stocké dans la var data
            data = rfile.read(L_block_bytes)
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)

    # ajout de padding si tailleFich / L_block_bytes != entier sinon pas besoin de padding
    if last_bloc_length != 0:
        with open(fichier, 'rb') as rfile:
            rfile.seek(last_bloc)
            data = rfile.read(last_bloc_length)
            # méthode d'ajout de padding
            nbr_byte_pad = L_block_bytes - len(data)
            # ajout d'un dernier octet sur la fin pour préciser combien il y a d'octets de padding
            data = (nbr_byte_pad - 1) * b'0' + data + bytes([nbr_byte_pad])
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)
    else:
        if do_padding == 1:
            pad_last_byte = bytes([L_block_bytes])
            data_pad = b'0' * (L_block_bytes - 1) + pad_last_byte
            data_pad = int.from_bytes(data_pad, byteorder='little', signed=False)
            datalist.append(data_pad)
    return datalist


# Takes a bytearray as input and write it in a file
def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)


def writefilelist(fichier, data):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)


def write_file_list_pad(fichier, data, val_last_data):
    with open(fichier, 'wb') as wfile:
        # ecriture de tout sauf de la dernière liste de data, celle qui contient la valeur sans padding
        for i in range(0, len(data) - 1):
            for j in data[i]:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)
        # dernière liste
        last_list = data[len(data) - 1]
        # écriture de tout sauf du dernier mot
        for i in range(0, len(last_list) - 1):
            wdata = last_list[i].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        if val_last_data == 8:
            wdata = last_list[len(last_list) - 1].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        else:
            wdata = last_list[len(last_list) - 1].to_bytes((8 - val_last_data), byteorder='little', signed=False)
            wfile.write(wdata)

def organize_data_list(data_list, L_bloc):
    # permet de mettre les données dans un tableau de list de n mots de 64bits
    l = int(L_bloc / 64)
    datalistorder = []
    for i in range(0, len(data_list), l):
        datalistorder.append(data_list[i:(i + l)])
    return datalistorder


def ajout_padding(datalistorder, Length_chif_bloc):
    last_list = datalistorder[len(datalistorder) - 1]
    # si la dernière liste ne fais pas la bonne taille N(4, 8 ou 16) alors do padding
    if len(last_list) == int(Length_chif_bloc / 64):
        # ajout d'une liste de N(4, 8, 16) - 1 mot random de 64bits
        new_last_list = []
        for i in range(0, int(Length_chif_bloc / 64) - 1):
            new_last_list.append(getrandbits(64))
        pad_info = getrandbits(56)
        # Si 4, 8 ou 16 mots on été ajoutés
        nbr_pad = int(Length_chif_bloc / 64)
        # convertion en byte du randint de 56 bits
        pad_info = pad_info.to_bytes(7, byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        # ajout de l'info dans la new list
        new_last_list.append(pad_info)
        # ajout de la new list dans le datalistorder
        datalistorder.append(new_last_list)
    else:
        # S'il ne faut ajouter q'un seul mot d'information a la dernière liste
        if len(last_list) + 1 == int(Length_chif_bloc / 64):
            nbr_rand = getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([1])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            # ajout du mot dans la dernière list
            last_list.append(pad_info)
        else:
            lenght_last_list = int(Length_chif_bloc / 64) - len(last_list)
            for i in range(0, (int(Length_chif_bloc / 64) - len(last_list)) - 1):
                last_list.append(getrandbits(64))
            nbr_rand = getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([lenght_last_list])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            last_list.append(pad_info)
    return datalistorder


def remove_padding_list(data, Length_chif_bloc):
    # dernière liste du tableau
    data_pad_list = data[len(data) - 1]
    # dernier élément de la dernière liste du tableau
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # conversion du last element en byte
    data_pad = data_pad.to_bytes(8, byteorder='little', signed=False)
    # valeur du pading
    data_pad_nbr = int(data_pad[7])
    # Si le padding est la dernière liste complète alors on la supprime
    if data_pad_nbr == int(Length_chif_bloc / 64):
        del data[len(data) - 1]
    else:
        data_pad = data_pad_list[:len(data_pad_list) - data_pad_nbr]
        del data[len(data) - 1]
        data.append(data_pad)
    return data


def remove_padding_data(data, L_bloc):
    L_bloc_byte = int(L_bloc / 8)
    # dernière liste du tableau
    data_pad_list = data[len(data) - 1]
    # dernier élément de la dernière liste du tableau
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # conversion du last element en byte
    data_pad = data_pad.to_bytes(L_bloc_byte, byteorder='little', signed=False)
    # valeur du pading
    data_pad_nbr = int(data_pad[7])
    if data_pad_nbr == L_bloc_byte:
        # suppression du dernier élément de la dernière liste
        del data_pad_list[len(data_pad_list) - 1]
    else:
        # remove padding
        data_pad_remove = data_pad[(data_pad_nbr - 1):(L_bloc_byte - 1)]
        # convertion de la nouvelle data en int
        new_data = int.from_bytes(data_pad_remove, byteorder='little', signed=False)
        # suppression du dernier élément de la dernière liste
        del data_pad_list[len(data_pad_list) - 1]
        # insertion du dernier élément de la dernière liste
        data_pad_list.append(new_data)
    return data, data_pad_nbr
