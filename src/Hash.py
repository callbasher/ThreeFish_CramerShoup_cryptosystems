#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src import Util
import src.Conversions as Conv

sigma = [(0,   1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15),
         (14, 10,  4,  8,  9, 15, 13,  6,  1, 12,  0,  2, 11,  7,  5,  3),
         (11,  8, 12,  0,  5,  2, 15, 13, 10, 14,  3,  6,  7,  1,  9,  4),
         (7,   9,  3,  1, 13, 12, 11, 14,  2,  6,  5, 10,  4,  0, 15,  8),
         (9,   0,  5,  7,  2,  4, 10, 15, 14,  1, 11, 12,  6,  8,  3, 13),
         (2,  12,  6, 10,  0, 11,  8,  3,  4, 13,  7,  5, 15, 14,  1,  9),
         (12,  5,  1, 15, 14, 13,  4, 10,  0,  7,  6,  3,  9,  2,  8, 11),
         (13, 11,  7, 14, 12,  1,  3,  9,  5,  0, 15,  4,  8,  6,  2, 10),
         (6,  15, 14,  9, 11,  3,  0,  8, 12,  2, 13,  7,  1,  4, 10,  5),
         (10,  2,  8,  4,  7,  6,  1,  5, 15, 11,  9, 14,  3, 12, 13,  0)]

IV = [0x6A09E667F3BCC908,   # Frac(Sqrt(2))
      0xBB67AE8584CAA73B,   # Frac(Sqrt(3))
      0x3C6EF372FE94F82B,   # Frac(Sqrt(5))
      0xA54FF53A5F1D36F1,   # Frac(Sqrt(7))
      0x510E527FADE682D1,   # Frac(Sqrt(11))
      0x9B05688C2B3E6C1F,   # Frac(Sqrt(13))
      0x1F83D9ABFB41BD6B,   # Frac(Sqrt(17))
      0x5BE0CD19137E2179]   # Frac(Sqrt(19))


# Function that hash a String message to a binary string of length 'hash_len' with a optional string key
def blake_hash(m, hash_len, key=""):
    if hash_len > 64:
        raise ValueError("Blake hash does not support hash_length greater than 512 bits.")

    m = Conv.str2bytes(m)
    key = Conv.str2bytes(key)

    m_len = len(m)
    key_len = len(key)

    h = IV
    init_mix = int("0x0101" + hex(key_len)[2:] + hex(hash_len)[2:], 16)
    h[0] = h[0] ^ init_mix

    bytes_compressed = 0
    bytes_remaining = m_len

    if key_len > 0:
        if key_len > 128:
            key = key[:128]
        elif key_len < 128:
            key = key.zfill(128)
        m = key + m
        bytes_remaining += 128

    while bytes_remaining > 128:
        chunk = m[bytes_compressed:bytes_compressed+127]
        bytes_compressed += 128
        bytes_remaining -= 128
        t = bytes_compressed.to_bytes(128, byteorder='big', signed=False)
        h = compress(h, chunk, t, False)

    chunk = m[bytes_compressed:]
    bytes_compressed = bytes_compressed + bytes_remaining
    chunk = chunk.zfill(128)
    t = bytes_compressed.to_bytes(128, byteorder='big', signed=False)
    h = compress(h, chunk, t, True)

    h_bytes = b''
    i = 0
    while len(h_bytes) < hash_len and i < 8:
        h_bytes += h[i].to_bytes(8, byteorder='big', signed=False)
        i += 1

    return int.from_bytes(h_bytes[:hash_len], byteorder='big', signed=False)


def compress(h, chunk, t=b'0' * 128, is_last_bloc=False):
    v = h
    v.extend(IV)
    lo_bits = int.from_bytes(t[64:], byteorder='big', signed=False)
    hi_bits = int.from_bytes(t[:63], byteorder='big', signed=False)
    v[12] = v[12] ^ lo_bits
    v[13] = v[13] ^ hi_bits

    if is_last_bloc:
        v[14] = v[14] ^ 0xFFFFFFFFFFFFFFFF

    m = []
    for i in range(0, 128, 8):
        word = int.from_bytes(chunk[i:i+7], byteorder='big', signed=False)
        m.append(word)

    for i in range(0, 12):
        s = sigma[i % 10]

        v[0], v[4], v[8],  v[12] = mix(v[0], v[4], v[8],  v[12], m[s[0]], m[s[1]])
        v[1], v[5], v[9],  v[13] = mix(v[1], v[5], v[9],  v[13], m[s[2]], m[s[3]])
        v[2], v[6], v[10], v[14] = mix(v[2], v[6], v[10], v[14], m[s[4]], m[s[5]])
        v[3], v[7], v[11], v[15] = mix(v[3], v[7], v[11], v[15], m[s[6]], m[s[7]])

        v[0], v[5], v[10], v[15] = mix(v[0], v[5], v[10], v[15], m[s[8]],  m[s[9]])
        v[1], v[6], v[11], v[12] = mix(v[1], v[6], v[11], v[12], m[s[10]], m[s[11]])
        v[2], v[7], v[8],  v[13] = mix(v[2], v[7], v[8],  v[13], m[s[12]], m[s[13]])
        v[3], v[4], v[9],  v[14] = mix(v[3], v[4], v[9],  v[14], m[s[14]], m[s[15]])

    for i in range(8):
        h[i] ^= v[i] ^ v[i+8]

    return h


def mix(v1, v2, v3, v4, x, y):
    mod = 2**64
    v1 = (v1 + v2 + x) % mod
    v4 = Util.rotate_right(bin(v1 ^ v4)[2:], 32)

    v3 = (v3 + v4) % mod
    v2 = Util.rotate_right(bin(v2 ^ v3)[2:], 24)

    v1 = (v1 + v2 + y) % mod
    v4 = Util.rotate_right(bin(v1 ^ v4)[2:], 16)

    v3 = (v3 + v4) % mod
    v2 = Util.rotate_right(bin(v2 ^ v3)[2:], 63)

    return v1, v2, v3, v4
