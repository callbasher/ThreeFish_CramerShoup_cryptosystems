#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom
from src.Util import *


def find_generator(p, factors):
    b = 1
    while b == 1:
        x = SystemRandom.choice(2, p)
        for f in factors:
            b = pow(x, (p-1) / f, p)
            if b != 1:
                break
    return b

def prime_and_generators(k):
    p, q, r = safe_prime(k)
    # prime factors of p-1
    # we want only the different prime factors not their exponent so we remove duplicates
    # We put q at the end of the list to ensure that smaller factors are tried first
    # in "find_generator" function
    factors = set(factorize(r))
    factors.add(2)
    factors = list(factors)
    factors.append(q)

    alpha1 = find_generator(p, factors)
    alpha2 = alpha1
    while alpha1 == alpha2:
        alpha2 = find_generator(p, factors)

    return p, alpha1, alpha2


def generate_publicKey(k):
    p, g1, g2 = prime_and_generators(k)

    Zp = range(2, p)
    x1 = SystemRandom.choice(Zp)
    x2 = SystemRandom.choice(Zp)
    y1 = SystemRandom.choice(Zp)
    y2 = SystemRandom.choice(Zp)
    w = SystemRandom.choice(Zp)

    X = pow(g1, x1, p) * pow(g2, x2, p)
    Y = pow(g1, y1, p) * pow(g2, y2, p)
    W = pow(g1, w, p)

    private_key = {x1, x2, y1, y2, w}
    public_key = {p, g1, g2, X, Y, W}

    writefile("public_key.txt", public_key)

    return private_key, public_key

