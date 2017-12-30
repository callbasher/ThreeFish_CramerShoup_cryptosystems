#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.ThreeFish as tf
import src.IO as io


def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n")
    print("\t\t\tProjet GS15 - A17 - ThreeFish - CramerShoup")
    print("\nMenu :")
    print("\n\t1. Chiffrement symétrique ThreeFish" +
          "\n\t2. Chiffrement de Cramer-Shoup" +
          "\n\t3. Hashage d'un message" +
          "\n\t4. Déchiffrement sysmétrique ThreeFish" +
          "\n\t5. Déchiffrement Cramer-Shoup" +
          "\n\t6. Vérification d'un hash")
    x = int(input("Option : "))
    while x < 0 or x > 6:
        x = int(input("Option : "))
    return x


def apply(x):
    if x < 4:
        # Todo : Garder uniquement les inputs ici et mettre le reste dans ThreeFish (par ex dans une fct "apply"
        # Todo : avec tous les paramètres
        bloc = 64
        mode = 0
        while mode != 1 and mode != 2:
            mode = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))

        bloc_len = 0
        while (bloc_len != 256) and (bloc_len != 512) and (bloc_len != 1024):
            bloc_len = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))
        fichier = input("Veuillez entrer le chemin d'un fichier qui va être chiffré : ")
        word_len = int(bloc_len / 64)

        if x == 1:
            lect_fichier = io.readfile(fichier, bloc, True)
            lect_fichier = io.organize_data_list(lect_fichier, word_len)
            key, keyuser = tf.keygen(bloc_len)
            tabKey = tf.keygenturn(key)
            print("Voici votre clé symétrique sur ", bloc_len, " bits : \t\n######################################\t\n"
                  , keyuser, "\t\n######################################")
            # Todo : écrire la key user dans un fichier texte dans le même répertoire que le fichier qui va être chiffré

            padding_fichier = io.ajout_padding(lect_fichier, bloc_len)

            if mode == 1:
                chiff = tf.ECB_threefish_cipher(padding_fichier, tabKey)
            else:
                chiff = tf.CBC_threefish_cipher(padding_fichier, tabKey, bloc_len)

            io.writefilelist(fichier, chiff)
            io.rename_fichier(fichier, 0)

            print("Félicitation !! Chiffrement terminé.")

        if x == 2:
            io.rename_file(fichier, 1)
            lect_fichier = io.readfile(fichier, bloc, False)
            lect_fichier = io.organize_data_list(lect_fichier, bloc_len)

            # todo : faire une fonction qui va lire la clé sym et généré des clés avec keygenturn
            key = "ToDo"
            tabKey = io.keygenturn(key)

            if mode == 1:
                dchiff = tf.ECB_threefish_decipher(lect_fichier, tabKey)
            else:
                dchiff = tf.CBC_threefish_decipher(lect_fichier, tabKey, bloc_len)

            no_padding_list = io.remove_padding_list(dchiff, bloc_len)
            no_padding_data, valeur_pad = io.remove_padding_data(no_padding_list, bloc)

            io.write_file_list_pad(fichier, no_padding_data, valeur_pad)

            print("Félicitation !! Déchiffrement terminé.")

        if x == 3:
            print("Well Done !")

    elif x == 4:
        print("Well Done !")
    elif x == 5:
        print("Well Done !")

    elif x == 6:
        print("Well Done !")
