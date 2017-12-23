import pytest
import os
import sys
#sys.path.append('/home/dev/Documents/Projet_Cryptologie/src')
from random import *
sys.path.append('C:/Users/aurélien/Google Drive/Cours UTT/STIC_3_SSI/CS_GS15_Chiffrement, signature électronique et PKI/Projet/Projet_Cryptologie/src')
from random import *
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
    liste = [6869182828364843105, 5685451262666598955, 6869182828364843105, 5685451262666598955]
    liste_mix = [12554634091031442060, 14834149863215961599, 12554634091031442060, 14834149863215961599]
    liste_mix_fct = mixcolumn(liste)
    assert liste_mix == liste_mix_fct


def test_unmix():
    liste = [6869182828364843105, 14834149863215961599, 6869182828364843105, 5685451262666598955]
    mix = mixcolumn(liste)
    unmix = inv_mixcolumn(mix)
    assert unmix == liste

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

def test_inv_ajoutkey():
    liste1 = []
    liste2 = []
    for i in range(10):
        liste1.append(randint(0, 100))
        liste2.append(randint(0, 100))
    a = ajoutkey(liste1, liste2)
    b = inv_ajoutkey(a, liste2)
    assert b == liste1

def test_inv_ECB():
    liste1 = [[18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61]]
    liste2keys = [[654, 5, 54, 54], [654, 654, 654, 5], [65, 54, 54, 54], [54, 54, 654, 654], [987, 987, 84, 84], [6884, 684, 654, 64], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [6551, 61, 51, 51], [561, 651, 651, 61]]
    a = ECBchiffThreef(liste1, liste2keys)
    b = ECBdechiffThreef(a, liste2keys)
    assert liste1 == b

def test_ROTD_ROTG():
    a = "1101111101011110011001001110111011001111000101101011100110000010"
    x = strToInt(a)
    for i in range(76):
        b = ROTD(a)
    b = intToByteArray(b)
    for i in range(76):
        c = ROTG(b)
    assert str(c) == str(x)

def test_xor_function():
    a = "0101111101011110011001001110111011001111000101101011100110000010"
    b = "1101111101011110011001001110111011001111000101101011100110000010"
    c = "1000000000000000000000000000000000000000000000000000000000000000"
    assert xor_function(a, b) == c

def test_addition_function():
    a = "0000100100101001001101101011100111110111001111001110001100110110"
    b = "1000010100111111100100111001011000011011110011001011101010000001"
    c = "1000111001101000110010100101000000010011000010011001110110110111"
    assert additionMod(a, b) == c

def test_soustraction_function():
    a = "0000100100101001001101101011100111110111001111001110001100110110"
    b = "1000010100111111100100111001011000011011110011001011101010000001"
    c = "1000111001101000110010100101000000010011000010011001110110110111"
    assert soustracMod(c, b) == a

def test_int2byte():
    a = 6869182828364843105
    b = 6869182828364843105
    output = []
    output1 = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, a & mask)
        a >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        output1.append(i)
    p = "".join(output1)
    p = str(p)
    assert p == intToByteArray(b)
