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
    print("Voici votre clé symétrique sur ", L_block, " bits : \t\n######################################\t\n"
          , keyuser, "\t\n######################################")
    # écriture de la clé symétrique dans un fichier
    writefile("../test/resources/symKey.txt", keyuser)
    return key
# Fin création / génération de la clé symétrique

# Génération des 20 clés pour les tournées
def keygenturn(key):
    N = len(key) - 1
    VingtKeys = []
    k = 0
    for i in range(0, 20):
       tabKey = []
       for n in range(0, (N - 4)):
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
# Fin génération des clés

# début fonction mélange
def mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
    datalistmix = []
    # convertion en bytearray
    Barray = []
    for i in datalist:
        Barray.append(intToByteArray(i))

    for i in range(0, len(datalist) - 1, 2):
        m11 = (datalist[i] + datalist[i+1]) % 2**64
        m22 = m11 ^ (datalist[i + 1] << R)
        datalistmix.append(m11)
        datalistmix.append(m22)
    return datalistmix
# Fin de la fonction mélange

# début de la fonction inverse de mélange
def inv_mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        m2 = (datalist[i] ^ datalist[i + 1]) >> R
        m1 = (datalist[i] - m2) % 2**64
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix
# Fin de la fonction inverse de mélange

# début fonction de permutation
def permute(n):
    # invertion de l'ordre des mots
    return list(reversed(n))
# fin fonction de permutation

# début fonction xor de la clé et du block qui est en train d'être chiffré
def ajoutkey(i_block, i_tabkey):
    datalistajoutkey = []
    for i in range(0, len(i_block)):
        datalistajoutkey.append((i_block[i] + i_tabkey[i]) % 2**64)
    return datalistajoutkey
# fin fonction xor de la clé et du block qui est en train d'être chiffré

# début fonction inverse ajoutkey
def inv_ajoutkey(i_block, i_tabkey):
    datalistinv_ajoutkey = []
    for i in range(0, len(i_block)):
        datalistinv_ajoutkey.append((i_block[i] - i_tabkey[i]) % 2 ** 64)
    return datalistinv_ajoutkey
# fin fonction inverse ajoutkey

# chiffrement ECB début
def ECBchiffThreef(datalist, tabkeys):
    encryptdatalist = []
    for j in datalist:
        j = mixcolumn(j)
        j = permute(j)
        encryptdatalist.append(j)
    return encryptdatalist
# chiffrement ECB fin

# déchiffrement ECB début
def ECBdechiffThreef(datalist, tabkeys):
    decryptdatalist = []
    for j in datalist:
        j = permute(j)
        j = inv_mixcolumn(j)
        decryptdatalist.append(j)
    return decryptdatalist
# déchiffrement ECB fin

# fonction rotation circulaire droite d'une chaine de 64bits
def ROTD(Barray):
    Barray = str(Barray)
    # la longueur de Barray dois être de 64
    longBarray = len(Barray)
    ROTDBarray = Barray[(longBarray - R):longBarray] + Barray[0:(longBarray - R)]
    return ROTDBarray

# rotation circulaire gauche d'une chaine de 64bits
def ROTG(Barray):
    Barray = str(Barray)
    # la longueur de Barray dois être de 64
    longBarray = len(Barray)
    ROTGBarray = Barray[R:longBarray] + Barray[0:R]
    return ROTGBarray