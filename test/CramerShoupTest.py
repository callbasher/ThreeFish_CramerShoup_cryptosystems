#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.CramerShoup import *

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