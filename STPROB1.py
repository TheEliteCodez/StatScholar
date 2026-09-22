# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Basic/complement/OR/AND/conditional/at-least-one solvers.
import STCORE as c


def solver_basic_prob():
    c.heading('P01 BASIC PROBABILITY')
    print('FAVORABLE = THE OUTCOMES THAT COUNT')
    print('TOTAL = ALL POSSIBLE OUTCOMES')
    a = c.read_int('FAVORABLE OUTCOMES: ')
    b = c.read_int('TOTAL OUTCOMES: ')
    c.results('P01 BASIC PROBABILITY', [('P', c.ratio(a, b))], ['P=FAVORABLE/TOTAL', str(a) + '/' + str(b)])


def solver_complement():
    p = c.read_exact('P(E): ')
    c.results('P02 COMPLEMENT', [('P(NOT E)', c.radd((1, 1), (-p[0], p[1])))], ['1-' + c.exact_text(p)])


def solver_general_or():
    a = c.read_exact('P(A): ')
    b = c.read_exact('P(B): ')
    both = c.read_exact('P(BOTH): ')
    c.results('P04 OR', [('P(OR)', c.radd(c.radd(a, b), (-both[0], both[1])))], [c.exact_text(a) + '+' + c.exact_text(b) + '-' + c.exact_text(both)])


def solver_mut_or():
    a = c.read_exact('P(A): ')
    b = c.read_exact('P(B): ')
    c.results('P03 EXCLUSIVE OR', [('P(OR)', c.radd(a, b))], ['MUTUALLY EXCLUSIVE: BOTH=0', c.exact_text(a) + '+' + c.exact_text(b)])


def solver_indep_and():
    a = c.read_exact('P(A): ')
    b = c.read_exact('P(B): ')
    c.results('P05 INDEPENDENT AND', [('P(BOTH)', c.rmul(a, b))], ['INDEPENDENT EVENTS', c.exact_text(a) + '*' + c.exact_text(b)])


def solver_general_and():
    a = c.read_exact('P(A): ')
    bg = c.read_exact('P(B GIVEN A): ')
    c.results('P06 GENERAL AND', [('P(BOTH)', c.rmul(a, bg))], ['P(A)*P(B GIVEN A)', c.exact_text(a) + '*' + c.exact_text(bg)])


def solver_conditional():
    k = c.menu('P07 CONDITIONAL', [('1', 'PROBABILITIES'), ('2', 'COUNTS FROM TABLE')])
    if k == '0':
        return
    both = c.read_exact('BOTH A AND B: ')
    given = c.read_exact('GIVEN GROUP B TOTAL: ')
    c.results('P07 GIVEN', [('P(A GIVEN B)', c.rdiv(both, given))], ['BOTH / GIVEN GROUP', c.exact_text(both) + ' / ' + c.exact_text(given)])


def solver_at_least_one():
    p = c.read_exact('SUCCESS p: ')
    n = c.read_int('TRIALS n: ')
    ans = c.ratio(p[1] ** n - (p[1] - p[0]) ** n, p[1] ** n)
    c.results('P09 AT LEAST ONE', [('P', ans)], ['1-(1-' + c.exact_text(p) + ')^' + str(n)])
