# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN5 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'B13':
        return STCORE.unpack_guide(
            'Binomial Usual Counts\n'
            'RANGE RULE; FIRST UNUSUAL\tQ034 CHICKENPOX 123 ADULTS\tQ047 47 DAYS FORGET LUNCH\tQ049 ON-TIME BUSES\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'mu=np; SD=SQRT(np(1-p))\tUSUAL: mu +/- 2 SD\tINTEGERS: CEIL LOW, FLOOR HIGH\tFIRST HIGH=FLOOR(HIGH)+1\tEXACT TAIL: SUM BINOMIAL P\n'
            'USE ENTER VALUES / SOLVE\n'
            '47,.387: FIRST HIGH=25\tQ034: mu=110.7000; SD=3.3272; 100 unusually low; P(100)=.0013\tQ047: mu=18.189; SD=3.33914016; first high=25; P(>=25)=.03071365753; part a labels missing\tQ049: n MISSING; p=.64; mu=.64n; SD=.48sqrt(n); integer range then exact tails\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'BINOMIAL_SESSION'
            , field)
    raise KeyError(gid)
    return None
