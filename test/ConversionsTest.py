#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crypto_gs15.Conversions import *


def test_int2bin_str():
    a = 7579627748166259002
    b = "0110100100110000001111110100011101000011001001001101000100111010"
    result = int2bin_str(a)
    assert result == b

def test_str2int():
    a = "toto"
    b = 1953461359
    result = str2int(a)
    assert result == b

def test_str2byte():
    a = "toto"
    b = b'toto'
    result = str2bytes(a)
    assert b == result

def test_bin_str2int():
    a = "0110100100110000001111110100011101000011001001001101000100111010"
    b = 7579627748166259002
    result = bin_str2int(a)
    assert result == b

def test_bytes2int_list():
    a = b'toot'
    b = [1953460084]
    result = bytes2int_list(a, 4)
    assert b == result

def test_int_list2bytes():
    a = [1953460084]
    b = b'toot'
    result = int_list2bytes(a, 4)
    assert b == result
