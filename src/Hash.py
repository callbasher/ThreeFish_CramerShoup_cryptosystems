#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.Util as util

sigma = [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
         (14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3),
         (11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4),
         (7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8),
         (9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13),
         (2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9),
         (12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11),
         (13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10),
         (6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5),
         (10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0)]

IV = [0x6A09E667F3BCC908,   # Frac(Sqrt(2))
      0xBB67AE8584CAA73B,   # Frac(Sqrt(3))
      0x3C6EF372FE94F82B,   # Frac(Sqrt(5))
      0xA54FF53A5F1D36F1,   # Frac(Sqrt(7))
      0x510E527FADE682D1,   # Frac(Sqrt(11))
      0x9B05688C2B3E6C1F,   # Frac(Sqrt(13))
      0x1F83D9ABFB41BD6B,   # Frac(Sqrt(17))
      0x5BE0CD19137E2179]   # Frac(Sqrt(19))


def blake_hash(M, hash_len, key = []):
    # M and key are considered to be byte arrays
    m_len = len(M)
    key_len = len(key)
    # init h as the init vector
    h = IV
    hex_mix = hex("OxO101" + str(hex(key_len)).replace("Ox", "") + str(hex(m_len).replace("Ox", "")))
    h[0] = h[0] ^ hex_mix

    bytes_compressed = 0
    bytes_remaining = m_len

    if key_len:
        M = util.pad(key, 128).append(M)
        bytes_remaining += 128

    while bytes_remaining > 128:
        chunk = M[bytes_compressed:bytes_compressed+127]
        bytes_compressed += 128
        bytes_remaining -= 128
        h = compress(h, chunk, util.int2byte_array(bytes_compressed), False)

    chunk = M[bytes_compressed:]
    bytes_compressed = bytes_compressed + bytes_remaining
    chunk = util.pad(chunk, 128)
    h = compress(h, chunk, util.int2byte_array(bytes_compressed), True)

    return h[:hash_len-1]


def compress(h, m=[], t=b'0' * 128, is_last_bloc=False):
    V = h
    V.append(IV)
    V[12] = util.xor_bytes(V[11], t[64:])
    V[13] = util.xor_bytes(V[12], t[:63])

    if is_last_bloc:
        V[14] = util.xor_bytes(V[14], util.int2byte_array(2**64))

    for i in range(0, 12):
        s = sigma[i % 10]

        V[0], V[4], V[8], V[12] = mix(V[0], V[4], V[8], V[12], m[s[0]], m[s[1]])
        V[1], V[5], V[9], V[13] = mix(V[1], V[5], V[9], V[13], m[s[2]], m[s[3]])
        V[2], V[6], V[10], V[14] = mix(V[2], V[6], V[10], V[14], m[s[4]], m[s[5]])
        V[3], V[7], V[11], V[15] = mix(V[3], V[7], V[11], V[15], m[s[6]], m[s[7]])

        V[0], V[5], V[10], V[15] = mix(V[0], V[5], V[10], V[15], m[s[8]], m[s[9]])
        V[1], V[6], V[11], V[12] = mix(V[1], V[6], V[11], V[12], m[s[10]], m[s[11]])
        V[2], V[7], V[8], V[13] = mix(V[2], V[7], V[8], V[13], m[s[12]], m[s[13]])
        V[3], V[4], V[9], V[14] = mix(V[3], V[4], V[9], V[14], m[s[14]], m[s[15]])

    h = util.xor_bytes(h, V[0:7])
    h = util.xor_bytes(h, V[8:15])
    return h


def mix(Va, Vb, Vc, Vd, x, y):
    Va = util.add_64bits(util.add_64bits(Va, Vb), x)
    Vd = util.rotate_right(util.xor_bytes(Va, Vd), 32)

    Vc = util.add_64bits(Vc, Vd)
    Vb = util.rotate_right(util.xor_bytes(Vb, Vc), 24)

    Va = util.add_64bits(util.add_64bits(Va, Vb), y)
    Vd = util.rotate_right(util.xor_bytes(Va, Vd), 16)

    Vc = util.add_64bits(Vc, Vd)
    Vb = util.rotate_right(util.xor_bytes(Vb, Vc), 63)

    return Va, Vb, Vc, Vd