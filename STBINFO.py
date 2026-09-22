# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Binomial answer pager; follow-up stats load one page at a time from STBINFO2.
import STCORE as c


def show_answer(n, p, event, answer, title, first_page=None, threshold=(1, 20), cache=None):
    cache = {} if cache is None else cache
    index = 0
    while True:
        if first_page is not None and index == 0:
            page = first_page
        else:
            target = index - (1 if first_page is not None else 0)
            page = c.call('STBINFO2', 'page', n, p, event, answer, threshold, cache, target)
            if page is None: return
        action = c.view(title, page)
        if action == 'exit': return
        if action == 'back':
            if index == 0: return
            index -= 1
        else: index += 1
