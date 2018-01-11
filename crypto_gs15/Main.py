#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Menu


def main():
    x = Menu.show()
    Menu.apply(x)


if __name__ == "__main__":
    x = 'y'
    while x == 'y' or x == 'Y':
        main()
        x = 'z'
        while x != 'y' and x != 'Y' and x != 'n' and x != 'N':
            x = input("Recommencer ? (y/n) ")
