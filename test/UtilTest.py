#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Util import *


def test_xor_bytes():
    a = "0101111101011110011001001110111011001111000101101011100110000010"
    b = "1101111101011110011001001110111011001111000101101011100110000010"
    c = "1000000000000000000000000000000000000000000000000000000000000000"
    assert xor_bytes(a, b) == c


def test_add_64bits():
    a = "0000100100101001001101101011100111110111001111001110001100110110"
    b = "1000010100111111100100111001011000011011110011001011101010000001"
    c = "1000111001101000110010100101000000010011000010011001110110110111"
    assert add_64bits(a, b) == c


def test_subtract_64bits():
    a = "0000100100101001001101101011100111110111001111001110001100110110"
    b = "1000010100111111100100111001011000011011110011001011101010000001"
    c = "1000111001101000110010100101000000010011000010011001110110110111"
    assert subtract_64bits(c, b) == a


# Todo : Why are you testing your function bu just redoing the same ???
# You should init an input and its corresponding dsiered output directly
# like : in = 31, expected_out = "1F"
# return expected_out == int2byte_array(in)
def test_int2byte():
    a = 6869182828364843105
    b = 6869182828364843105
    output = []
    output1 = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, a & mask)
        a >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        output1.append(i)
    p = "".join(output1)
    p = str(p)
    assert p == int2bin_str(b)


# Todo : Same comment as above !!
def test_xor2list():
    liste1 = [18, 24, 52, 96]
    liste2 = [18, 24, 52, 96]
    result = xor_lists(liste1, liste2)
    m = [0, 0, 0, 0]
    begin = xor_lists(m, liste2)
    assert m == result
    assert begin == liste1


# Todo : Same comment as above !!
# Just do a rotg to x bytes and a rotd to x bytes and verify if the input stays the same
def test_ROTD_ROTG():
    a = "1101111101011110011001001110111011001111000101101011100110000010"
    x = bin_str2int(a)
    for i in range(76):
        b = rotate_right(a)
    b = bin_str2int(b)
    for i in range(76):
        c = rotate_left(b)
    assert str(c) == str(x)
