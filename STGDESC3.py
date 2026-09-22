# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC3 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'F03':
        return STCORE.unpack_guide(
            'Cumulative Frequency\n'
            'TYPICAL START:\t"COMPLETE THE CUMULATIVE\tFREQUENCY COLUMN."\t\tWORD CUE:\tCUMULATIVE = RUNNING TOTAL.\n'
            'YOU NEED:\tTHE FREQUENCY IN EACH ROW.\t\tLAST CUMULATIVE FREQUENCY\tSHOULD EQUAL TOTAL n.\n'
            '1. FIRST CUM = FIRST f.\t2. NEXT = PREVIOUS CUM\t   + CURRENT f.\t3. KEEP RUNNING DOWN TABLE.\n'
            'USE + TO CHECK TOTALS.\n'
            'FREQUENCIES: 4,6,3.\tCUMULATIVE:\t4\t4+6=10\t10+3=13.\n'
            'DO NOT START OVER EACH ROW.\tYOU KEEP ALL PREVIOUS\tFREQUENCIES.\n'
            'F01 FREQUENCY\tF02 REL FREQ\n'
            'FREQUENCY_SESSION'
            , field)

    if gid == 'F04':
        return STCORE.unpack_guide(
            'Sample Proportion / Percent\n'
            'TYPICAL START:\t"WHAT PROPORTION OF\tSTUDENTS..."\t"WHAT PERCENT..."\t"HOW MANY OUT OF THE SAMPLE"\n'
            'PART = COUNT MEETING CONDITION.\tWHOLE = TOTAL SAMPLE SIZE.\t\tPROPORTION=PART/WHOLE.\tPERCENT=PROPORTION*100.\n'
            '1. COUNT WHO MEET CONDITION.\t2. FIND TOTAL n.\t3. DIVIDE PART/n.\t4. *100 IF PERCENT.\n'
            'TYPE PART/n ENTER.\tOR USE REL FREQ SOLVER.\n'
            'COMMUTE GROUP:\t22 OF 80 >10 MILES.\t22/80=.275\t=27.5%.\n'
            'THIS IS DESCRIBING OBSERVED\tDATA, NOT AUTOMATICALLY\tA BINOMIAL PROBABILITY.\n'
            'F02 REL FREQ\tP01 BASIC PROB\n'
            'REL_FREQ'
            , field)

    if gid == 'S01':
        return STCORE.unpack_guide(
            'Mean from Raw Data\n'
            'TYPICAL START:\t"FOR THE DATA SHOWN, FIND\tTHE MEAN..."\t"FIND x-bar..."\t\tYOU SEE A LIST/COLUMN\tOF NUMBERS.\n'
            'x values = RAW DATA.\tn = NUMBER OF VALUES.\t\txbar = SAMPLE MEAN.\n'
            'BY HAND:\t1. ADD ALL x VALUES.\t2. COUNT VALUES n.\t3. xbar=SUM(x)/n.\t\tFOR LONG LIST, USE EVO.\n'
            'STAT > EDIT.\tENTER DATA IN L1.\tSTAT > CALC.\t1-VAR STATS.\tLIST=L1.\tREAD xbar.\n'
            'COMMUTE DATA:\t16 VALUES.\t1-VAR STATS GAVE\txbar=11.5625.\n'
            'DO NOT USE MEDIAN.\tDO NOT DIVIDE BY WRONG n.\tCLEAR OLD L1 DATA FIRST.\n'
            'S02 MEDIAN\tS09 SD\tS05 FIVE NUMBER\tF05 MEAN WITH FREQUENCIES\n'
            ''
            , field)
    return None
