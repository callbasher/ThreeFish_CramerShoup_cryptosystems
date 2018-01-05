#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.ThreeFish as tf
import src.IO as io
import src.Util as Util


def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n")
    print("\t\t\tProjet GS15 - A17 - ThreeFish - CramerShoup")
    x = -1
    while x < 0 or x > 6:
        print("\nMenu :\n\t")
        print(
            "\t1. Chiffrement symétrique ThreeFish\n\t"
            "2. Déchiffrement sysmétrique ThreeFish\n\t"
            "3. Chiffrement de Cramer-Shoup\n\t"
            "4. Déchiffrement Cramer-Shoup\n\t"
            "5. Hashage d'un message\n\t"
            "6. Vérification d'un hash")
        x = int(input("Option : "))
    return x


def apply(x):
    if x < 3:
        bloc_len = 64
        bloc_byte_len = int(bloc_len / 8)
        mode = 0
        while mode != 1 and mode != 2:
            mode = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))

        key_len = 0
        while (key_len != 256) and (key_len != 512) and (key_len != 1024):
            key_len = int(input("Choisir la taille de clé à utiliser pour le chiffrement (256/512/1024) : "))

        file_path = input("Veuillez entrer le chemin du fichier à chiffrer : ")
        word_len = int(key_len / 64)

        if x == 1:
            file_data = io.readfile(file_path, bloc_len, 1)
            file_data_list = Util.organize_data_list(file_data, word_len)

            encrypted_file = tf.threefish_chiffrement(file_data_list, mode, key_len)

            io.writefilelist(file_path, encrypted_file, bloc_byte_len)
            io.rename_file(file_path, 0)

            print("Chiffrement terminé.")

        elif x == 2:
            ciph_data = io.readfile(file_path, bloc_len, 0)
            ciph_data_list = Util.organize_data_list(ciph_data, word_len)

            clear_file_data, valeur_pad = tf.threefish_dechiffrement(ciph_data_list, mode, key_len, bloc_len)

            io.write_file_list_pad(file_path, clear_file_data, bloc_byte_len, valeur_pad)
            io.rename_file(file_path, 1)

            print("Déchiffrement terminé.")

    elif x == 3:
            print("todo")

    elif x == 4:
        print("todo")

    elif x == 5:
        print("todo")

    elif x == 6:
        print("todo")
