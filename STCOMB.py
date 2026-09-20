# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Small combinatorics shared by dice, binomial and counting.

def factorial(n):
    if n < 0:
        return 0
    r = 1
    i = 2
    while i <= n:
        r *= i
        i += 1
    return r

def ncr(n, r):
    if n < 0 or r < 0 or r > n:
        return 0
    r = min(r, n - r)
    value = 1
    for i in range(1, r + 1):
        value = value * (n - r + i) // i
    return value

def npr(n, r):
    if n < 0 or r < 0 or r > n:
        return 0
    return factorial(n) // factorial(n - r)
