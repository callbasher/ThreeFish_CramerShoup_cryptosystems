#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom, randint
import src.Hash as Hh
import src.IO as IO
import src.Primes as Pm
import src.Util as Util
import src.Conversions as Conv
import src.ArithMod as Arithmod


# The password is hashed to an int.
# This int correspond to the line in which the encrypted keys will be in the password file.
# TODO : enable to cipher with an already-existing public key (retrieve the private with the password)
def encode_with_file(filepath, keypath):
    return 0

def encode_no_file(filepath, keypath, k, password):
    private, public = generateKeys(k)
    cipher_pv = Util.cipher_key(password, private)
    formatted_pb = Util.encode_int_list(public)
    IO.writeKey(key_dest, public)
    bloc_list = IO.readfile(fichier, 64, 0)
    crypt_bytes = []
    for b in bloc_list:
        crypt_bytes.append(cipher(b, public))
    return 0


def decode(fichier, password):
    # retrieve private Key
    pv_key = retrieve_key(password)
    file = IO.readfile(fichier, 64, 0)
    bloc_list = IO.organize_data_list(file, 4)
    clear = []
    for b in bloc_list:
        clear.append(decipher(key, b))


# The block is supposed to be an int.
# The key is a table containing p, alpha1, alpha2, X, Y, W
def cipher(bloc, key):
    p, a1, a2, X, Y, W = key[0], key[1], key[2], key[3], key[4], key[5]
    b = randint(0, p)
    B1 = pow(a1, b, p)
    B2 = pow(a2, b, p)
    c = (pow(W, b, p) * bloc) % p
    concat = (B1 + B2 + c) % p
    H = Hh.blake_hash(concat, 64)

    v = (pow(X, b, p) * pow(Y, b*H, p)) % p

    return B1, B2, c, v


def decipher(key, bloc):
    p, x1, x2, y1, y2, w = key[0], key[1], key[2], key[3], key[4], key[5]
    B1, B2, v, c = bloc[0], bloc[1], bloc[2], bloc[3]

    # 1 : Validate bloc
    concat = (B1 + B2 + c) % p
    H = Hh.blake_hash(Conv.int2str(concat), 64)
    By = (pow(B1, y1, p) * pow(B2, y2, p)) % p
    vv = (pow(B1, x1, p) * pow(B2, x2, p) * pow(By, H, p)) % p
    # Compute res only if bloc is validated.
    if vv == v:
        return (Arithmod.inv(pow(B1, w, p), p) * c) % p


def find_generator(p, factors):
    b = 1
    rand = SystemRandom()
    while b == 1:
        x = rand.randint(2, p)
        for f in factors:
            exp = (p-1) // f
            b = pow(x, exp, p)
            if b != 1:
                break
    return b


def prime_and_generators(k):
    p, q, r = Pm.safe_prime(k)
    # prime factors of p-1
    # we want only the different prime factors not their exponent so we remove duplicates
    # We put q at the end of the list to ensure that smaller factors are tried first
    # in "find_generator" function
    factors = Pm.factorize(r)
    factors.append(2)
    factors = list(set(factors))
    factors.append(q)

    alpha1 = find_generator(p, factors)
    alpha2 = alpha1
    while alpha1 == alpha2:
        alpha2 = find_generator(p, factors)

    return p, alpha1, alpha2


def generateKeys(k):
    p, g1, g2 = prime_and_generators(k)
    rand = SystemRandom()
    x1 = rand.randint(2, p)
    x2 = rand.randint(2, p)
    y1 = rand.randint(2, p)
    y2 = rand.randint(2, p)
    w = rand.randint(2, p)

    X = (pow(g1, x1, p) * pow(g2, x2, p)) % p
    Y = (pow(g1, y1, p) * pow(g2, y2, p)) % p
    W = pow(g1, w, p)

    private_key = [p, x1, x2, y1, y2, w]
    public_key = [p, g1, g2, X, Y, W]

    return private_key, public_key
