# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC6 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S08':
        return STCORE.unpack_guide(
            'Interquartile Range IQR\n'
            'TYPICAL START:\t"FIND THE IQR."\t"INTERQUARTILE RANGE."\t"SPREAD OF MIDDLE 50%."\n'
            'YOU NEED Q1 AND Q3.\t\tIQR=Q3-Q1.\n'
            '1. FIND Q1.\t2. FIND Q3.\t3. SUBTRACT Q1 FROM Q3.\n'
            '1-VAR STATS FOR Q1,Q3.\tTHEN TYPE Q3-Q1.\n'
            'COMMUTE:\t16.5-5.5=11.\n'
            'MAX-MIN IS RANGE.\tQ3-Q1 IS IQR.\n'
            'S04 RANGE\tG03 OUTLIERS\n'
            'RANGE_IQR'
            , field)

    if gid == 'S09':
        return STCORE.unpack_guide(
            'Sample Standard Deviation\n'
            'TYPICAL START:\t"FIND THE SAMPLE STANDARD\tDEVIATION."\t"FIND s."\n'
            'ON EVO:\tSx = SAMPLE SD.\tsigma-x = POPULATION SD.\t\tIF DATA IS A SAMPLE,\tREPORT Sx.\n'
            'BY-HAND FORMULA USES n-1,\tBUT FOR LONG RAW DATA\tUSE 1-VAR STATS.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tREAD Sx.\n'
            'COMMUTE SAMPLE:\tSx ABOUT 7.6243.\n'
            'COMMON ERROR:\tREPORTING sigma-x FOR\tA SAMPLE.\n'
            'S01 MEAN\tS12 Z-SCORE\n'
            ''
            , field)

    if gid == 'S10':
        return STCORE.unpack_guide(
            'Maximum Usual Value\n'
            'TYPICAL START:\t"CALCULATE THE MAXIMUM\tUSUAL VALUE = MEAN +\t2*(STANDARD DEVIATION)."\n'
            'NEED:\tMEAN\tSTANDARD DEVIATION\t\tFORMULA:\tMEAN+2(SD).\n'
            '1. GET MEAN.\t2. GET SD.\t3. MULTIPLY SD BY 2.\t4. ADD TO MEAN.\t5. VALUES ABOVE ARE\t   OFTEN STAT HIGH.\n'
            'GET xbar AND Sx USING\t1-VAR STATS IF NEEDED.\tTHEN TYPE xbar+2*Sx.\n'
            'COMMUTE:\t11.5625+2(7.6243)\tABOUT 26.81.\t29 > 26.81.\n'
            'WRONG: MEAN+SD+2.\tWRONG: 2*MEAN+SD.\n'
            'S11 MIN USUAL\tS12 Z-SCORE\n'
            'USUAL'
            , field)
    return None
