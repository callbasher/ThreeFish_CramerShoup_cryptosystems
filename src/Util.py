#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random

def bezout(a, b):
    (r, u, v, r1, u1, v1) = (a, 1, 0, b, 0, 1)
    while r1 != 0:
        q = int(r / r1)
        (r, u, v, r1, u1, v1) = (r1, u1, v1, r - q * r1, u - q * u1, v - q * v1)
    return r, u, v

def inv(a, mod):
    (r, u, v) = bezout(a, mod)
    return u % mod

# function that calculate the PGCD between 2 int
# input0 = int
# input1 = int
# ouput = int
def pgcd(a, b):
    # recursive calcul of a and b PGCD
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)

# function that factorize an int
# input = int
# output = list of int
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

# Rabin-Miller primality test, use in big prime number generation
# input0 = int
# input1 = int
# ouput = boolean (true or false)
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

# function that convert an int value into a hexa
# input = int
# output = hexa
def int2hexa(n):
    hexk = hex(n)
    hexk = hexk.replace('\'', '')
    hexk = hexk.replace('0x', '', 1)
    hexk = str(hexk)
    return hexk

# function that convert a 64 bits int value into a list of str
# intput = int
# output = list of str
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

# function that convert a str value into an int value
# input = str
# output = int
def strToInt(to_convert):
    return (int(to_convert, 2))

# function that xor 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def xor_function(Barray0, Barray1):
    result = str(bin(int(Barray0, 2) ^ int(Barray1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

# function that add 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def additionMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) + int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result

# function that substract 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def soustracMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) - int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

# function that convert a list of str into an 64bits int
# input = list of str
# output = int
def bytearrayToInt(to_convert):
    convert = "".join(to_convert)
    convert = int(convert, 2)
    return convert

# function that modular add 2 lists
# input0 = tab of list
# input1 = tab of list
# output = tab of list
def addition_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output

# function that modular substract 2 lists
# input0 = tab of list
# input1 = tab of list
# output = tab of list
def soustraction_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i]) % 2 ** 64
        output.append(result)
    return output

# function that xor 2 lists
# input0 = list
# input1 = list
# output = list
def xor_2_lists(list1, list2):
    output = []
    for i in range(0, len(list1)):
        result = list1[i] ^ list2[i]
        output.append(result)
    return output
