#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import itertools
from src.Util import *

# Constantes
# Décalage de R bits
R = 49
# premier tweak sur 64 bits (cogranne)
tweak0 = 99111103114097110110101
# second tweak sur 64 bits (gs15love)
tweak1 = 103115049053108111118101
tweak2 = tweak0 ^ tweak1
tweaks = [tweak0, tweak1, tweak2]
# soit 0x1bd11bdaa9fc1a22 en hexa C = constante pour la génération des clés des tournées
C = 513129967392069919254
# Création / génération de la clé symétrique
def keygen(L_block):
    key = []
    hexkey = []
    k = 0
    for i in range(0, int(L_block/64) - 1):
        n = random.getrandbits(64)
        key.append(n)
        k ^= n
        hexk = int2hexa(n)
        # padding pour que le nombre convertis en hex soit sur 16bits
        if len(hexk) != 16:
            pad = "0"
            hexk = (16 - (len(str(hexk)))) * pad + str(hexk)
            hexkey.append(hexk)
        else:
            hexkey.append(hexk)
        # keyuser est la clé symétrique que l'on va afficher à l'utilisateur
        keyuser = ""
        # pour qu'il la note et s'ne serve pour le déchiffrement
        for i in hexkey:
            keyuser += i
    k ^= C
    key.append(k)
    return key, keyuser

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
       # cela calcul le modulo sans calculer 2^64 même si les puissances de 2 sont optimiser sur les processeur
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
       # k est le dernier mot de 64 bits kn = k0+..+kn-1+C
       tabKey.append(k)
       VingtKeys.append(tabKey)
    return VingtKeys

def mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
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

def inv_mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        varXor = xor_function(intToByteArray(datalist[i]), intToByteArray(datalist[(i + 1)]))
        m2 = ROTG(varXor)
        m1 = soustracMod(intToByteArray(datalist[i]), intToByteArray(m2))
        m1 = strToInt(m1)
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix

def permute(n):
    # invertion de l'ordre des mots
    return list(reversed(n))

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

def CBC_threefish_cipher(datalist, tabkeys, L_bloc):
    iv = IV_function(L_bloc)
    encryp_list = []
    datalist[0] = xor_2_lists(datalist[0], iv)
    var_count = 1
    anterior_occurence_counter = 0
    for j in datalist:
        if var_count == 0:
            j = xor_2_lists(j, encryp_list[anterior_occurence_counter])
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

    for i in range(1, len(decrypt_list)):
        decrypt_list[i] = xor_2_lists(decrypt_list[i], datalist[i - 1])

    decrypt_list[0] = xor_2_lists(decrypt_list[0], iv)

    return decrypt_list

def ROTD(Barray):
    longBarray = len(Barray)
    ROTDBarray = Barray[(longBarray - R):longBarray] + Barray[0:(longBarray - R)]
    ROTDBarray = strToInt(ROTDBarray)
    # return an int value
    return ROTDBarray

def ROTG(Barray):
    longBarray = len(Barray)
    ROTGBarray = Barray[R:longBarray] + Barray[0:R]
    ROTGBarray = strToInt(ROTGBarray)
    # return an int value
    return ROTGBarray

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
