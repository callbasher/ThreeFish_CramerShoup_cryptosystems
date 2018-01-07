#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Util import *
from random import getrandbits


def test_encode_decode_int_list():
    a = 2**64 - 1
    i = getrandbits(245)
    t = [0, 1, a, 1, i, 0,  a, i, 1]
    ft = encode_int_list(t)
    tt = decode_int_list(ft)
    assert t == tt


def test_add_padding():
    d = [[334446546576571321, 34545657685446, 345454213456, 56544334567]]
    pad_data = add_padding_v2(d, 8, 64)
    print(d)
    dd = remove_padding_listv2(pad_data, 8, 64)
    print(dd)
    assert d == dd


def test_ajout_pad():
    d = [[334446546576571321, 34545657685446, 345454213456, 56544334567]]
    pad_data = ajout_padding(d, 256, 64)
    dd = remove_padding_list(pad_data, 256, 64)
    assert d == dd


def test_pad_bin():
    a = '1'
    expected = '0001'
    assert expected == pad_bin(a, 4)


def test_pad_bin_no_pad():
    a = 'O11O'
    assert a == pad_bin(a, 4)


def test_rotations():
    a = 12345678987654321
    rg = rotate_left(bin(a)[2:], 49)
    rd = rotate_right(bin(rg)[2:], 49)
    assert a == rd

