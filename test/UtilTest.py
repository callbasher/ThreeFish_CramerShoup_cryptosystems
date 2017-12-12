import pytest
import binascii
import os
import sys
sys.path.append('/home/dev/Documents/Projet_Cryptologie/src')
from src.Util import *

# test lecture fichier
def read_txt_file():
    L_block = 256
    fich = "resources/test.txt"
    fichier = readfile(fich, L_block)
    print(fichier)