# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Shared exact arithmetic for the binomial follow-up pages.

def gcd(a, b):
    a = abs(int(a)); b = abs(int(b))
    while b:
        a, b = b, a % b
    return a


def ratio(a, b=1):
    if b == 0:
        raise ValueError("ZERO DENOMINATOR")
    a, b = int(a), int(b)
    g = gcd(a, b)
    if b < 0: g = -g
    return (a//g, b//g)


def to_ratio(value):
    if isinstance(value, tuple): return value
    if isinstance(value, int): return (value, 1)
    return value


def compare_exact(a, b):
    a = to_ratio(a); b = to_ratio(b)
    delta = a[0]*b[1] - b[0]*a[1]
    return (delta > 0) - (delta < 0)


def radd(a, b):
    return ratio(a[0]*b[1] + b[0]*a[1], a[1]*b[1])


def rmul(a, b):
    return ratio(a[0]*b[0], a[1]*b[1])


def number(value):
    return value[0]/value[1] if isinstance(value, tuple) else value


def range_relation(count, mean, variance):
    delta = radd(to_ratio(count), (-mean[0], mean[1]))
    if compare_exact(rmul(delta, delta), rmul((4, 1), variance)) <= 0: return 0
    return -1 if delta[0] < 0 else 1


def fixed(value, places):
    if isinstance(value, tuple):
        a, b = value
        scaled, rem = divmod(abs(a)*10**places, b)
        if rem*2 >= b: scaled += 1
        sign = "-" if a < 0 and scaled else ""
        digits = str(scaled)
        while len(digits) <= places: digits = "0" + digits
        if places: return sign + digits[:-places] + "." + digits[-places:]
        return sign + digits
    return ("%.*f" % (places, value))


def exact_text(value):
    a, b = to_ratio(value)
    if b == 1: return str(a)
    tail = b; twos = 0; fives = 0
    while tail % 2 == 0: tail //= 2; twos += 1
    while tail % 5 == 0: tail //= 5; fives += 1
    if tail == 1: return fixed((a, b), max(twos, fives))
    return str(a) + "/" + str(b)
