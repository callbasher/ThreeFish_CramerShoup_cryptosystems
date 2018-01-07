#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.IO import *
import src.Conversions as Conv


def test_basic_rw():
    filepath = "resources/test2.txt"

    with open(filepath, 'rb') as rfile:
        data = rfile.read()

    with open(filepath, 'wb') as wfile:
        wfile.write(data)


def test_rw_bytes():
    filepath = "resources/test2.txt"

    file_data = read_bytes(filepath)
    c = Conv.bytes2int_list(file_data, 13)
    file_data = Conv.int_list2bytes(c, 13)
    write_bytes(filepath, file_data)

    data = read_bytes(filepath)

    assert file_data == data


def test_rw_file():
    filepath = "resources/test2.txt"

    file_data = readfile(filepath, 64, 0)
    write_list(filepath, file_data, 8)
    data = readfile(filepath, 64, 1)

    assert file_data == data