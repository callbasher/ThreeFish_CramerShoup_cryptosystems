#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.ThreeFish import *
from src.Cramer_Shoup import *
from src.Util import *


def show():
    print("\nArnaud FOURNIER, Aurélien DIAS\n")
    print("\t\t\tProjet GS15 - A17 - ThreeFish - CramerShoup")
    print("\nMenu :\n")
    print(
        "\t1. Chiffrement symétrique ThreeFish\n\t"
        "2. Chiffrement de Cramer-Shoup\n\t"
        "3. Hashage d'un message\n\t"
        "4. Déchiffrement sysmétrique ThreeFish\n\t"
        "5. Déchiffrement Cramer-Shoup\n\t6. Vérification d'un hash")
    x = int(input("Option : "))
    while x < 0 or x > 6:
        x = int(input("Option : "))

    return x


def apply(x):
    if x < 4:
        if x == 1:
            threefish_chiffrement()

        if x == 2:
            print("Well Done !")

        if x == 3:
            print("Well Done !")

    elif x == 4:
        threefish_dechiffrement()
    elif x == 5:
        print("Well Done !")

    elif x == 6:
        print("Well Done !")
