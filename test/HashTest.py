#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crypto_gs15.Hash import *


def test_mix():
    v1 = 0x6A09E667F3BCC908  # Frac(Sqrt(2))
    v2 = 0xBB67AE8584CAA73B  # Frac(Sqrt(3))
    v3 = 0x3C6EF372FE94F82B  # Frac(Sqrt(5))
    v4 = 0xA54FF53A5F1D36F1  # Frac(Sqrt(7))
    x  = 0x510E527FADE682D1  # Frac(Sqrt(11))
    y  = 0x9B05688C2B3E6C1F  # Frac(Sqrt(13))

    m1 = mix(v1, v2, v3, v4, x, y)
    m2 = mix(v1, v2, v3, v4, x, y)

    assert m1 == m2


def test_compress():
    h = [0x6A09E667F3BCC908,
         0xBB67AE8584CAA73B,
         0x3C6EF372FE94F82B,
         0xA54FF53A5F1D36F1,
         0x510E527FADE682D1,
         0x9B05688C2B3E6C1F,
         0x1F83D9ABFB41BD6B,
         0x5BE0CD19137E2179]

    chunk1 = Conversions.str2bytes("test").zfill(128)
    chunk2 = Conversions.str2bytes("test").zfill(128)

    t = int(34).to_bytes(128, byteorder="little", signed=False)
    t2 = int(34).to_bytes(128, byteorder="little", signed=False)

    h1 = compress(h, chunk1, t, False)
    h2 = compress(h, chunk1, t, False)

    h3 = compress(h, chunk2, t2, True)
    h4 = compress(h, chunk2, t2, True)

    assert h1 == h2 and h3 == h4


def test_hash():
    h1 = blake_hash("pass", 64)
    h2 = blake_hash("pass", 64)

    fh = Util.encode_int_list([h1])
    fh2 = Util.encode_int_list([h2])

    print(fh)
    print(fh2)

    assert h1 == h2 and fh == fh2


def test_long_hash():
    str = "dfjlgdflsdmfjẐPERFIU4543656453353434523245fdgTRLMK$*P=" + \
          "É*L&&T'Tgjdflgjdfvndfljvdfgodfgldfgjdflgjdlfgjfdljgldfhqhqgmjqmg"+ \
          "DFSLJGDFSLGJSFDPOGEROPURPGJDFLJDFMOVKQ43553456567564fglrgjslesfsdhfsd"

    h1 = blake_hash(str, 64)
    h2 = blake_hash(str, 64)

    assert h1 == h2
