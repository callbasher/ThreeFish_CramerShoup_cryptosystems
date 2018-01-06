#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.IO as IO
import src.Util as Util
import src.ThreeFish as Tf
import src.CramerShoup as Cs

def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n")
    print("\t\t\tProjet GS15 - A17 - ThreeFish - CramerShoup")
    x = -1
    while x < 0 or x > 6:
        print("\nMenu :")
        print("\t"
            "1. Chiffrement symétrique ThreeFish\n\t"
            "2. Déchiffrement sysmétrique ThreeFish\n\t"
            "3. Chiffrement de Cramer-Shoup\n\t"
            "4. Déchiffrement Cramer-Shoup\n\t"
            "5. Hashage d'un message\n\t"
            "6. Vérification d'un hash")
        x = int(input("Option : "))
    return x


def apply(x):
    if x < 3:
        mode = 0
        while mode != 1 and mode != 2:
            mode = int(input("Veuillez choisir votre mode de (dé)chiffrement : \n\t1. ECB\n\t2. CBC"))

        key_len = 0
        while (key_len != 256) and (key_len != 512) and (key_len != 1024):
            key_len = int(input("Choisir la taille de clé à utiliser pour le (dé)chiffrement (256/512/1024) : "))

        file_key = input("Choisir un fichier pour stocker / lire votre clé : ")

        passwd_user = input("Choisir un mot de passe pour (dé)chiffrer votre clé : ")

        file_path = input("Veuillez entrer le chemin du fichier à (dé)chiffrer : ")

        word_len = 64
        num_words = int(key_len / word_len)
        word_len_bytes = int(word_len / 8)

        if x == 1:
            file_data = IO.readfile(file_path, word_len, 1)
            file_data_list = Util.organize_data_list(file_data, num_words)
            encrypted_file = Tf.threefish_chiffrement(file_data_list, mode, key_len, passwd_user, file_key)
            IO.writefilelist(file_path, encrypted_file, word_len_bytes)
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
        filepath = input("Entrer le chemin du fichier à chiffrer:")
        ans = ''
        while ans != 'y' and ans != 'n' and ans != 'Y' and ans != 'N':
            ans = input("Avez-vous une clé publique ?( y/n")
        if ans == 'y' or ans == 'Y':
            keypath = input("Entrer le chemin du fichier contenant la clé publique:")
            Cs.encode_with_file(filepath, keypath)
        else:
            k = int(input("Entrez la taille de clé souhaitée en bits:"))
            password = input("Entrez un mot de passe pour générer vos clés. Il servira a chiffrer votre clé privée.")
            keypath = input("Entrez le chemin où stocker les clés")
            Cs.encode_no_file(filepath, keypath, k, password)

    elif x == 4:
        filepath = input("Entrer le chemin du fichier à déchiffrer:")
        keypath = input("Entrer le chemin du fichier contenant la clé privée:")
        password = input("Entrez le mot de passe de la clé privée:")

        Cs.decode(filepath, keypath, password)

    elif x == 5:
        print("todo")

    elif x == 6:
        print("todo")
