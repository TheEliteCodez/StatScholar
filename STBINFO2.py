# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Follow-up page dispatcher; pages live in small transient modules.
import STCORE as c


def usual_counts(n, p):
    return c.call('STBINFO4', 'usual_counts', n, p)


def binomial_quartiles(n, p):
    return c.call('STBINFO4', 'binomial_quartiles', n, p)


def page(n, p, event, answer, threshold, cache, target):
    if target < 2:
        return c.call('STBINFO5', 'page', n, p, event, answer, threshold, cache, target)
    if target == 2:
        return c.call('STBINFO6', 'page', n, p, event, answer, threshold, cache, target)
    return c.call('STBINFO7', 'page', n, p, event, answer, threshold, cache, target)
