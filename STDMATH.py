# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STDMATH - loaded only when needed.
import STCORE
RAW_LIMIT = 100  # Desktop tested; physical Evo limit pending.


def sub(a, b):
    return STCORE.call('STDMATH1', 'sub', a, b)


def read_raw(title='DATA > RAW'):
    return STCORE.call('STDMATH1', 'read_raw', title)


def median_span(values, start, end):
    return STCORE.call('STDMATH1', 'median_span', values, start, end)


def quartiles(values):
    return STCORE.call('STDMATH1', 'quartiles', values)


def descriptive(values):
    return STCORE.call('STDMATH1', 'descriptive', values)


def weighted_stats(rows):
    return STCORE.call('STDMATH2', 'weighted_stats', rows)


def edit_raw(values):
    return STCORE.call('STDMATH3', 'edit_raw', values)


def edit_frequency(rows):
    return STCORE.call('STDMATH3', 'edit_frequency', rows)


def min_exact(a,b):
    return STCORE.call('STDMATH1', 'min_exact', a, b)


def max_exact(a,b):
    return STCORE.call('STDMATH1', 'max_exact', a, b)


def value_counts(values):
    return STCORE.call('STDMATH1', 'value_counts', values)


def read_frequency_rows():
    return STCORE.call('STDMATH3', 'read_frequency_rows')


def probe_summary(size):
    return STCORE.call('STDMATH3', 'probe_summary', size)
