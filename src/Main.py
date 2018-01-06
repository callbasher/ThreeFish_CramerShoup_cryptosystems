#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.Menu as Menu
import src.Util as Util
import src.ThreeFish as Tf


def main():
    key, keyuser = Tf.keygen(256)
    c = Util.cipher_key("pass", key)
    d = Util.decipher_key("pass", c)
    x = Menu.show()
    Menu.apply(x)


if __name__ == "__main__":
    x = 'y'
    while x == 'y' or x == 'Y':
        main()
        x = 'z'
        while x != 'y' and x != 'Y' and x != 'n' and x != 'N':
            x = input("Recommencer ? (y/n)")