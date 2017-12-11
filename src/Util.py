#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd

from random import randrange
import os


def pgcd(a, b):
    # calcul recursif du pgcd de a et b
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def factorize(n):
    factors = []
    i = 2
    while i <= n / i:
        while n % i == 0:
            factors.append(i)
            n /= i
        i += 1

    if n > 1:
        factors.append(n)

    return factors


# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_miller(n, t = 7):
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
def readfile(fichier, L_block):
    pad = "0"
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    print("taille fichier : ", tailleFich)

    # conversion de L_block en octets
    L_block_bytes = int(L_block / 8)
    print("taille du block en octets : ", L_block_bytes)

    for i in range(0, tailleFich, L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            # L_block bits de data stocké dans la var data
            data = bytearray(rfile.read(L_block_bytes))

            # réalisation de padding si necessaire
            if len(data) != L_block_bytes:
                print("do padding !!!!")
                data = data.ljust(L_block_bytes, b'0')

            print("longueur données : ", len(data), "octets, donnée = ", data)

            # conversion du bytearray en list ou chaque éléments est représenté par 2 octets
            conversion = list(data)
            print(conversion)

    return data
