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

def int2hexa(n):
    hexk = hex(n)
    hexk = hexk.replace('\'', '')
    hexk = hexk.replace('0x', '', 1)
    hexk = str(hexk)
    return hexk

def readfile(fichier, L_block):
    # information sur la taille du fichier
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    # conversion de L_block en octets
    L_block_bytes = int(L_block / 8)
    # nbr de blocks sans padding
    nbrblocknopad = int(tailleFich / L_block_bytes)
<<<<<<< HEAD
    # taille dernier block
=======
    # taille du dernier block
>>>>>>> Threefish
    lastblock = tailleFich - (L_block_bytes * nbrblocknopad)
    # list avec la valeur des int du fichier
    datalist = []

    for i in range(0, tailleFich - lastblock, L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            # L_block bits de data stocké dans la var data
            data = rfile.read(L_block_bytes)
            print(data)
            data = int.from_bytes(data, byteorder='little')
            datalist.append(data)

    # padding
    if lastblock != 0:
        with open(fichier, 'rb') as rfile:
<<<<<<< HEAD
            rfile.seek(nbrblocknopad * L_block_bytes)
=======
            rfile.seek(L_block_bytes * nbrblocknopad)
>>>>>>> Threefish
            data = rfile.read(tailleFich - lastblock)
            data = data.rjust(L_block_bytes, b'0')
            print(data)
            data = int.from_bytes(data, byteorder='little')
            datalist.append(data)

    return datalist


def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)
