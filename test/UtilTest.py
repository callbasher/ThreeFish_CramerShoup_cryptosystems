from sys import path
from src.Util import *

path.append('C:/Users/aurélien/Google Drive/Cours UTT/STIC_3_SSI/CS_GS15_Chiffrement, signature électronique et PKI/Projet/Projet_Cryptologie/src')

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

def test_xor2list():
    liste1 = [18, 24, 52, 96]
    liste2 = [18, 24, 52, 96]
    result = xor_2_lists(liste1, liste2)
    m = [0, 0, 0, 0]
    begin = xor_2_lists(m, liste2)
    assert m == result
    assert begin == liste1
