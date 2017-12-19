#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.ThreeFish import *
from src.Cramer_Shoup import *
from src.Util import *


def show():


    bloc = 256
    lon = 64
    a = readfile("../test/resources/test.txt", lon, bloc)
    print("datafile = ", a)
    key = keygen(bloc)
    kk = keygenturn(key)
    print("20clés = ", kk)
    chiff = ECBchiffThreef(a, kk)
    print("dataECB = ", chiff)
    writefilelist("../test/resources/encrypt.txt", chiff)
    b = read_encryptedfile("../test/resources/encrypt.txt", lon, bloc)
    print("datafilelecture = ", b)
    dchiff = ECBdechiffThreef(b, kk)
    print("dataECBdchiff = ", dchiff)
    writefilelist("../test/resources/encrypt.txt", dchiff)



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
            print("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC")
            ModeChif = int(input("Option :"))
            while ModeChif != 1 and ModeChif != 2:
                ModeChif = int(input("Veuillez choisir votre mode de chiffrement : \n\t1. ECB\n\t2. CBC"))

            L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))
            while (L_block != 256) and (L_block != 512) and (L_block != 1024):
                L_block = int(input("Choisir la taille de bloc à utiliser pour le chiffrement (256/512/1024) : "))

            key = keygen(L_block)
            tabKey = keygenturn(key)

            fich = input("Veuillez entrer le chemin du fichier à chiffrer : ")
            fichier = readfile(fich, L_block)
            print(fichier)

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