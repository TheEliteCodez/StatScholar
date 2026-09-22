# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Event input, guide unpacking and size input, loaded only while needed.
import STCORE


def event_input(binomial=False):
    key = STCORE.menu("BINOMIAL > EVENT" if binomial else "WHAT DOES IT ASK?", [("1", "EXACTLY ="), ("2", "AT MOST <="),
          ("3", "LESS THAN <"), ("4", "AT LEAST >="), ("5", "MORE THAN >"),
          ("6", "BETWEEN x AND y")] + ([("7", "AT LEAST ONE"), ("8", "NOT =")] if binomial else [("7", "NOT =")]), page_size=6)
    if key == "0": return None
    if binomial and key == "7": return ">=", (1, 1), 0
    if key == "8": key = "7"
    op = {"1": "=", "2": "<=", "3": "<", "4": ">=", "5": ">", "7": "!="}.get(key, "[]")
    a = STCORE.read_exact("VALUE / LOWER: ")
    b = 0
    if key == "6":
        b = STCORE.read_exact("UPPER: ")
        c = STCORE.menu("INCLUDE ENDPOINTS?", [("1", "BOTH [a,b]"), ("2", "NEITHER (a,b)"),
               ("3", "LOWER ONLY [a,b)"), ("4", "UPPER ONLY (a,b]")])
        op = {"1": "[]", "2": "()", "3": "[)", "4": "(]"}.get(c, "[]")
    return op, a, b


def unpack_guide(text, field=None):
    names = ("title", "recognize", "values", "byhand", "ti84",
             "example", "mistakes", "related", "solver")
    if field is not None:
        index = names.index(field)
        start = 0
        for i in range(index):
            start = text.find("\n", start) + 1
        end = text.find("\n", start)
        section = text[start:] if end < 0 else text[start:end]
        return section if index in (0, 8) else section.split("\t")
    fields = text.split("\n")
    result = {}
    for i in range(9):
        result[names[i]] = fields[i] if i in (0, 8) else fields[i].split("\t")
    return result


def read_size(prompt, maximum, minimum=1):
    while True:
        n = STCORE.read_int(prompt)
        if minimum <= n <= maximum:
            return n
        print("ENTER " + str(minimum) + ".." + str(maximum))
