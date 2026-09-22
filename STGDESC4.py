# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC4 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S02':
        return STCORE.unpack_guide(
            'Median / Half\n'
            'TYPICAL START:\t"FIND THE MEDIAN."\t"HALF OF STUDENTS TRAVEL\tUNDER WHAT DISTANCE?"\t"50TH PERCENTILE"\n'
            'MEDIAN = MIDDLE OF\tORDERED DATA.\t\tEVEN n:\tAVERAGE TWO MIDDLE VALUES.\n'
            '1. ORDER LOW TO HIGH.\t2. FIND MIDDLE.\t3. IF TWO MIDDLE VALUES,\t   ADD THEM /2.\n'
            '1-VAR STATS.\tREAD Med.\n'
            'COMMUTE n=16.\tMIDDLE VALUES 10 AND 11.\t(10+11)/2=10.5.\n'
            'MEDIAN IS NOT 50% OF MAX.\tIT IS A POSITION IN\tORDERED DATA.\n'
            'S06 Q1\tS07 Q3\tS01 MEAN\tF06 MEDIAN WITH FREQUENCIES\n'
            ''
            , field)

    if gid == 'S03':
        return STCORE.unpack_guide(
            'Mode\n'
            'TYPICAL START:\t"FIND THE MODE."\t"MOST FREQUENT VALUE."\n'
            'MODE = VALUE OCCURRING\tMOST OFTEN.\t\tTHERE CAN BE MULTIPLE MODES\tOR NO MODE.\n'
            '1. COUNT EACH VALUE.\t2. FIND HIGHEST COUNT.\t3. REPORT VALUE(S),\t   NOT THE COUNT.\n'
            'NO SPECIAL CMD NEEDED.\n'
            '2,3,3,4,5\t3 OCCURS MOST.\tMODE=3.\n'
            'DO NOT REPORT FREQUENCY\tAS MODE.\tMODE IS THE VALUE.\n'
            'F01 FREQUENCY\tS01 MEAN\tS02 MEDIAN\tF07 MODE WITH FREQUENCIES\n'
            ''
            , field)

    if gid == 'S04':
        return STCORE.unpack_guide(
            'Range\n'
            'TYPICAL START:\t"FIND THE RANGE."\tNEEDS MINIMUM AND MAXIMUM.\n'
            'MIN = SMALLEST VALUE.\tMAX = LARGEST VALUE.\t\tRANGE=MAX-MIN.\n'
            '1. FIND MAX.\t2. FIND MIN.\t3. SUBTRACT MIN FROM MAX.\n'
            '1-VAR STATS GIVES\tminX AND maxX.\n'
            'COMMUTE DATA:\tMAX=29, MIN=2.\tRANGE=27.\n'
            'Q3-Q1 IS IQR,\tNOT RANGE.\n'
            'S08 IQR\tS05 FIVE NUMBER\n'
            'RANGE_IQR'
            , field)
    return None
