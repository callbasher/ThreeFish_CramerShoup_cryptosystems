#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Keys import *
import src.ThreeFish as Tf
import src.Util as Util


def test_key_to_hex():
    key, ku = Tf.keygen(256)
    key = Util.format_data(key)
    expected = key
    hexa = key2hex(expected)
    fkey = hex2key(hexa)
    assert expected == fkey