#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
import Arithmod, Conversions, Keys, IO, Util

# Constants
tweak0 = Conversions.str2int("cogranne")
tweak1 = Conversions.str2int("gs15love")
tweak2 = tweak0 ^ tweak1
tweaks = [tweak0, tweak1, tweak2]
C = 0x1bd11bdaa9fc1a22
R = 49


# Is apply when the user chose the option 1 in the menu which is correspond to ThreeFish cipher
# input :
#   file_data_list = 2D array of int
#   mode = int, permit to choose between ecb or cbc decipher
#   key_len = int, length of the key, 256, 512 or 1024
# output = 2D array of int, correspond to the cipher data
def threefish_chiffrement(file_data_list, mode, key_len, passwd_user, file_key):
    key, keyuser = keygen(key_len)
    tab_key = keygenturn(key)
    # cipher the key using the password given by the user
    cipher_key = Keys.cipher_key(passwd_user, key)
    # writing cipher key in the specific file
    IO.write_2D_list(file_key, cipher_key, 8)

    Keys.print_key(key_len, keyuser)

    padded_file = Util.ajout_padding(file_data_list, key_len, 64)

    if mode == 1:
        return ecb_threefish_cipher(padded_file, tab_key)
    else:
        return cbc_threefish_cipher(padded_file, tab_key, key_len)


# Is apply when the user chose the option 2 in the menu which is correspond to ThreeFish decipher
# ciph_data_list = 2D array of int
#   mode = int, permit to choose between ecb or cbc decipher
#   key_len = int, length of the key, 256, 512 or 1024
#   bloc_len = int, length of the reading bloc, for threefish it is 8 bytes
# output :
#   file_data = 2D array of int, that correspond to decipher data
#   valeur_pad = int value that wil permit to remove padding data
def threefish_dechiffrement(ciph_data_list, mode, key_len, bloc_len, passwd_user, file_key):
    # reading the file where the key is
    cipher_key_desorganize = IO.readfile(file_key, 64, 0)
    # organize the data
    formatted_key = Util.organize_data_list(cipher_key_desorganize, 8)
    key = Keys.decipher_key(passwd_user, formatted_key)
    tab_key = keygenturn(key)

    if mode == 1:
        deciph_data = ecb_threefish_decipher(ciph_data_list, tab_key)
    else:
        deciph_data = cbc_threefish_decipher(ciph_data_list, tab_key, key_len)
    data_list = Util.remove_padding_list(deciph_data, key_len, bloc_len)
    file_data, valeur_pad = Util.remove_padding_data(data_list, bloc_len)

    return file_data, valeur_pad


# Generate a random key that will be send to keygenturn function
# to generate 20 keys that will be use to cipher in ECB and CBC functions
# input :
#   key_len = int that is 256, 512 or 1024
# output :
#   key = list of int
#   keyuser = keyuser is the key in hexadecimal that we print to the user
def keygen(key_len):
    key = []
    keyuser = ""
    hexkey = []
    k = 0
    num_words = int(key_len/64)
    for i in range(0, num_words - 1):
        n = getrandbits(64)
        key.append(n)
        k ^= n
        hexk = hex(n)[2:]
        if len(hexk) < 16:
            hexk = '0' * (16 - len(hexk)) + hexk
        hexkey.append(hexk)

        keyuser = ""
        for j in hexkey:
            keyuser += j
    k ^= C
    key.append(k)
    return key, keyuser


# Generate 20 keys based on the random key generate with the function keygen
# input :
#   key = list of int generate in the function keygen()
# output :
#   keys = 2D array of int, correspond to the 20 keys that are use in ecb or cbc cipher and decipher
def keygenturn(key):
    n = len(key) - 1
    mod = 2**64
    keys = []
    k = 0
    for i in range(0, 20):
        tab_key = []
        for k in range(0, (n - 3)):
            t = key[(i + k) % (n + 1)]
            tab_key.append(t)
            k ^= t

        # N - 3
        u = n - 3
        t = key[(i + u) % (n + 1)] + tweaks[i % 3] % mod
        tab_key.append(t)
        k ^= t
        # N - 2
        u = n - 2
        t = (key[(i + u) % (n + 1)]) + (tweaks[(i + 1) % 3]) % mod
        tab_key.append(t)
        k ^= t
        # N - 1
        u = n - 1
        t = (key[(i + u) % (n + 1)]) + i % mod
        tab_key.append(t)
        k ^= t
        k ^= C
        # k is the last word of 64 bits kn = k0+..+kn-1+C
        tab_key.append(k)
        keys.append(tab_key)
    return keys


# mix the data that is send from ciphers functions
# input :
#   datalist = list of int
# output :
#   datalistmix = list of int
def mixcolumn(datalist):
    # according to the block length we do 2, 4 or 8 times the mix
    datalistmix = []
    for i in range(0, len(datalist) - 1, 2):
        m11 = Arithmod.add_64bits(Conversions.int2bin_str(datalist[i]), Conversions.int2bin_str(datalist[i + 1]))
        m11 = Conversions.bin_str2int(m11)

        rotation = Util.rotate_right(Conversions.int2bin_str(datalist[(i + 1)]), R)

        m22 = Arithmod.xor_bin_str(Conversions.int2bin_str(m11), Conversions.int2bin_str(rotation))
        m22 = Conversions.bin_str2int(m22)
        datalistmix.append(m11)
        datalistmix.append(m22)
    return datalistmix


# Unmix the data send from the decipher functions
# input :
#   datalist = list of int
# output :
#   datalist_unmix = list of int
def inv_mixcolumn(datalist):
    # according to the block length we do 2, 4 or 8 times the mix
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        xor = Arithmod.xor_bin_str(Conversions.int2bin_str(datalist[i]), Conversions.int2bin_str(datalist[(i + 1)]))
        m2 = Util.rotate_left(xor, R)
        m1 = Arithmod.subtract_64bits(Conversions.int2bin_str(datalist[i]), Conversions.int2bin_str(m2))
        m1 = Conversions.bin_str2int(m1)
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix


# Permute the data send from cipher and decipher functions
# input :
#   n = list of int
# output :
#   n = list of int permute
def permute(n):
    return list(reversed(n))


# Do 76 tours for cipher data (use in ecb_threefish_cipher and in cbc_threefish_cipher)
# input :
#   data_list = list of int, correspond to a data that will be cipher
#   tabkeys = list of int, , correspond to a key generated
# output :
#   data_list = list of int, correspond to a cipher data
def cipher_tour(data_list, tabkeys):
    for k in range(0, 19):
        data_list = Arithmod.add_list_64bits(data_list, tabkeys[k])
        for i in range(4):
            data_list = mixcolumn(data_list)
            data_list = permute(data_list)
    return data_list


# Do 76 tours for decipher data (use in ecb_threefish_decipher and in cbc_threefish_decipher)
# input :
#   data_list = list of int, correspond to cipher data
#   tabkeys = list of int, correspond to a key generated
# output :
#   data_list = list of int, correspond to decipher data
def decipher_tour(data_list, tabkeys):
    counter = 18
    for k in range(0, 19):
        for i in range(4):
            data_list = permute(data_list)
            data_list = inv_mixcolumn(data_list)
        data_list = Arithmod.subtract_list_64bits(data_list, tabkeys[counter])
        counter -= 1
    return data_list


# Do ECB threefish cipher
# input :
#   datalist = 2D array of int, data that will be cipher
#   tabkeys = 2D array of int, correspond to the 20 keys generated
# output :
#   encrypt_list = 2D array of int, cipher data
def ecb_threefish_cipher(datalist, tabkeys):
    encryp_list = []
    for j in datalist:
        cipher_tour(j, tabkeys)
        j = Arithmod.add_list_64bits(j, tabkeys[19])
        encryp_list.append(j)
    return encryp_list


# Do ECB threefish decipher
# input :
#   datalist = 2D array of int, correspond to the cipher data
#   tabkeys = 2D array of int, correspond to the 20 keys generated
# output :
#   decrypt_list = 2D array of int, decipher data
def ecb_threefish_decipher(datalist, tabkeys):
    decrypt_list = []
    for j in datalist:
        j = Arithmod.subtract_list_64bits(j, tabkeys[19])
        decipher_tour(j, tabkeys)
        decrypt_list.append(j)
    return decrypt_list


# Do CBC threefish cipher
# input :
#   datalist = 2D array of int, data that will be cipher
#   tabkeys = 2D array of int, correspond to the 20 keys generated
#   bloc_len = int, permit to have the iv
# output :
#   encrypt_list = 2D array of int, correspond to cipher data
def cbc_threefish_cipher(datalist, tabkeys, bloc_len):
    iv = init(bloc_len)
    encryp_list = []
    datalist[0] = Arithmod.add_list_64bits(datalist[0], iv)
    var_count = 1
    anterior_occurence_counter = 0
    for j in datalist:
        if var_count == 0:
            j = Arithmod.add_list_64bits(j, encryp_list[anterior_occurence_counter])
            anterior_occurence_counter += 1
            cipher_tour(j, tabkeys)
        else:
            cipher_tour(j, tabkeys)
        j = Arithmod.add_list_64bits(j, tabkeys[19])
        encryp_list.append(j)
        var_count = 0
    return encryp_list


# Do CBC threefish decipher
# input :
#   datalist = 2D array of int, correpond to cipher data
#   tabkeys = 2D array of int, correspond to the 20 keys generated
#   bloc_len = int, this permit to have the iv
# output :
#   decrypt_list = tab of list of int, decipher data
def cbc_threefish_decipher(datalist, tabkeys, bloc_len):
    iv = init(bloc_len)
    decrypt_list = []
    for j in datalist:
        j = Arithmod.subtract_list_64bits(j, tabkeys[19])
        decipher_tour(j, tabkeys)
        decrypt_list.append(j)
    for i in range(1, len(decrypt_list)):
        decrypt_list[i] = Arithmod.subtract_list_64bits(decrypt_list[i], datalist[i - 1])
    decrypt_list[0] = Arithmod.subtract_list_64bits(decrypt_list[0], iv)
    return decrypt_list


# Return an IV based on the length of the block
# The IV is use in cbc_threefish_cipher and decipher functions to cipher and decipher data
# input :
#   key_len = int (256, 512 or 1024)
# output :
#   IV_* = list of int that correspond to an iv for CBC (de)cipher
def init(key_len):
    iv_256 = [11939804896947846136, 4219065746052997657, 14289511192216538576, 6129295191351922843]
    iv_512 = [14021392340165679391, 10713825714517858312, 16678454614520143940, 2176821685655837471,
              993364598582970774, 17432205245676079126, 15273195067266655935, 17670466041850028273]
    iv_1024 = [15345143141016669355, 13465911367260466770, 5383010510772685731, 10149785470626774238,
               616504849952386683, 9934305711475078234, 7510955176798512515, 10974823043510880208,
               10506771315442257531, 2703887491885455230, 506214325955753681, 7244289412050330942,
               15552188946686260547, 3934227692526149925, 8351231218515392481, 12278345771412770886]

    if key_len == 256:
        return iv_256
    elif key_len == 512:
        return iv_512
    elif key_len == 1024:
        return iv_1024
