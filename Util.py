#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd

from random import randrange, getrandbits, sample
import sys

def pgcd(a, b):
    # calcul recursif du pgcd de a et b
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def powermod(a, exp, mod):
    resultat = 1
    while exp > 0:
        if exp % 2 == 1:
            resultat = (resultat * a) % mod
        exp >>= 1
        a = (a * a) % mod
    return resultat

# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_miller(n, b = 7):
   if n < 6:
      return [False, False, True, True, False, True][n]
   elif n & 1 == 0:
      return False
   else:
      s, p = 0, n - 1
      while p & 1 == 0:
         s, p = s + 1, p >> 1
      for i in sample(range(2, min(n - 2, sys.maxsize)), min(n - 4, b)):
         c = pow(i, p, n)
         if c != 1 and c + 1 != n:
            for r in range(1, s):
               c = pow(c, 2, n)
               if c == 1:
                  return False
               elif c == n - 1:
                  i = 0
                  break
            if i:
               return False
      return True

# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_millerv2(n, t = 7):
    isPrime = True
    if n < 6:
        return [not isPrime, not isPrime, isPrime, isPrime, not isPrime, isPrime][n]
    elif not n & 1:
        return not isPrime

    def check(a, s, r, n):
        x = pow(a, r, n)
        if x == 1:
            return isPrime
        for i in xrange(s-1):
            if x == n - 1:
                return isPrime
            x = pow(x, 2, n)
        return x == n-1

    # Find s and r such as n - 1 = 2^s * r
    s, r = 0, n - 1
    while r & 1:
        s = s + 1
        r = r >> 1

    for i in xrange(t):
        a = randrange(2, n-1)
        if not check(a, s, r, n):
            return not isPrime

    return isPrime
