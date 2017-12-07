#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random

# Constantes

R = 49 # Décalage de R bits

tweak0 = 99111103114097110110101  # premier tweak sur 64 bits (cogranne)

tweak1 = 103115049053108111118101   # second tweak sur 64 bits (gs15love)

tweak2 = tweak0 ^ tweak1

tweaks = [tweak0, tweak1, tweak2]

C = 513129967392069919254   # soit 0x1bd11bdaa9fc1a22 en hexa  # C = constante pour la génération des clés des tournées

# Création / génération de la clé symétrique

def keygen(L_block):
    key = []
    hexkey = []
    k = 0
    for i in range(0, int(L_block/64)):
        n = random.getrandbits(64)              # génération d'un int de 64bits
        key.append(n)
        k ^= n                                  # xor des int généré

        hexk = hex(n)                           # convertion de l'int généré en hexa
        hexk = hexk.replace('\'', '')           # supression des '
        hexk = hexk.replace('0x', '', 1)        # suppression des caractères 0x au début du mot
        hexk = str(hexk)

        if len(hexk) != 16:
            pad = "0"                           # padding pour que le nombre convertis en hex soit sur 16bits
            hexk = (16 - (len(str(hexk)))) * pad + str(hexk)
            hexkey.append(hexk)
        else:
            hexkey.append(hexk)

        keyuser = ""     # keyuser est la clé symétrique que l'on va afficher à l'utilisateur
        for i in hexkey:    # pour qu'il la note et s'ne serve pour le déchiffrement
            keyuser += i

    k ^= C          # xor de toutes les cles avec C puis ajout du résultat dans la clé
    key.append(k)
    print(len(str(keyuser)))
    print("Voici votre clé symétrique sur ", L_block, " bits : \t\n######################################\t\n"
          , keyuser, "\t\n######################################")
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
       tabKey.append(k)                                     # k est le dernier mot de 64 bits kn = k0+..+kn-1+C

       VingtKeys.append(tabKey)
    return VingtKeys         # var VingKeys est la var ou se trouve les 20 cles des tournées

# Fin génération des clés