# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STDATA - data solver dispatcher; heavy code loads per session type.
import STCORE


def summary_results(stats, title='DATA > RAW > SUMMARY', population=False):
    return STCORE.call('STDATA1', 'summary_results', stats, title, population)


def data_normal(stats, first, population=False):
    return STCORE.call('STDATA1', 'data_normal', stats, first, population)


def choose_population(population):
    return STCORE.call('STDATA1', 'choose_population', population)


def raw_session(values=None):
    return STCORE.call('STDATA2', 'raw_session', values)


def comparison(a, b):
    return STCORE.call('STDATA2', 'comparison', a, b)


def compare_session(a=None, boxes=False):
    return STCORE.call('STDATA3', 'compare_session', a, boxes)


def frequency_data_session():
    return STCORE.call('STDATA3', 'frequency_data_session')
