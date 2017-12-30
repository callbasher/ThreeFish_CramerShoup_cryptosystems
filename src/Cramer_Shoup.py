#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom, randint, seed
import src.Hash as Hh
import src.IO as IO
import src.Primes as Pm
import src.Util as util


# The password is hashed to an int.
# This int correspond to the line in which the encrypted keys will be in the password file.
# TODO : enable to cipher with an already-existing public key (retrieve the private with the password)
def apply(fichier, public_key_dest, k = 512, password = "default"):
    private, public = generateKeys(k)
    write_pv_key(password, private)
    IO.writefile(public_key_dest, public)
    bloc_list = IO.readfile(fichier, 64, 0)
    crypt_bytes = []
    for b in bloc_list:
        crypt_bytes.append(cipher(public, b))


# The block is supposed to be an int.
# The key is a table containing p, alpha1, alpha2, X, Y, W
def cipher(key, bloc):
    p, a1, a2, X, Y, W = key[0], key[1], key[2], key[3], key[4], key[5]
    b = randint(0, p)
    B1 = pow(a1, b, p)
    B2 = pow(a2, b, p)
    c = (pow(W, b, p) * bloc) % p
    concat = (B1 + B2 + c) % p
    H = Hh.hashInt(concat)

    v = (pow(X, b, p) * pow(Y, b*H, p)) % p

    return B1, B2, c, v


def decode(fichier, password):
    # retrieve private Key
    key = retrieve_key(password)
    file = IO.readfile(fichier, 64, 0)
    bloc_list = IO.organize_data_list(file, 4)
    clear = []
    for b in bloc_list:
        clear.append(decipher(key, b))


def decipher(key, bloc):
    p, x1, x2, y1, y2, w = key[0], key[1], key[2], key[3], key[4], key[5]
    B1, B2, v, c = bloc[0], bloc[1], bloc[2], bloc[3]

    # 1 : Validate bloc
    concat = (B1 + B2 + c) % p
    beta = Hh.hashInt(concat)
    By = (pow(B1, y1, p) * pow(B2, y2, p)) % p
    vv = (pow(B1, x1, p) * pow(B2, x2, p) * pow(By, beta, p)) % p
    if vv == v:
        return (util.inv(pow(B1, w, p), p) * c) % p


def write_pv_key(password, key):
    pv_ciph = sym_cipher(password, key)
    tab_keys = IO.read_tab_keys()
    ind = hash_pass(password)
    tab_keys[ind] = pv_ciph
    IO.write_tab_keys(tab_keys)


def hash_pass(password):
    passInt = Hh.hashInt(password)
    seed(passInt)
    return randint(0, 10000)


def retrieve_key(password):
    tab_keys = IO.read_tab_keys()
    ind = hash_pass(password)
    return tab_keys[ind]


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
    p, q, r = Pm.safe_prime(k)
    # prime factors of p-1
    # we want only the different prime factors not their exponent so we remove duplicates
    # We put q at the end of the list to ensure that smaller factors are tried first
    # in "find_generator" function
    factors = set(Pm.factorize(r))
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

    private_key = {p, x1, x2, y1, y2, w}
    public_key = {p, g1, g2, X, Y, W}

    return private_key, public_key
