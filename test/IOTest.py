#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crypto_gs15.IO import *
import crypto_gs15.Conversions as Conv


def test_rw_bytes():
    filepath = "resources/test.txt"

    file_data = read_bytes(filepath)
    c = Conv.bytes2int_list(file_data, 13)
    file_data = Conv.int_list2bytes(c, 13)
    write_bytes(filepath, file_data)

    data = read_bytes(filepath)

    assert file_data == data
