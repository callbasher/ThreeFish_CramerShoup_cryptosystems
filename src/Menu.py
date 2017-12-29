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
        if x == 1:
            # Todo : Garder uniquement les inputs ici et mettre le reste dans ThreeFish (par ex dans une fct "apply"
            # Todo : avec tous les paramètres
            bloc = 64
            print("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC")
            ModeChif = int(input("Option :"))
            while ModeChif != 1 and ModeChif != 2:
                ModeChif = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))

            L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))
            while (L_block != 256) and (L_block != 512) and (L_block != 1024):
                L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))

            fichier = input("Veuillez entrer le chemin d'un fichier qui va être chiffré : ")
            lect_fichier = io.readfile(fichier, bloc, 1)
            lect_fichier = io.organize_data_list(lect_fichier, L_block)

            key, keyuser = tf.keygen(L_block)
            tabKey = tf.keygenturn(key)
            print("Voici votre clé symétrique sur ", L_block, " bits : \t\n######################################\t\n"
                  , keyuser, "\t\n######################################")
            # Todo : écrire la key user dans un fichier texte dans le même répertoire que le fichier qui va être chiffré

            padding_fichier = io.ajout_padding(lect_fichier, L_block)

            if ModeChif == 1:
                chiff = tf.ECB_threefish_cipher(padding_fichier, tabKey)
            else:
                chiff = tf.CBC_threefish_cipher(padding_fichier, tabKey, L_block)

            io.writefilelist(fichier, chiff)
            io.rename_fichier(fichier, 0)

            print("Félicitation !! Chiffrement terminé.")

        if x == 2:
            bloc = 64
            print("Veuillez choisir votre mode de déchiffrement : \n\t1. ECB\n\t2. CBC")
            ModeChif = int(input("Option :"))
            while ModeChif != 1 and ModeChif != 2:
                ModeChif = int(input("Veuillez choisir votre mode de déchiffrement : \n\t1. ECB\n\t2. CBC"))

            L_block = int(input("Choisir la taille de bloc à utiliser pour le déchiffrement (256/512/1024) : "))
            while (L_block != 256) and (L_block != 512) and (L_block != 1024):
                L_block = int(input("Choisir la taille de bloc à utiliser pour le déchiffrement (256/512/1024) : "))

            fichier = input("Veuillez entrer le chemin d'un fichier qui va être déchiffré : ")
            io.rename_fichier(fichier, 1)
            lect_fichier = io.readfile(fichier, bloc, 0)
            lect_fichier = io.organize_data_list(lect_fichier, L_block)

            # todo : faire une fonction qui va lire la clé sym et généré des clés avec keygenturn
            key = "ToDo"
            tabKey = io.keygenturn(key)

            if ModeChif == 1:
                dchiff = tf.ECB_threefish_decipher(lect_fichier, tabKey)
            else:
                dchiff = tf.CBC_threefish_decipher(lect_fichier, tabKey, L_block)

            no_padding_list = io.remove_padding_list(dchiff, L_block)
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
