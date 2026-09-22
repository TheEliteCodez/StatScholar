# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Exact-ratio input parsing and comparison core, loaded only while needed.

def gcd(a, b):
    a = abs(int(a))
    b = abs(int(b))
    while b != 0:
        a, b = b, a % b
    return a


def ratio(a, b=1):
    if b == 0:
        raise ValueError("ZERO DENOMINATOR")
    a, b = int(a), int(b)
    g = gcd(a, b)
    if b < 0:
        g = -g
    return (a//g, b//g)


def rdiv(a, b):
    return ratio(a[0]*b[1], a[1]*b[0])


def as_ratio(text):
    text = str(text).strip()
    if text.endswith("%"):
        a = as_ratio(text[:-1])
        return ratio(a[0], a[1]*100)
    if "/" in text:
        a, b = text.split("/")
        return rdiv(as_ratio(a), as_ratio(b))
    if "e" in text.lower():
        a, e = text.lower().split("e")
        a = as_ratio(a)
        e = int(e)
        if e >= 0:
            return ratio(a[0]*10**e, a[1])
        return ratio(a[0], a[1]*10**(-e))
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    if "." in text:
        whole, part = text.split(".")
        return ratio(sign*int((whole or "0")+part), 10**len(part))
    return ratio(sign*int(text))


def to_ratio(value):
    if isinstance(value, tuple): return value
    if isinstance(value, int): return (value, 1)
    return as_ratio(str(value))


def compare_exact(a, b):
    a = to_ratio(a); b = to_ratio(b)
    delta = a[0]*b[1] - b[0]*a[1]
    return (delta > 0) - (delta < 0)


def event_match(x, op, a, b=0):
    left = compare_exact(x, a)
    if op == "=": return left == 0
    if op == "<": return left < 0
    if op == "<=": return left <= 0
    if op == ">": return left > 0
    if op == ">=": return left >= 0
    if op == "!=": return left != 0
    right = compare_exact(x, b)
    if op == "[]": return left >= 0 and right <= 0
    if op == "()": return left > 0 and right < 0
    if op == "[)": return left >= 0 and right < 0
    return left > 0 and right <= 0


def read_exact(prompt):
    while True:
        try:
            return as_ratio(input(prompt))
        except (ValueError, ZeroDivisionError):
            print("USE NUMBER, A/B OR %")
