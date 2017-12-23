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

def readfile(fichier, L_block, Lchifblock):
    # information sur la taille du fichier
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    # conversion de L_block en octets
    L_block_bytes = int(L_block / 8)
    # nbr de blocks sans padding
    nbrblocknopad = int(tailleFich / L_block_bytes)
    # taille du dernier block
    lastblock =  int(L_block_bytes * nbrblocknopad)
    # list avec la valeur des int du fichier
    datalist = []

    for i in range(0, (tailleFich - (tailleFich - lastblock)), L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            # L_block bits de data stocké dans la var data
            data = rfile.read(L_block_bytes)
            data = int.from_bytes(data, byteorder='little')
            datalist.append(data)

    # padding
    if lastblock != 0:
        with open(fichier, 'rb') as rfile:
            rfile.seek(L_block_bytes * nbrblocknopad)
            data = rfile.read(tailleFich - lastblock)
            data = data.rjust(L_block_bytes, b'0')
            data = int.from_bytes(data, byteorder='little')
            datalist.append(data)

    # permet de mettre les données dans un tableau de list de n mots de 64bits
    l = int(Lchifblock / 64)
    datalistorder = []
    for i in range(0, len(datalist), l):
        datalistorder.append(datalist[i:(i + l)])

    return datalistorder


def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)

def writefilelist(fichier, data):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(len(str(j)), byteorder='little', signed=False)
                wfile.write(j)

def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data

# fonction de conversion int2bytearray
def intToByteArray(to_convert):
    to_convert = int(to_convert)
    output = []
    result = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, to_convert & mask)
        to_convert >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        result.append(i)
    result = "".join(result)
    result = str(result)
    return result

# fonction de conversion de bytearray2int
def strToInt(to_convert):
    return (int(to_convert, 2))

def xor_function(Barray0, Barray1):
    result = str(bin(int(Barray0, 2) ^ int(Barray1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

def additionMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) + int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result

def soustracMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) - int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result
