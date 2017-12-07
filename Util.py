#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd

import random
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
        exp = int(exp / 2)
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
      for i in random.sample(range(2, min(n - 2, sys.maxsize)), min(n - 4, b)):
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
