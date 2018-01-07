#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crypto_gs15.CramerShoup import *
from crypto_gs15 import IO, Conversions as Conv

private, public = generate_keys(128)


def test_cipher_bloc():
    bloc = 4546546546
    print(public)

    c = cipher_bloc(bloc, public)
    d = decipher_bloc(c, private)

    assert bloc == d


def test_cipher_data():
    data = [0, 1, 12, 47]

    c = cipher_data(data, public)
    d = decipher_data(c, private)

    assert data == d


def test_encode():
    filepath = "resources/test.txt"
    keypath = "resources/"
    k = 512
    password = "test"

    file_data = IO.read_bytes(filepath)
    c = encode_no_key(file_data, keypath, k, password)
    ciph_bytes = Conv.int_list2bytes(c, 8)
    IO.write_bytes(filepath, ciph_bytes)
    IO.rename_file(filepath, 0)

    filepath = "resources/test.txt.encrypt"
    keypath = "resources/private_key.txt"

    ciph_bytes = IO.read_bytes(filepath)
    ciph_data = Conv.bytes2int_list(ciph_bytes, 8)
    clear_data = decode(ciph_data, keypath, password)
    IO.write_bytes(filepath, clear_data)
    IO.rename_file(filepath, 1)

    assert file_data == clear_data
