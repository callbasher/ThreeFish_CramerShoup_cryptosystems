#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.IO as IO
import src.Hash as Hh
import src.Util as Util
import src.ThreeFish as Tf
import src.CramerShoup as Cs
import src.Conversions as Conv


def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n\t\t\t"
          "Projet GS15 - A17 - ThreeFish - CramerShoup")

    display = "\nMenu:\n\t" \
              "1. Chiffrement symétrique ThreeFish\n\t" \
              "2. Déchiffrement sysmétrique ThreeFish\n\t" \
              "3. Chiffrement de Cramer-Shoup\n\t" \
              "4. Déchiffrement Cramer-Shoup\n\t" \
              "5. Hashage d'un message\n\t" \
              "6. Vérification d'un hash"
    x = -1
    while x < 0 or x > 6:
        print(display)
        x = int(input("Option : "))
    return x


def apply(x):
    if x < 3:
        mode = 0
        while mode != 1 and mode != 2:
            mode = int(input("Mode de (dé)chiffrement : \n\t1. ECB\n\t2. CBC\n"))
        key_len = 0
        while (key_len != 256) and (key_len != 512) and (key_len != 1024):
            key_len = int(input("Taille de la clé en bits(256/512/1024): "))
        file_key = input("Chemin du fichier de la clé: ")
        passwd_user = input("Mot de passe pour chiffrer la clé: ")
        file_path = input("Chemin du fichier à (dé)chiffrer : ")
        word_len = 64
        num_words = int(key_len / word_len)
        word_len_bytes = int(word_len / 8)

        if x == 1:
            file_data = IO.readfile(file_path, word_len, 1)
            file_data_list = Util.organize_data_list(file_data, num_words)
            encrypted_file = Tf.threefish_chiffrement(file_data_list, mode, key_len, passwd_user, file_key)
            IO.write_2D_list(file_path, encrypted_file, word_len_bytes)
            IO.rename_file(file_path, 0)

            print("Chiffrement terminé.")

        elif x == 2:
            ciph_data = IO.readfile(file_path, word_len, 0)
            ciph_data_list = Util.organize_data_list(ciph_data, num_words)
            clear_file_data, valeur_pad = Tf.threefish_dechiffrement(ciph_data_list, mode, key_len, word_len,
                                                                     passwd_user, file_key)
            IO.write_file_list_pad(file_path, clear_file_data, word_len_bytes, valeur_pad)
            IO.rename_file(file_path, 1)

            print("Déchiffrement terminé.")

    elif x == 3:
        filepath = input("Chemin du fichier à chiffrer:")
        file_data = IO.read_bytes(filepath)
        ans = ''
        while ans != 'y' and ans != 'n' and ans != 'Y' and ans != 'N':
            ans = input("Avez-vous un fichier de clé publique ? (y/n) ")
        if ans == 'y' or ans == 'Y':
            keypath = input("Chemin de la clé publique: ")
            ciph_data = Cs.encode_with_key(file_data, keypath)
        else:
            k = int(input("Taille de clé souhaitée en bits: "))
            password = input("Mot de passe pour chiffrer la clé privée: ")
            keypath = input("Chemin du répertoire des clés: ")
            ciph_data = Cs.encode_no_key(file_data, keypath, k, password)

        ciph_bytes = Conv.int_list2bytes(ciph_data, 8)
        IO.write_bytes(filepath, ciph_bytes)
        IO.rename_file(filepath, 0)

        print("Chiffrement terminé.")

    elif x == 4:
        filepath = input("Chemin du fichier à déchiffrer: ")
        file_data = IO.read_bytes(filepath)
        keypath = input("Chemin de la clé privée: ")
        password = input("Mot de passe: ")

        ciph_data = Conv.bytes2int_list(file_data, 8)
        clear_data = Cs.decode(ciph_data, keypath, password)
        IO.write_bytes(filepath, clear_data)
        IO.rename_file(filepath, 1)

        print("Déchiffrement terminé.")

    elif x == 5:
        hash_len = 0
        while hash_len != 256 and hash_len != 512 and hash_len != 1 and hash_len != 2:
            hash_len = int(input("1. BLAKE-256\n2. BLAKE-512\n"))
        if hash_len < 256:
            hash_len *= 32
        else:
            hash_len //= 8

        filepath = input("Chemin du fichier: ")
        with open(filepath, 'r') as rfile:
            file_data = rfile.read()

        ans = ''
        while ans != 'y' and ans != 'n' and ans != 'Y' and ans != 'N':
            ans = input("Protéger l'empreinte ? (y/n) ")

        key = ''
        if ans == 'y' or ans == 'Y':
            key = input("Mot de passe: ")

        h = hex(Hh.blake_hash(file_data, hash_len, key)) + '\n'

        # Rename file : "name.ext" -> "name~hash.ext"
        path = filepath.split('/')
        l = len(path)
        filename = path[l - 1].split('.')
        filename[0] += '~hash'
        path[l - 1] = '.'.join(filename)
        filepath = '/'.join(path)

        with open(filepath, 'w') as wfile:
            wfile.write(h)

    elif x == 6:
        hash_len = 0
        while hash_len != 256 and hash_len != 512 and hash_len != 1 and hash_len != 2:
            hash_len = int(input("1. BLAKE-256\n2. BLAKE-512\n"))
        if hash_len < 256:
            hash_len *= 32
        else:
            hash_len //= 8

        filepath = input("Chemin du fichier: ")
        with open(filepath, 'r') as rfile:
            file_data = rfile.read()

        hashpath = input("Chemin du hash: ")
        with open(hashpath, 'r') as hfile:
            hash = hfile.read()

        ans = ''
        while ans != 'y' and ans != 'n' and ans != 'Y' and ans != 'N':
            ans = input("Empreinte protégée ?(y/n) ")

        key = ''
        if ans == 'y' or ans == 'Y':
            key = input("Mot de passe: ")

        h = hex(Hh.blake_hash(file_data, hash_len, key)) + '\n'

        if h == hash:
            print("Les empreintes sont égales.")
        else:
            print("Les empreintes ne correspondent pas.")
