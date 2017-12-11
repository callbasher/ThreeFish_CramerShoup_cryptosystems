import pytest
import binascii
from src.Util import *

# test lecture fichier
def read_txt_file():
    L_block = 256
    fich = "resources/test.txt"
    fichier = readfile(fich, L_block)
    print(fichier)