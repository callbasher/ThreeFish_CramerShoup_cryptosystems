#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom, randint
from src.Hash import hashInt
from src.Util import *

# The password is hashed to an int.
# This int correspond to the line in which the encrypted keys will be in the password file.
def apply(fichier, k = 512, password = "default"):
    private, public = generateKeys(k)
    pv_ciph = sym_cipher(password, private)
    pb_ciph = sym_cipher(password, public)

    hash = hashInt(password)
    #writefile(fich, data, begin)
    writefile("../data/psw.txt", )

    blockList = readfile(fichier, 64, 64)

    cryptedBytes = []
    for b in blockList:
        cryptedBytes.append(cipher(b))

# The block is supposed to be an int.
# The key is a table containing p, alpha1, alpha2, X, Y, W
def cipher(key, block):
    p, a1, a2, X, Y, W = key[0], key[1], key[2], key[3], key[4], key[5]
    b = randint(0, p)
    B1 = pow(a1, b, p)
    B2 = pow(a2, b, p)
    c = pow(W, b, p) * block
    concat = (B1 + B2 + c) % p
    H = hash(concat)

    v = pow(X, b, p) * pow(Y, b*H, p)

    return B1, B2, c, v

def decode(fichier, password):
    key = retrieveKey(password)

def retrieveKey(password):
    # Read the "password" file containing all te keys
    # Hash the password to get three values : r, c, and seed.
    # Find the keys with r and c
    # decipher the key with ECB and the seed
    # return keys
    return password
def sym_cipher(key, m):
    return key

def find_generator(p, factors):
    b = 1
    while b == 1:
        x = SystemRandom.choice(2, p)
        for f in factors:
            b = pow(x, (p-1) / f, p)
            if b != 1:
                break
    return b

def prime_and_generators(k):
    p, q, r = safe_prime(k)
    # prime factors of p-1
    # we want only the different prime factors not their exponent so we remove duplicates
    # We put q at the end of the list to ensure that smaller factors are tried first
    # in "find_generator" function
    factors = set(factorize(r))
    factors.add(2)
    factors = list(factors)
    factors.append(q)

    alpha1 = find_generator(p, factors)
    alpha2 = alpha1
    while alpha1 == alpha2:
        alpha2 = find_generator(p, factors)

    return p, alpha1, alpha2


def generateKeys(k):
    p, g1, g2 = prime_and_generators(k)

    Zp = range(2, p)
    x1 = SystemRandom.choice(Zp)
    x2 = SystemRandom.choice(Zp)
    y1 = SystemRandom.choice(Zp)
    y2 = SystemRandom.choice(Zp)
    w = SystemRandom.choice(Zp)

    X = pow(g1, x1, p) * pow(g2, x2, p)
    Y = pow(g1, y1, p) * pow(g2, y2, p)
    W = pow(g1, w, p)

    private_key = {x1, x2, y1, y2, w}
    public_key = {p, g1, g2, X, Y, W}



    writefile("public_key.txt", public_key)

    return private_key, public_key
