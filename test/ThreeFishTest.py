#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crypto_gs15.ThreeFish import *
from crypto_gs15 import IO, Arithmod as Ar


# test de la fonction permute
def test_permute():
    list_test = [12, 26, 57, 89]
    list_test_permute = [89, 57, 26, 12]
    a = permute(list_test)
    assert a == list_test_permute


# test de la fonction mixcolumn
def test_mix():
    liste = [6869182828364843105, 5685451262666598955, 6869182828364843105, 5685451262666598955]
    liste_mix = [12554634091031442060, 14834149863215961599, 12554634091031442060, 14834149863215961599]
    liste_mix_fct = mixcolumn(liste)
    assert liste_mix == liste_mix_fct


def test_unmix():
    liste = [6869182828364843105, 14834149863215961599, 6869182828364843105, 5685451262666598955]
    mix = mixcolumn(liste)
    unmix = inv_mixcolumn(mix)
    assert unmix == liste


def test_inv_ECB():
    liste1 = [[18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651]]
    liste2keys = [[654, 5, 54, 54], [654, 654, 654, 5], [65, 54, 54, 54], [54, 54, 654, 654], [987, 987, 84, 84], [6884, 684, 654, 64], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [6551, 61, 51, 51], [561, 651, 651, 61]]
    a = ecb_threefish_cipher(liste1, liste2keys)
    b = ecb_threefish_decipher(a, liste2keys)
    assert liste1 == b


def test_inv_CBC():
    key, userk = keygen(256)
    all_keys = keygenturn(key)
    data = IO.readfile("../test/resources/test.txt", 64, 1)
    data_org = Util.organize_data_list(data, 4)
    data_org_pad = Util.ajout_padding(data_org, 256, 64)
    c = cbc_threefish_cipher(data_org_pad, all_keys, 256)
    d = cbc_threefish_decipher(c, all_keys, 256)
    data_org_pad[0] = Ar.subtract_list_64bits(data_org_pad[0], init(256))
    assert d == data_org_pad


def test_keygenturn():
    k, keyuser = keygen(256)

    t1 = keygenturn(k)
    t2 = keygenturn(k)

    assert t1 == t2


def test_ecb():
    h = [0x6A09E667F3BCC908,
         0xBB67AE8584CAA73B,
         0x3C6EF372FE94F82B,
         0xA54FF53A5F1D36F1,
         0x510E527FADE682D1,
         0x9B05688C2B3E6C1F,
         0x1F83D9ABFB41BD6B,
         0x5BE0CD19137E2179]
    key, keyuser = keygen(512)
    turn_keys = keygenturn(key)
    a = [h, permute(h)]
    c = ecb_threefish_cipher(a, turn_keys)
    d = ecb_threefish_decipher(c, turn_keys)

    assert a == d

def test_iv_function():
    iv_256 = [11939804896947846136, 4219065746052997657, 14289511192216538576, 6129295191351922843]
    return_iv = init(256)
    assert iv_256 == return_iv
