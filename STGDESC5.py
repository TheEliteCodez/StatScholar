# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC5 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S05':
        return STCORE.unpack_guide(
            'Five-Number Summary\n'
            'TYPICAL START:\t"FIND THE FIVE-NUMBER\tSUMMARY."\tOR NEEDS VALUES FOR BOXPLOT.\n'
            'FIVE VALUES:\tMIN\tQ1\tMEDIAN\tQ3\tMAX\n'
            'BY HAND REQUIRES ORDERING\tDATA AND FINDING QUARTILES.\tON TEST, EVO IS FASTER.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tSCROLL TO:\tminX,Q1,Med,Q3,maxX.\n'
            'COMMUTE:\t2, 5.5, 10.5, 16.5, 29.\n'
            'DO NOT INCLUDE MEAN.\tFIVE-NUMBER SUMMARY DOES\tNOT CONTAIN xbar.\n'
            'S06 Q1\tS07 Q3\tG01 BOXPLOT\n'
            ''
            , field)

    if gid == 'S06':
        return STCORE.unpack_guide(
            'First Quartile Q1\n'
            'TYPICAL START:\t"UNDER WHAT DISTANCE DO\tTHE SHORTEST 25%..."\t"FIND Q1."\t"25TH PERCENTILE."\n'
            'Q1 = FIRST QUARTILE.\tIT MARKS ABOUT LOWEST 25%.\t\t25% -> Q1.\t50% -> MEDIAN.\t75% -> Q3.\n'
            '1. RECOGNIZE 25% -> Q1.\t2. ENTER RAW DATA IF GIVEN.\t3. RUN 1-VAR STATS.\t4. READ Q1.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tREAD Q1.\n'
            'COMMUTE QUESTION:\t"UNDER WHAT DISTANCE DO\tSHORTEST 25% TRAVEL?"\tQ1=5.5 MILES.\n'
            'WRONG: .25*MAX.\tQ1 IS A LOCATION IN\tORDERED DATA.\n'
            'S02 MEDIAN\tS07 Q3\tS08 IQR\n'
            ''
            , field)

    if gid == 'S07':
        return STCORE.unpack_guide(
            'Third Quartile Q3\n'
            'TYPICAL START:\t"FIND Q3."\t"75TH PERCENTILE."\t"75% ARE BELOW WHAT VALUE?"\n'
            'Q3 = THIRD QUARTILE.\tABOUT 75% OF DATA IS\tAT OR BELOW THIS REGION.\n'
            '1. RECOGNIZE 75% -> Q3.\t2. ENTER DATA L1.\t3. RUN 1-VAR STATS.\t4. READ Q3.\n'
            'STAT > EDIT -> L1.\t1-VAR STATS -> Q3.\n'
            'COMMUTE Q3=16.5.\n'
            'WRONG: .75*MAX.\tQ3 IS A DATA POSITION.\n'
            'S06 Q1\tS08 IQR\n'
            ''
            , field)
    return None
