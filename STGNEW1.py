# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGNEW1 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S13':
        return STCORE.unpack_guide('Raw Data Summary\nLIST OF NUMBERS; MEAN MEDIAN SD\nn VALUES; SAMPLE SD USES n-1\nORDER DATA; MEDIANS OF HALVES; OMIT ODD CENTER\n1-VAR STATS L1\n1,2,3,4: MEAN=2.5; Q1=1.5; Q3=3.5\nDO NOT USE POPULATION SD FOR SAMPLE\nS14 S15 S16\nS13', field)

    if gid == 'S14':
        return STCORE.unpack_guide('Sample Variance\nVARIANCE s^2\nSUM SQUARED DISTANCES / (n-1)\nSUBTRACT MEAN; SQUARE; SUM; DIVIDE n-1\nSQUARE Sx FROM 1-VAR STATS\n1,2,3: s^2=1\nVARIANCE HAS SQUARED UNITS\nS13 S09\nS14', field)

    if gid == 'S15':
        return STCORE.unpack_guide('Midrange\nAVERAGE OF MIN AND MAX\n(MIN+MAX)/2\nADD EXTREMES; DIVIDE BY TWO\n1-VAR STATS minX,maxX\n2,4,10: MIDRANGE=6\nNOT THE MEDIAN OR MEAN\nS13\nS15', field)
    return None
