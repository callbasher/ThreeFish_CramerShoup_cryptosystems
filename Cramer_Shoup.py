#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math
import random
import Primes
from Util import *

# Cette fonction teste si un nombre possède des facteurs premiers allant jusqu'à 500.
# C'est une manière rapide de vérifier si un nombre n'est pas premier pour la génération de grands nombres premiers.
def trial_division(n, B = 1000):
    if (n == 1):
        return True
    if(n == 2):
        return False

    isDivisible = False
    primes = Primes.primes()
    for p in primes:
        if p > B:
            break
        if n % p == 0 and n != p:
            isDivisible = True
            break

    return isDivisible

# Test de primalité de Fermat, utilisé dans la génération de nombres premiers très grands
def fermat_test(n, k):
    if(n == 2):
        return True
    isPrime = True
    for i in range(0, k):
        a = random.randint(2, n-2)
        x = powermod(a, n-1, n)
        if x != 1:
            isPrime = False
            break

    return isPrime

def probable_prime(k, B = 1000):
    success = False
    n = 0
    while not success:
        divisible = True
        while divisible:
            # generate a k-bit random odd number
            n = random.getrandbits(k) | 1
            divisible = trial_division(n, B)

        if rabin_miller(n):
                success = True

    return n

def safe_prime(k):
    success = False
    while not success:
        q = probable_prime(k-1)
        # We try to find p = 2 * R * q + 1 1000 times and if it fails we change q
        for r in range(1, 1000):
            p = 2*r*q + 1
            if not trial_division(p):
                success = rabin_miller(p)
                break

    return p

# Experimental
def Maurer_primeGen(k):

    if k<17:
        primes = Primes.primes()
        x = random.randrange(0, len(primes))
        return primes[x], 0, 0

    c = 0.1
    m = 20
    B = c * k*k
    r = 0.5

    if k > 2*m:
        while (k - (r*k)) < m:
            s = random.randrange(0, 1000) / 1000
            r = 2**(s-1)

    q, R, n = Maurer_primeGen(int(r * k) + 1)
    print(k, q, R , n)
    p = math.pow(2, k-1)
    Q = q << 1
    I = int(p / Q)

    success = False
    while not success:
        J = I+1
        K = I << 1
        R = random.randrange(J, K)
        n = Q*R + 1
        div = trial_division(n, B)
        print(div)
        if not div:
            a = random.randrange(2, n - 2)
            b = powermod(a, n-1, n)
            if b == 1:
                b = powermod(a, R << 1, n)
                d = pgcd(b-1, n)
                success = d == 1

    return q, R, n

def find_generator(p, q):
    factors = [2, q]
    b = 1
    while b == 1:
        x = random.randint(2, p)
        for i in range(0, 1):
            b = powermod(x, factors[i], p)
            if b != 1:
                break
    return b

def prime_and_generators(k):
    return 0
