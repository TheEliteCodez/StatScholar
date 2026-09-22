# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Dice counting arithmetic.
import STCORE
from STCOMB import ncr


def solver_dice_space():
    n = STCORE.read_int('# DICE: ')
    STCORE.results('C02 DICE OUTCOMES', [('TOTAL', (6 ** n, 1))], ['6^' + str(n)])


def dice_sum_at_most(n, value):
    if value < n: return 0
    if value >= 6*n: return 6**n
    count = 0
    for j in range(min(n, (value-n)//6)+1):
        term = ncr(n,j) * ncr(value-6*j,n)
        count += -term if j % 2 else term
    return count


def dice_event_count(n, event, value=0):
    total = 6 ** n
    if event == '1':
        return total
    if event == '2':
        return dice_sum_at_most(n,value)-dice_sum_at_most(n,value-1)
    if event == '3':
        return dice_sum_at_most(n,value)
    if event == '4':
        return total-dice_sum_at_most(n,value-1)
    if event == '5':
        return total - 5 ** n
    if event == '6':
        if value < 0 or value > n:
            return 0
        return ncr(n, value) * 5 ** (n - value)
    if event == '7':
        return 5 ** n
    if event in ('8', '9'):
        return 3 ** n
    if event == '10':
        return total - 3 ** n
    if event == '11':
        return 6
    if event == '12':
        return 1
