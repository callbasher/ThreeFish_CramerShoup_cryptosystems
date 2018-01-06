#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom
import src.Hash as Hh
import src.IO as IO
import src.Primes as Pm
import src.Util as Util
import src.ArithMod as Arithmod
import src.Keys as Keys


# The password is hashed to an int.
# This int correspond to the line in which the encrypted keys will be in the password file.
# TODO : enable to cipher with an already-existing public key (retrieve the private with the password)
def encode_with_key(filepath, keypath):
    public = Keys.read_key(keypath)
    p = public[0]
    k = len(bin(p)[2:])

    clear_data = IO.readfile(filepath, k, 0)
    ciph_data = cipher_data(clear_data, public)

    return ciph_data


def encode_no_key(filepath, keypath, k, password):
    private, public = generate_keys(k)
    private = Util.cipher_key(password, private)
    public = Util.format_data(public)

    Keys.write_key(keypath, "private_key.txt", private)
    Keys.write_key(keypath, "public_key.txt", public)

    clear_data = IO.readfile(filepath, k, 0)
    ciph_data = cipher_data(clear_data, public)

    return ciph_data


def decode(filepath, keypath, password):
    private = Keys.read_key(keypath)
    private = Util.decipher_key(password, private)
    p = private[0]
    k = len(bin(p)[2:])

    ciph_data = IO.readfile(filepath, k, 0)
    clear_data = decipher_data(ciph_data, private)

    return clear_data


def cipher_data(clear_data, public):
    ciph_data = []
    for bloc in clear_data:
        ciph_bloc = cipher_bloc(bloc, public)
        ciph_data.extend(ciph_bloc)

    return Util.format_data(ciph_data)


def decipher_data(ciph_data, private):
    ciph_data = Util.deformat_data(ciph_data)
    ciph_blocs = Util.organize_data_list(ciph_data, 4)
    clear_data = []
    for b in ciph_blocs:
        clear_data.append(decipher_bloc(private, b))

    return clear_data


# The block is supposed to be an int.
# The key is a table containing p, alpha1, alpha2, X, Y, W
def cipher_bloc(bloc, key):
    p, a1, a2, X, Y, W = key[0], key[1], key[2], key[3], key[4], key[5]
    rand = SystemRandom()
    b = rand.randint(2, p-1)
    B1 = pow(a1, b, p)
    B2 = pow(a2, b, p)
    c = (pow(W, b, p) * bloc) % p
    concat = (B1 + B2 + c) % p
    h = Hh.blake_hash(str(concat), 64) % p
    exp = (b * h) % p
    v = (pow(X, b, p) * pow(Y, exp, p)) % p

    return B1, B2, c, v


def decipher_bloc(bloc, key):
    p, x1, x2, y1, y2, w = key[0], key[1], key[2], key[3], key[4], key[5]
    B1, B2, c, v = bloc[0], bloc[1], bloc[2], bloc[3]

    # 1 : Validate bloc
    concat = (B1 + B2 + c) % p
    h = Hh.blake_hash(str(concat), 64) % p

    # Method 1
    bx = (pow(B1, x1, p) * pow(B2, x2, p)) % p
    by = (pow(B1, y1, p) * pow(B2, y2, p)) % p
    vv = (bx * pow(by, h, p)) % p

    # Method 2
    exp1 = (x1 + h * y2) % p
    exp2 = (x2 + h * y2) % p
    vv2 = (pow(B1, exp1, p) * pow(B2, exp2, p)) % p

    print(v)
    print(vv)
    print(vv2)

    # Compute res only if bloc is validated.
    if vv == v:
        clear = (Arithmod.inv(pow(B1, w, p), p) * c) % p
        return clear


def generate_keys(k):
    p, g1, g2 = Pm.prime_and_generators(k)
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
