# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGPROB4 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'P10':
        return STCORE.unpack_guide(
            'Test Mutually Exclusive\n'
            'CAN THESE OCCUR TOGETHER?\tQ016 DOG / CAT / BOTH\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'EXCLUSIVE IF P(BOTH)=0\n'
            'USE ENTER VALUES / SOLVE\n'
            'BOTH=.46: NOT EXCLUSIVE\tQ016: .6000,.4300,.8000,.6825 (dog GIVEN cat)\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SUPPLIED_SESSION'
            , field)

    if gid == 'P11':
        return STCORE.unpack_guide(
            'Test Independence\n'
            'ARE EVENTS INDEPENDENT?\tQ017 COMPOST / RECYCLE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'P(BOTH)=P(A)*P(B)\n'
            'USE ENTER VALUES / SOLVE\n'
            '.57*.69=.3933, NOT .46: NO\tQ017: .5700,.4600,.8000,.6667; exclusive NO; independent NO\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SUPPLIED_SESSION'
            , field)

    if gid == 'P12':
        return STCORE.unpack_guide(
            'Direct Intersection Counts\n'
            'AND / BOTH FROM COUNTS\tQ010 BOTH INTOXICATED\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'BOTH CELL / WHOLE TOTAL\n'
            'USE ENTER VALUES / SOLVE\n'
            '61/979=0.0623\tQ010: 61/979=.0623; whole total, not given group\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'TWO_WAY_SESSION'
            , field)
    return None
