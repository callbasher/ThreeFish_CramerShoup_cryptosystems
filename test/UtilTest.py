import pytest
import os
import sys
from random import *

sys.path.append('C:/Users/aurélien/Google Drive/Cours UTT/STIC_3_SSI/CS_GS15_Chiffrement, signature électronique et PKI/Projet/Projet_Cryptologie/src')

from src.Util import *
from src.ThreeFish import *

# test de la fonction permute
def test_permute():
    list_test = [12, 26, 57, 89]
    list_test_permute = [89, 57, 26, 12]
    a = permute(list_test)
    assert a == list_test_permute

# test de la fonction mixcolumn
def test_mix():
    liste = [658, 7532]
    liste_mix = [8190, 4240139049169330174]
    liste_mix_fct = mixcolumn(liste)
    assert liste_mix == liste_mix_fct


def test_unmix():
    liste = list(range(10))
    mix1 = mixcolumn(liste)
    mix2 = inv_mixcolumn(mix1)
    print(mix2)
    assert mix2 == liste

def test_ajoutkey():
    liste1 = []
    liste2 = []
    for i in range(10):
        liste1.append(randint(0, 100))
        liste2.append(randint(0, 100))
    test1 = []
    for i in range(0, len(liste1)):
        test1.append((liste1[i] + liste2[i]) % 2**64)
    test_ftc = ajoutkey(liste1, liste2)
    assert test1 == test_ftc