# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Counting basics: sample space, nCr, nPr.
import STCORE as c
from STCOMB import ncr, npr


def solver_sample_space():
    stages = c.read_int('# STAGES: ')
    total = 1
    work = []
    for i in range(stages):
        choices = c.read_int('CHOICES ' + str(i + 1) + ': ')
        total *= choices
        work.append('STAGE ' + str(i + 1) + '=' + str(choices))
    c.results('C01 SAMPLE SPACE', [('TOTAL', (total, 1))], ['MULTIPLY CHOICES'] + work)


def solver_ncr():
    n = c.read_int('n: ')
    r = c.read_int('r: ')
    c.results('C03', [('ANSWER', (ncr(n, r), 1))], [str(n) + ' ncr ' + str(r)])


def solver_npr():
    n = c.read_int('n: ')
    r = c.read_int('r: ')
    c.results('C04', [('ANSWER', (npr(n, r), 1))], [str(n) + ' npr ' + str(r)])


def solver_expected():
    c.call('STCOUNT', 'distribution_session')
