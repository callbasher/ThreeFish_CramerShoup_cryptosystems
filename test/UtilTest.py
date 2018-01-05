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


def test_format_deformat_key():
    key = [234345543543, 5676746745, 23432, 34543, 34345456576786534, 4565676554334]
    fk = format_key(key)
    kk = deformat_key(fk)
    assert key == kk


def test_pad_bin():
    a = '1'
    expected = '0001'
    assert expected == pad_bin(a, 4)


def test_pad_bin_no_pad():
    a = 'O11O'
    assert a == pad_bin(a, 4)


def test_ROTD_ROTG():
    a = 12345678987654321
    rg = rotate_left(bin(a)[2:], 49)
    rd = rotate_right(bin(rg)[2:], 49)
    assert a == rd
