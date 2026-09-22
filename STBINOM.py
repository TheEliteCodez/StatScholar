# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STBINOM - binomial solver dispatcher; heavy code loads per group.
import STCORE
from STBMATH import *


def solver_bin_exact():
    return STCORE.call('STBINOM1', 'solver_bin_exact')


def solver_bin_at_most():
    return STCORE.call('STBINOM1', 'solver_bin_at_most')


def solver_bin_less():
    return STCORE.call('STBINOM1', 'solver_bin_less')


def solver_bin_at_least():
    return STCORE.call('STBINOM1', 'solver_bin_at_least')


def solver_bin_more():
    return STCORE.call('STBINOM1', 'solver_bin_more')


def solver_bin_between():
    return STCORE.call('STBINOM1', 'solver_bin_between')


def solver_bin_mean_sd():
    return STCORE.call('STBINOM1', 'solver_bin_mean_sd')


def binomial_session(n=None, exact_p=None, first_action=None):
    return STCORE.call('STBINOM2', 'binomial_session', n, exact_p, first_action)


def binomial_method(n, p, event):
    return STCORE.call('STBINOM1', 'binomial_method', n, p, event)
