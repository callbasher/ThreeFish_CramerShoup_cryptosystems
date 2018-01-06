#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Conversions import *


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
    assert p == int2str(a)


def test_int_list2hexa():
    l = [15, 33, 21, 12, 5]
    expected = 'Oxf1f15c5'

    assert expected == int_list2hexa(l)
