#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import SystemRandom

# Retrieve primes from the file containing all the primes until lower than 100 000
def get_primes():
    primes_100k = []
    prime_file = open("../data/primes.txt", "r")
    for line in prime_file:
        primes_100k.append(int(line))
    return primes_100k


primes = get_primes()


# function that calculate the PGCD between 2 ints
def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


# function that factorize an int
# n = int
# factors = list of prime factors
def factorize(n):
    factors = []
    i = 2
    while i <= n / i:
        while n % i == 0:
            factors.append(i)
            n /= i
        i += 1

    if n > 1:
        factors.append(int(n))
    return factors


# This function test if a number contains prime factor up to a threshold b
# This serves as a first check to know if a number is probably prime
def trial_division(n, b=1000):
    if n == 1:
        return True
    if n == 2:
        return False

    is_divisible = False
    for p in primes:
        if p > b:
            break
        if n % p == 0 and n != p:
            is_divisible = True
            break

    return is_divisible


# Rabin-Miller primality test, used in big prime number generation
def rabin_miller(n, t=7):
    is_prime = True
    if n < 6:
        return [not is_prime, not is_prime, is_prime, is_prime, not is_prime, is_prime][n]
    elif not n & 1:
        return not is_prime

    def check(a, s, r, n):
        x = pow(a, r, n)
        if x == 1:
            return is_prime
        for i in range(s-1):
            if x == n - 1:
                return is_prime
            x = pow(x, 2, n)
        return x == n-1

    # Find s and r such as n - 1 = 2^s * r
    s, r = 0, n - 1
    while r & 1:
        s = s + 1
        r = r >> 1

    rand = SystemRandom()
    for i in range(t):
        a = rand.randint(2, n-1)
        if not check(a, s, r, n):
            return not is_prime

    return is_prime


# This function returns a probable prime based on the success of Rabin-Miller primality test
# It serves to generate q in order to find a prime p such as p = 2 * r * q + 1
# Inputs:
#   k = bit length of the prime
#   b = number of primes to try for trial division
# Outputs:
#    n = a prime number on k bits
def probable_prime(k, b=1000):
    success = False
    n = 0
    rand = SystemRandom()
    while not success:
        divisible = True
        while divisible:
            # We force the first and last bits to be set to 1
            # Thus we can ensure to have an odd number on k bits
            n = int('1' + rand.getrandbits(k-2) + '1', 2)
            divisible = trial_division(n, b)

        if rabin_miller(n):
                success = True
    return n


# This function generates a safe prime p to the form p = 2 * r * q + 1
# Finding p = 2 * r * q is quicker than finding p = 2 * q + 1.
# Therefore we try to find a small r (<1000)  which is short enough to be quickly factorizable.
# Inputs :
#   k = number of bits
# Ouputs:
#   p = safe prime on k bits
#   q = big prime factor of p on k-1 bits
#   r = small residual integer
def safe_prime(k):
    success = False
    r, q, p = 0, 0, 0
    while not success:
        q = probable_prime(k - 1)
        # We try to find p = 2 * R * q + 1 1000 times and if it fails we change q
        for r in range(1, 1000):
            p = 2 * r * q + 1
            if (not trial_division(p)) and rabin_miller(p):
                success = True
                break

    return p, q, r
