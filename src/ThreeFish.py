#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
import src.Util as util
import src.IO as io

# Constants
# R bits shift
R = 49
# first tweak on 64 bits (cogranne)
tweak0 = 99111103114097110110101
# second tweak on 64 bits (gs15love)
tweak1 = 103115049053108111118101
tweak2 = tweak0 ^ tweak1
tweaks = [tweak0, tweak1, tweak2]
# 0x1bd11bdaa9fc1a22 in hexa C = constant for key generation
C = 513129967392069919254


# function that is apply when the user chose the option 1 in the menu
def threefish_chiffrement(file_data_list, mode, key_len, bloc_len):
    key, keyuser = keygen(key_len, bloc_len)
    tabKey = keygenturn(key)
    io.print_key(key_len, keyuser)

    # Todo : écrire la key user dans un fichier texte dans le même répertoire que le fichier qui va être chiffré

    padded_file = io.ajout_padding(file_data_list, key_len, 64)

    if mode == 1:
        return ECB_threefish_cipher(padded_file, tabKey)
    else:
        return CBC_threefish_cipher(padded_file, tabKey, key_len)


# function tha is apply when the user chose the option 2 in the menu
def threefish_dechiffrement(ciph_data_list, mode, key_len, bloc_len):
    # todo : faire une fonction qui va lire la clé sym et généré des clés avec keygenturn
    key = "ToDo"
    tabKey = keygenturn(key)

    if mode == 1:
        deciph_data = ECB_threefish_decipher(ciph_data_list, tabKey)
    else:
        deciph_data = CBC_threefish_decipher(ciph_data_list, tabKey, key_len)

    data_list = io.remove_padding_list(deciph_data, key_len, bloc_len)
    file_data, valeur_pad = io.remove_padding_data(data_list, bloc_len)

    return file_data


# function that generate a random key
# input = int that is 256, 512 or 1024
# output0 = list of int (key)
# output1 = str (keyuser)
def keygen(key_len, bloc_len):
    key = []
    keyuser = ""
    hexkey = []
    k = 0
    for i in range(0, int(key_len/bloc_len) - 1):
        n = getrandbits(bloc_len)
        key.append(n)
        k ^= n
        hexk = util.int2str_hexa(n)
        if len(hexk) != 16:
            pad = "0"
            hexk = (16 - (len(str(hexk)))) * pad + str(hexk)
            hexkey.append(hexk)
        else:
            hexkey.append(hexk)

        # keyuser is the hexa key that we gonna give to the user
        keyuser = ""
        for j in hexkey:
            keyuser += j
    k ^= C
    key.append(k)
    return key, keyuser


# function that generate 20 keys based on the random key generate with the function keygen
# input = list of int
# output = tab of list of int
def keygenturn(key):
    N = len(key) - 1
    keys = []
    k = 0
    for i in range(0, 20):
        tabKey = []
        for n in range(0, (N - 3)):
            t = key[(i + n) % (N + 1)]
            tabKey.append(t)
            k ^= t

        # N - 3
        n = N - 3
        t = (key[(i + n) % (N + 1)]) + (tweaks[i % 3])
        # We want t % 2^64
        # We truncate the hexadecimal characters over the range of 2^64
        tHex = hex(t)
        tStr = str(tHex)
        tStr = tStr[len(tStr)-16:len(tStr)]
        t = int(tStr, 16)
        # it computes the modulo without doing the 2^64 operation
        tabKey.append(t)
        k ^= t
        # N - 2
        n = N - 2
        t = (key[(i + n) % (N + 1)]) + (tweaks[(i + 1) % 3]) % (2**64)
        tabKey.append(t)
        k ^= t
        # N - 1
        n = N - 1
        t = (key[(i + n) % (N + 1)]) + i % (2**64)
        tabKey.append(t)
        k ^= t
        k^= C
        # k is the last word of 64 bits kn = k0+..+kn-1+C
        tabKey.append(k)
        keys.append(tabKey)
    return keys


# function that mix data
# input = list of int
# output = list of int
def mixcolumn(datalist):
    # according to the block length we do 2, 4 or 8 times the mix
    datalistmix = []
    for i in range(0, len(datalist) - 1, 2):
        m11 = util.add_64bits(util.int2byte_array(datalist[i]), util.int2byte_array(datalist[i + 1]))
        m11 = util.bin_str2int(m11)

        rotation = util.rotate_right(util.int2byte_array(datalist[(i + 1)]), R)

        m22 = util.xor_bytes(util.int2byte_array(m11), util.int2byte_array(rotation))
        m22 = util.bin_str2int(m22)
        datalistmix.append(m11)
        datalistmix.append(m22)
    return datalistmix


# function that unmix data
# intput = list of int
# output = list of int
def inv_mixcolumn(datalist):
    # according to the block lenght we do 2, 4 or 8 times the mix
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        xor = util.xor_bytes(util.int2byte_array(datalist[i]), util.int2byte_array(datalist[(i + 1)]))
        m2 = util.rotate_left(xor, R)
        m1 = util.subtract_64bits(util.int2byte_array(datalist[i]), util.int2byte_array(m2))
        m1 = util.bin_str2int(m1)
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix


# function that permute data
# intput = list of int
# output = list of int
def permute(n):
    return list(reversed(n))


# function that do ECB threefish encryption
# intput = tab of list of int
# output = tab of list of int
def ECB_threefish_cipher(datalist, tabkeys):
    encryp_list = []
    for j in datalist:
        for k in range(0, 19):
            j = util.add_list_64bits(j, tabkeys[k])
            for i in range(4):
                j = mixcolumn(j)
                j = permute(j)
        j = util.add_list_64bits(j, tabkeys[19])
        encryp_list.append(j)
    return encryp_list


# function that do ECB threefish decipherment
# intput = tab of list of int
# output = tab of list of int
def ECB_threefish_decipher(datalist, tabkeys):
    decrypt_list = []
    for j in datalist:
        counter = 18
        j = util.subtract_list_64bits(j, tabkeys[19])
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = util.subtract_list_64bits(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    return decrypt_list


# function that do CBC threefish encryption
# intput = tab of list of int
# output = tab of list of int
def CBC_threefish_cipher(datalist, tabkeys, bloc_len):
    iv = init(bloc_len)
    encryp_list = []
    datalist[0] = util.add_list_64bits(datalist[0], iv)
    var_count = 1
    anterior_occurence_counter = 0
    for j in datalist:
        if var_count == 0:
            # modular addition with the current occurence and the cipher occurence before
            j = util.add_list_64bits(j, encryp_list[anterior_occurence_counter])
            anterior_occurence_counter += 1
            for k in range(0, 19):
                j = util.add_list_64bits(j, tabkeys[k])
                for i in range(4):
                    j = mixcolumn(j)
                    j = permute(j)
        else:
            for k in range(0, 19):
                j = util.add_list_64bits(j, tabkeys[k])
                for i in range(4):
                    j = mixcolumn(j)
                    j = permute(j)
        j = util.add_list_64bits(j, tabkeys[19])
        encryp_list.append(j)
        var_count = 0
    return encryp_list


# function that do CBC threefish decipherment
# intput = tab of list of int
# output = tab of list of int
def CBC_threefish_decipher(datalist, tabkeys, bloc_len):
    iv = init(bloc_len)
    decrypt_list = []
    for j in datalist:
        j = util.subtract_list_64bits(j, tabkeys[19])
        counter = 18
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = util.subtract_list_64bits(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    # modular substract with the cipher occurence before and the decipher occurence
    for i in range(1, len(decrypt_list)):
        decrypt_list[i] = util.subtract_list_64bits(decrypt_list[i], datalist[i - 1])
    # xor between the iv and the first occurence
    decrypt_list[0] = util.subtract_list_64bits(decrypt_list[0], iv)
    return decrypt_list


# function that return an IV based on the length of the block
# input = int (256, 512 or 1024)
# output = list of int
def init(key_len):
    IV_256 = [11939804896947846136, 4219065746052997657, 14289511192216538576, 6129295191351922843]
    IV_512 = [14021392340165679391, 10713825714517858312, 16678454614520143940, 2176821685655837471,
              993364598582970774, 17432205245676079126, 15273195067266655935, 17670466041850028273]
    IV_1024 = [15345143141016669355, 13465911367260466770, 5383010510772685731, 10149785470626774238,
               616504849952386683, 9934305711475078234, 7510955176798512515, 10974823043510880208,
               10506771315442257531, 2703887491885455230, 506214325955753681, 7244289412050330942,
               15552188946686260547, 3934227692526149925, 8351231218515392481, 12278345771412770886]

    if key_len == 256:
        return IV_256
    elif key_len == 512:
        return IV_512
    elif key_len == 1024:
        return IV_1024
