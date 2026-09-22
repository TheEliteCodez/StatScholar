# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Histogram-heights and table-check pages for the distribution task loop.
import STCORE as c


def heights_page(rows, approximate):
    c.paged_results('APPROXIMATE HEIGHTS' if approximate else 'PROBABILITY HISTOGRAM',len(rows),lambda i:('x='+c.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=P(X)', 'INCLUDE EVERY X, INCLUDING ZERO', 'NUMERIC x AXIS; PROBABILITY y AXIS', 'APPROXIMATE HEIGHTS: ROUNDED TABLE' if approximate else 'USE EQUAL-WIDTH BARS'])


def check_table(rows, note, approximate):
    valid = all((c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0 for x, p in rows)) and c.rsum([p for x, p in rows]) == (1, 1)
    lines = note + ['VALID=' + ('UNKNOWN (ROUNDED)' if approximate else str(valid))]
    lines += [c.exact_text(x) + ': ' + c.answer_text(p, 'F') for x, p in rows]
    c.view('R01 TABLE', lines)
