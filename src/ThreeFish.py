#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
from src.Util import *
from src.IO import *

# Constants
# R bits shift
R = 49
# first tweak on 64 bits (cogranne)
tweak0 = 99111103114097110110101
# second tweak on 64 bits (gs15love)
tweak1 = 103115049053108111118101
tweak2 = tweak0 ^ tweak1
tweaks = [tweak0, tweak1, tweak2]
# 0x1bd11bdaa9fc1a22 in hexa C = constant for key generation
C = 513129967392069919254

# function that is apply when the user chose the option 1 in the menu
def threefish_chiffrement():
    bloc = 64
    print("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC")
    ModeChif = int(input("Option :"))
    while ModeChif != 1 and ModeChif != 2:
        ModeChif = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))

    bloc_len = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))
    while (bloc_len != 256) and (bloc_len != 512) and (bloc_len != 1024):
        bloc_len = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))

    fichier = input("Veuillez entrer le chemin d'un fichier qui va être chiffré : ")
    lect_fichier = readfile(fichier, bloc, 1)
    lect_fichier = organize_data_list(lect_fichier, bloc_len)

    key, keyuser = keygen(bloc_len)
    tabKey = keygenturn(key)
    print("Voici votre clé symétrique sur ",
          bloc_len,
          " bits : \t\n######################################\t\n",
          keyuser,
          "\t\n######################################")
    # Todo : écrire la key user dans un fichier texte dans le même répertoire que le fichier qui va être chiffré

    padding_fichier = ajout_padding(lect_fichier, bloc_len, bloc)

    if ModeChif == 1:
        chiff = ECB_threefish_cipher(padding_fichier, tabKey)
    else:
        chiff = CBC_threefish_cipher(padding_fichier, tabKey, bloc_len)

    writefilelist(fichier, chiff)
    rename_file(fichier, 0)

    print("Félicitation !! Chiffrement terminé.")

# function tha is apply when the user chose the option 2 in the menu
def threefish_dechiffrement():
    bloc = 64
    print("Veuillez choisir votre mode de déchiffrement : \n\t1. ECB\n\t2. CBC")
    ModeChif = int(input("Option :"))
    while ModeChif != 1 and ModeChif != 2:
        ModeChif = int(input("Veuillez choisir votre mode de déchiffrement : \n\t1. ECB\n\t2. CBC"))

    bloc_len = int(input("Choisir la taille de bloc à utiliser pour le déchiffrement (256/512/1024) : "))
    while (bloc_len != 256) and (bloc_len != 512) and (bloc_len != 1024):
        bloc_len = int(input("Choisir la taille de bloc à utiliser pour le déchiffrement (256/512/1024) : "))

    fichier = input("Veuillez entrer le chemin d'un fichier qui va être déchiffré : ")
    rename_file(fichier, 1)
    lect_fichier = readfile(fichier, bloc, 0)
    lect_fichier = organize_data_list(lect_fichier, bloc_len)

    # todo : faire une fonction qui va lire la clé sym et généré des clés avec keygenturn
    key = "ToDo"
    tabKey = keygenturn(key)

    if ModeChif == 1:
        dchiff = ECB_threefish_decipher(lect_fichier, tabKey)
    else:
        dchiff = CBC_threefish_decipher(lect_fichier, tabKey, bloc_len)

    no_padding_list = remove_padding_list(dchiff, bloc_len, bloc)
    no_padding_data, valeur_pad = remove_padding_data(no_padding_list, bloc)

    write_file_list_pad(fichier, no_padding_data, valeur_pad)

    print("Félicitation !! Déchiffrement terminé.")


# function that generate a random key
# input = int that is 256, 512 or 1024
# output0 = list of int (key)
# output1 = str (keyuser)
def keygen(L_block):
    key = []
    hexkey = []
    k = 0
    for i in range(0, int(L_block/64) - 1):
        n = getrandbits(64)
        key.append(n)
        k ^= n
        hexk = int2hexa(n)
        if len(hexk) != 16:
            pad = "0"
            hexk = (16 - (len(str(hexk)))) * pad + str(hexk)
            hexkey.append(hexk)
        else:
            hexkey.append(hexk)
        # keyuser is the hexa key that we gonna give to the user
        keyuser = ""
        for i in hexkey:
            keyuser += i
    k ^= C
    key.append(k)
    return key, keyuser

# function that generate 20 keys based on the random key generate with the function keygen
# input = list of int
# output = tab of list of int
def keygenturn(key):
    N = len(key) - 1
    VingtKeys = []
    k = 0
    for i in range(0, 20):
       tabKey = []
       for n in range(0, (N - 3)):
          t = key[(i + n) % (N + 1)]
          tabKey.append(t)
          k ^= t
       # N - 3
       n = N - 3
       t = (key[(i + n) % (N + 1)]) + (tweaks[i % 3])
       # We want t % 2^64
       # We truncate the hexadecimal characters over the range of 2^64
       tHex = hex(t)
       tStr = str(tHex)
       tStr = tStr[len(tStr)-16:len(tStr)]
       t = int(tStr, 16)
       # it calculate the modulo witout doing the 2^64 operation
       tabKey.append(t)
       k ^= t
       # N - 2
       n = N - 2
       t = (key[(i + n) % (N + 1)]) + (tweaks[(i + 1) % 3]) % (2**64)
       tabKey.append(t)
       k ^= t
       # N - 1
       n = N - 1
       t = (key[(i + n) % (N + 1)]) + i % (2**64)
       tabKey.append(t)
       k ^= t
       k ^= C
       # k is the last word of 64 bits kn = k0+..+kn-1+C
       tabKey.append(k)
       VingtKeys.append(tabKey)
    return VingtKeys

# function that mix data
# input = list of int
# output = list of int
def mixcolumn(datalist):
    # according to the block length we do 2, 4 or 8 times the mix
    datalistmix = []
    for i in range(0, len(datalist) - 1, 2):
        m11 = additionMod(intToByteArray(datalist[i]), intToByteArray(datalist[i + 1]))
        m11 = strToInt(m11)

        Rotation = ROTD(intToByteArray(datalist[(i + 1)]))

        m22 = xor_function(intToByteArray(m11), intToByteArray(Rotation))
        m22 = strToInt(m22)
        datalistmix.append(m11)
        datalistmix.append(m22)
    return datalistmix

# function that unmix data
# intput = list of int
# output = list of int
def inv_mixcolumn(datalist):
    # according to the block lenght we do 2, 4 or 8 times the mix
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        varXor = xor_function(intToByteArray(datalist[i]), intToByteArray(datalist[(i + 1)]))
        m2 = ROTG(varXor)
        m1 = soustracMod(intToByteArray(datalist[i]), intToByteArray(m2))
        m1 = strToInt(m1)
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix

# function that permute data
# intput = list of int
# output = list of int
def permute(n):
    return list(reversed(n))

# function that do ECB threefish encryption
# intput = tab of list of int
# output = tab of list of int
def ECB_threefish_cipher(datalist, tabkeys):
    encryp_list = []
    for j in datalist:
        for k in range(0, 19):
            j = addition_modulaire_listes(j, tabkeys[k])
            for i in range(4):
                j = mixcolumn(j)
                j = permute(j)
        j = addition_modulaire_listes(j, tabkeys[19])
        encryp_list.append(j)
    return encryp_list

# function that do ECB threefish decipherment
# intput = tab of list of int
# output = tab of list of int
def ECB_threefish_decipher(datalist, tabkeys):
    decrypt_list = []
    for j in datalist:
        counter = 18
        j = soustraction_modulaire_listes(j, tabkeys[19])
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = soustraction_modulaire_listes(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    return decrypt_list

# function that do CBC threefish encryption
# intput = tab of list of int
# output = tab of list of int
def CBC_threefish_cipher(datalist, tabkeys, L_bloc):
    iv = IV_function(L_bloc)
    encryp_list = []
    datalist[0] = addition_modulaire_listes(datalist[0], iv)
    var_count = 1
    anterior_occurence_counter = 0
    for j in datalist:
        if var_count == 0:
            # modular addition with the current occurence and the cipher occurence before
            j = addition_modulaire_listes(j, encryp_list[anterior_occurence_counter])
            anterior_occurence_counter += 1
            for k in range(0, 19):
                j = addition_modulaire_listes(j, tabkeys[k])
                for i in range(4):
                    j = mixcolumn(j)
                    j = permute(j)
        else:
            for k in range(0, 19):
                j = addition_modulaire_listes(j, tabkeys[k])
                for i in range(4):
                    j = mixcolumn(j)
                    j = permute(j)
        j = addition_modulaire_listes(j, tabkeys[19])
        encryp_list.append(j)
        var_count = 0
    return encryp_list

# function that do CBC threefish decipherment
# intput = tab of list of int
# output = tab of list of int
def CBC_threefish_decipher(datalist, tabkeys, L_bloc):
    iv = IV_function(L_bloc)
    decrypt_list = []
    for j in datalist:
        j = soustraction_modulaire_listes(j, tabkeys[19])
        counter = 18
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = soustraction_modulaire_listes(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    # modular substract with the cipher occurence before and the decipher occurence
    for i in range(1, len(decrypt_list)):
        decrypt_list[i] = soustraction_modulaire_listes(decrypt_list[i], datalist[i - 1])
    # xor between the iv and the first occurence
    decrypt_list[0] = soustraction_modulaire_listes(decrypt_list[0], iv)
    return decrypt_list

# function that do a right rotation
# input = list of string
# output = int
def ROTD(Barray):
    longBarray = len(Barray)
    ROTDBarray = Barray[(longBarray - R):longBarray] + Barray[0:(longBarray - R)]
    ROTDBarray = strToInt(ROTDBarray)
    return ROTDBarray

# function that do a left rotation
# input = list of string
# output = int
def ROTG(Barray):
    longBarray = len(Barray)
    ROTGBarray = Barray[R:longBarray] + Barray[0:R]
    ROTGBarray = strToInt(ROTGBarray)
    return ROTGBarray

# function that return an IV based on the length of the block
# input = int (256, 512 or 1024)
# output = list of int
def IV_function(L_bloc):
    IV_256 = [11939804896947846136, 4219065746052997657, 14289511192216538576, 6129295191351922843]
    IV_512 = [14021392340165679391, 10713825714517858312, 16678454614520143940, 2176821685655837471,
              993364598582970774, 17432205245676079126, 15273195067266655935, 17670466041850028273]
    IV_1024 = [15345143141016669355, 13465911367260466770, 5383010510772685731, 10149785470626774238,
               616504849952386683, 9934305711475078234, 7510955176798512515, 10974823043510880208,
               10506771315442257531, 2703887491885455230, 506214325955753681, 7244289412050330942,
               15552188946686260547, 3934227692526149925, 8351231218515392481, 12278345771412770886]

    if L_bloc == 256:
        return IV_256
    elif L_bloc == 512:
        return IV_512
    elif L_bloc == 1024:
        return IV_1024
