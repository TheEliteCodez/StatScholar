# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Counts, Venn regions and repeated selections; heavy code loads per group.
import STCORE as c


def all_probability(total,good,n,replaced):
    return c.call('STVENN1', 'all_probability', total, good, n, replaced)


def selection_session(total=None,good=None,model=None):
    return c.call('STVENN1', 'selection_session', total, good, model)


def selection_question():
    return c.call('STVENN1', 'selection_question')


def regions(total,a,b,both):
    return c.call('STVENN2', 'regions', total, a, b, both)


def venn_session():
    return c.call('STVENN2', 'venn_session')
