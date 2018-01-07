#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom
from crypto_gs15 import Arithmod, Conversions, Hash, Keys, Primes, Util


# The password is hashed to an int.
# This int correspond to the line in which the encrypted keys will be in the password file.
def encode_with_key(file_data, keypath):
    formatted_pb = Keys.read_key(keypath)
    public = Keys.deformat_key(formatted_pb)
    k = public[6]
    clear_data = Conversions.bytes2int_list(file_data, k >> 3)
    ciph_data = cipher_data(clear_data, public)
    return ciph_data


def encode_no_key(file_data, keypath, k, password):
    private, public = generate_keys(k)
    private = Keys.cipher_key(password, private)
    formatted_pb = Keys.format_key(public)
    Keys.write_key(keypath, "private_key.txt", private)
    Keys.write_key(keypath, "public_key.txt", formatted_pb)

    clear_data = Conversions.bytes2int_list(file_data, k >> 3)
    ciph_data = cipher_data(clear_data, public)
    return ciph_data


def decode(ciph_data, keypath, password):
    private = Keys.read_key(keypath)
    private = Keys.decipher_key(password, private)
    k = private[6]
    clear_data = decipher_data(ciph_data, private)
    file_data = Conversions.int_list2bytes(clear_data, k >> 3)
    return file_data


def cipher_data(bloc_list, public):
    ciph_blocs = []
    for bloc in bloc_list:
        ciph_blocs.extend(cipher_bloc(bloc, public))
    ciph_data = Util.encode_int_list(ciph_blocs)
    return ciph_data


def decipher_data(ciph_data, private):
    ciph_blocs = Util.decode_int_list(ciph_data)
    ciph_blocs = Util.organize_data_list(ciph_blocs, 4)
    bloc_list = []
    for b in ciph_blocs:
        bloc_list.append(decipher_bloc(b, private))
    return bloc_list


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
    h = Hash.blake_hash(str(concat), 64) % p
    v = (pow(X, b, p) * pow(Y, b * h, p)) % p

    return B1, B2, c, v


def decipher_bloc(bloc, key):
    p, x1, x2, y1, y2, w = key[0], key[1], key[2], key[3], key[4], key[5]
    B1, B2, c, v = bloc[0], bloc[1], bloc[2], bloc[3]

    # 1 : Validate bloc
    concat = (B1 + B2 + c) % p
    h = Hash.blake_hash(str(concat), 64) % p

    # Method 1
    bx = (pow(B1, x1, p) * pow(B2, x2, p)) % p
    by = (pow(B1, y1, p) * pow(B2, y2, p)) % p
    vv = (bx * pow(by, h, p)) % p

    # Compute res only if bloc is validated.
    if vv == v:
        return (Arithmod.inv(pow(B1, w, p), p) * c) % p


def generate_keys(k):
    p, g1, g2 = Primes.prime_and_generators(k)
    rand = SystemRandom()
    x1 = rand.randint(2, p)
    x2 = rand.randint(2, p)
    y1 = rand.randint(2, p)
    y2 = rand.randint(2, p)
    w = rand.randint(2, p)

    X = (pow(g1, x1, p) * pow(g2, x2, p)) % p
    Y = (pow(g1, y1, p) * pow(g2, y2, p)) % p
    W = pow(g1, w, p)

    private_key = [p, x1, x2, y1, y2, w, k]
    public_key = [p, g1, g2, X, Y, W, k]
    return private_key, public_key
