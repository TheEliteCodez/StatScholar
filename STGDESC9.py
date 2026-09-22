# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC9 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'F06':
        return STCORE.unpack_guide(
            'Median from Frequency Table\n'
            'FREQUENCY TABLE; MEDIAN\tQ002 RAIN: MEDIAN AND MODE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ORDER VALUES LOW TO HIGH\tn=SUM(FREQUENCIES)\tODD: POSITION (n+1)/2\tEVEN: n/2 AND n/2+1\tLOCATE VIA CUMULATIVE f\tAVERAGE THOSE TWO VALUES\n'
            'USE ENTER VALUES / SOLVE\n'
            'n=20: POS 10 AND 11 BOTH 7\tQ002: n=20; positions 10,11=7; mode=7\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)

    if gid == 'F07':
        return STCORE.unpack_guide(
            'Mode from Frequency Table\n'
            'FREQUENCY TABLE; MODE\tQ002 RAIN: MEDIAN AND MODE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'VALUE WITH GREATEST COUNT\n'
            'USE ENTER VALUES / SOLVE\n'
            '6 HAS f=5; 7 HAS f=6: MODE 7\tQ002: n=20; positions 10,11=7; mode=7\n'
            'REPORT VALUE, NOT FREQUENCY\tCOMBINE REPEATED VALUE ROWS\tIGNORE ZERO FREQUENCIES\tASSIGNMENT: >2 MODES -> DNE\tALL EQUAL COUNTS -> NO MODE\tONE DISTINCT VALUE: ITS MODE\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)
    raise KeyError(gid)
    return None
