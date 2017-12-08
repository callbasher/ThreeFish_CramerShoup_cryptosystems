#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd

from random import randrange, getrandbits, sample
import sys
import os
import struct
import binascii

def pgcd(a, b):
    # calcul recursif du pgcd de a et b
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def powermod(a, exp, mod):
    resultat = 1
    while exp > 0:
        if exp % 2 == 1:
            resultat = (resultat * a) % mod
        exp >>= 1
        a = (a * a) % mod
    return resultat

# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_miller(n, b = 7):
   if n < 6:
      return [False, False, True, True, False, True][n]
   elif n & 1 == 0:
      return False
   else:
      s, p = 0, n - 1
      while p & 1 == 0:
         s, p = s + 1, p >> 1
      for i in sample(range(2, min(n - 2, sys.maxsize)), min(n - 4, b)):
         c = pow(i, p, n)
         if c != 1 and c + 1 != n:
            for r in range(1, s):
               c = pow(c, 2, n)
               if c == 1:
                  return False
               elif c == n - 1:
                  i = 0
                  break
            if i:
               return False
      return True

# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_millerv2(n, t = 7):
    isPrime = True
    if n < 6:
        return [not isPrime, not isPrime, isPrime, isPrime, not isPrime, isPrime][n]
    elif not n & 1:
        return not isPrime

    def check(a, s, r, n):
        x = pow(a, r, n)
        if x == 1:
            return isPrime
        for i in range(s-1):
            if x == n - 1:
                return isPrime
            x = pow(x, 2, n)
        return x == n-1

    # Find s and r such as n - 1 = 2^s * r
    s, r = 0, n - 1
    while r & 1:
        s = s + 1
        r = r >> 1

    for i in range(t):
        a = randrange(2, n-1)
        if not check(a, s, r, n):
            return not isPrime

    return isPrime

# Début lecture fichier a chiffrer
# but de la fonction est de lire L_Block du fichier et de les chiffrer puis d'écrire dans un nouveau fichier


def readfile(fichier, L_block):                  # C:/Users/aurélien/Google Drive/DGSE.txt
    pad = "0"
    stat = os.stat(fichier)
    tailleFich = stat.st_size           # taille du fichier en octets
    print("taille fichier : ", tailleFich)  # affichage de la taille du fichier

    L_block_bytes = int(L_block / 8)         # conversion de L_block en octets
    print("taille du block en octets : ", L_block_bytes)

    for i in range(0, tailleFich, L_block_bytes):
        with open(fichier, 'rb') as rfile:  # ouverture du fichier
            rfile.seek(i)  # début lecture de fichier au début
            data = bytearray(rfile.read(L_block_bytes))  # L_block bits de data stocké dans la var data

            if len(data) != L_block_bytes:                  # Condition pour le dernier block, réalisation de padding right !!!
                print("do padding !!!!")
                data = data.ljust(L_block_bytes, b'0')         # rjust pour right padding

            print("longueur données : ", len(data), "octets, donnée = ", data)     # affichage de la longueur des données

            conversion = list(data)             # conversion du bytearray en list ou chaque éléments est représenté par 2 octets
            print(conversion)

    return data

# Fin lecture fichier a chiffrer