#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ThreeFish import *
from Cramer_Shoup import *

def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n")
    print("\t\t\tProjet GS15 - A17 - ThreeFish - CramerShoup")
    print("\nMenu :\n")
    print(
        "\t1. Chiffrement symétrique ThreeFish\n\t2. Chiffrement de Cramer-Shoup\n\t3. Hashage d'un message\n\t4. Déchiffrement sysmétrique ThreeFish\n\t"
        + "5. Déchiffrement Cramer-Shoup\n\t6. Vérification d'un hash")
    x = int(input("Option : "))
    while x < 0 or x > 6:
        x = int(input("Option : "))

    return x


def apply(x):
    if x < 4:
        if x == 1:
            fich = input("Veuillez entrer le chemin du fichier à chiffrer : ")
            fichier = readfile(fich)            # C:\Users\aurélien\Google Drive
            print(fichier)


            print("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC")
            ModeChif = int(input("Option :"))
            while ModeChif != 1 and ModeChif != 2:
                ModeChif = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))



            L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))
            while (L_block != 256) and (L_block != 512) and (L_block != 1024):
                L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))


            key = keygen(L_block)
            tabKey = keygenturn(key)

        if x == 2:
            print("Well Done !")

        if x == 3:
            print("Well Done !")

    elif x == 4:
        print("Well Done !")
    elif x == 5:
        print("Well Done !")

    elif x == 6:
        print("Well Done !")