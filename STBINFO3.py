# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Test/support wrappers over STBINFO2.page; never loaded on the device.
import STCORE
from STBINFO2 import page


def report_pages(n, p, event=None, answer=None, threshold=(1, 20), cache=None):
    cache = {} if cache is None else cache
    target = 0
    while True:
        pg = page(n, p, event, answer, threshold, cache, target)
        if pg is None: return
        yield pg
        target += 1


def append_page(lines, page):
    count = sum(1 for line in STCORE.wrapped_lines(page))
    lines.extend(page)
    lines.extend(['']*((-count) % STCORE.VIEW_LINES))


def followup(n, p, event, answer, threshold=(1, 20)):
    lines = []
    for pg in report_pages(n, p, event, answer, threshold):
        append_page(lines, pg)
    return lines
