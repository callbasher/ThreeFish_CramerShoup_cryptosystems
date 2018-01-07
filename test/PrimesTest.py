#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Primes import *


def test_find_generators():
    p = probable_prime(10, 1000)
    factors = factorize(p-1)

    a1 = find_generator(p, factors)

    print("p = {0}".format(p))
    print("alpha = {0}".format(a1))
    print("factors = {0}".format(factors))

    r = []
    w1 = []
    for i in range(1, p):
        w1.append(pow(a1, i, p))
        r.append(i)

    w1.sort()
    assert r == w1


def test_factorize():
    a = 60
    expected = [[2, 2], [3, 1], [5, 1]]
    fac = factorize(a)

    assert expected == fac
