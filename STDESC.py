# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STDESC - descriptive solver dispatcher; heavy code loads per group.
import STCORE


def solver_rel_freq():
    return STCORE.call('STDESC1', 'solver_rel_freq')


def solver_range_iqr():
    return STCORE.call('STDESC1', 'solver_range_iqr')


def solver_usual():
    return STCORE.call('STDESC1', 'solver_usual')


def solver_zscore():
    return STCORE.call('STDESC1', 'solver_zscore')


def solver_outlier():
    return STCORE.call('STDESC1', 'solver_outlier')


def frequency_stats(rows):
    return STCORE.call('STDESC2', 'frequency_stats', rows)


def frequency_session(rows=None):
    return STCORE.call('STDESC2', 'frequency_session', rows)
