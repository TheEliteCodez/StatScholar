# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN4 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'B10':
        return STCORE.unpack_guide(
            'Binomial Between a and b\n'
            'TYPICAL START:\t"BETWEEN 3 AND 6\tINCLUSIVE"\t"3<=X<=6"\n'
            'a = LOW END.\tb = HIGH END.\t\tCDF(b) HAS 0..b.\tSUBTRACT CDF(a-1).\n'
            '1. IDENTIFY a,b.\t2. COMPUTE CDF(b).\t3. COMPUTE CDF(a-1).\t4. SUBTRACT.\n'
            'binomcdf(n,p,b)\t-binomcdf(n,p,a-1).\n'
            'P(3<=X<=6)=\tCDF(6)-CDF(2).\n'
            'CHECK WHETHER ENDPOINTS\tARE INCLUDED.\tSTRICTLY BETWEEN CHANGES\tTHE LIMITS.\n'
            'B03 AT MOST\tB04 LESS THAN\n'
            'BINOMIAL_SESSION'
            , field)

    if gid == 'B11':
        return STCORE.unpack_guide(
            'Full Binomial Distribution\n'
            'LIST X AND P(X) FOR TRIALS\tQ035 THREE FLIPS COUNT HEADS\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'X=0..n; P=nCx*p^x*(1-p)^(n-x)\n'
            'USE ENTER VALUES / SOLVE\n'
            '3 FAIR FLIPS: 1,3,3,1 OVER 8\tQ035: 1/8,3/8,3/8,1/8; symmetric; mu=1.500 heads; sigma=.866; P(<=2)=7/8\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'BINOMIAL_SESSION'
            , field)

    if gid == 'B12':
        return STCORE.unpack_guide(
            'Binomial Shape and Symmetry\n'
            'MATCH GRAPH TO p; SYMMETRY\tQ033 BINOMIAL TAIL SYMMETRY?\tQ042 MATCH THREE HISTOGRAMS\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'GRAPH CENTER=np\tREFLECTED TAILS MATCH IF p=.5\tFIXED n DOES NOT FIX p\tUSE COMPARE TAILS FOR EQUALITY\n'
            'USE ENTER VALUES / SOLVE\n'
            'n=10,p=.35: CENTER=3.5\tQ033: FALSE generally; matching opposite tails requires p=.5\tQ042: n=10; top-to-bottom p=.35,.25,.20; centers=3.5,2.5,2\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SHAPE_TASKS'
            , field)
    return None
