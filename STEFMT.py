# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Formatting and statistical display helpers, loaded only while needed.
from STEXACT import ratio, to_ratio, compare_exact


def fmt(x):
    try:
        if abs(x - int(x)) < 0.0000000001:
            return str(int(x))
    except:
        pass
    return str(round(x, 10))


def radd(a, b):
    return ratio(a[0]*b[1] + b[0]*a[1], a[1]*b[1])


def rmul(a, b):
    return ratio(a[0]*b[0], a[1]*b[1])


def rsum(values):
    total = (0, 1)
    for value in values:
        total = radd(total, value)
    return total


def number(value):
    if isinstance(value, tuple):
        return value[0]/value[1]
    return value


def fixed(value, places):
    if isinstance(value, tuple):
        a, b = value
        scaled, rem = divmod(abs(a)*10**places, b)
        if rem*2 >= b:
            scaled += 1
        sign = "-" if a < 0 and scaled else ""
        digits = str(scaled)
        while len(digits) <= places:
            digits = "0" + digits
        if places:
            return sign + digits[:-places] + "." + digits[-places:]
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


def answer_text(value, style="D", places=4):
    if isinstance(value, str):
        return value
    if style == "F":
        if isinstance(value, tuple):
            return str(value[0]) + "/" + str(value[1])
        return fmt(value) + " (APPROX)"
    if style == "P":
        value = rmul(value, (100, 1)) if isinstance(value, tuple) else value*100
        return fixed(value, places) + "%"
    return fixed(value, places)


def exact_sorted(values):
    ordered = []
    for value in values:
        i = len(ordered)
        while i > 0 and compare_exact(value, ordered[i-1]) < 0:
            i -= 1
        ordered.insert(i, value)
    return ordered


def range_relation(count, mean, variance):
    delta = radd(to_ratio(count), (-mean[0], mean[1]))
    if compare_exact(rmul(delta, delta), rmul((4, 1), variance)) <= 0: return 0
    return -1 if delta[0] < 0 else 1
