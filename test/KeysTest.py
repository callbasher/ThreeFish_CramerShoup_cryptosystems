#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Keys import *


def test_key_to_hex():
    key = [3344465465765713213456576, 3454565768765434546, 3454576756534213456, 34565654433456765]
    fk = format_key(key)
    print(fk)
    hexa = key2hex(fk)
    fkk = hex2key(hexa)
    print(fk == fkk)
    assert fk == fkk


def test_format_deformat_data():
    key = [3344465465765713213456576, 3454565768765434546, 3454576756534213456, 34565654433456765]
    fk = format_key(key)
    kk = deformat_key(fk)
    assert key == kk


def test_decipher_key():
    key = [3344465465765713213456576, 3454565768765434546, 3454576756534213456, 34565654433456765]
    c = cipher_key("pass", key)
    d = decipher_key("pass", c)
    assert key == d


def test_rw_key():
    key = [3344465435453454543557656576, 345456434546, 3454213456, 34565656765]
    keypath = "resources/"
    name = "test_key.txt"
    ckey = cipher_key("test", key)
    write_key(keypath, name, ckey)
    keypath += name
    kk = read_key(keypath)

    assert ckey == kk