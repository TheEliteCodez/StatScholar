# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC7 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S11':
        return STCORE.unpack_guide(
            'Minimum Usual Value\n'
            'TYPICAL START:\t"MINIMUM USUAL VALUE"\tOR MEAN-2(SD).\n'
            'NEED MEAN AND SD.\t\tFORMULA:\tMEAN-2(SD).\n'
            '1. GET MEAN.\t2. GET SD.\t3. COMPUTE 2*SD.\t4. SUBTRACT FROM MEAN.\n'
            '1-VAR STATS FOR xbar,Sx.\tTHEN xbar-2*Sx.\n'
            'MEAN=20, SD=3:\t20-2(3)=14.\n'
            'SUBTRACT WHOLE 2*SD.\tUSE PARENTHESES.\n'
            'S10 MAX USUAL\tS12 Z-SCORE\n'
            'USUAL'
            , field)

    if gid == 'S12':
        return STCORE.unpack_guide(
            'Z-Score\n'
            'TYPICAL START:\t"FIND THE z-SCORE."\t"ARE ANY VALUES\tSTATISTICALLY HIGH?"\t"HOW MANY SDs FROM MEAN?"\n'
            'NEED:\tx = VALUE BEING CHECKED.\tMEAN = CENTER.\tSD = STANDARD DEVIATION.\t\tz=(x-MEAN)/SD.\n'
            '1. IDENTIFY x.\t2. IDENTIFY MEAN.\t3. IDENTIFY SD.\t4. COMPUTE x-MEAN.\t5. DIVIDE BY SD.\t6. z>2 OFTEN HIGH.\t   z<-2 OFTEN LOW.\n'
            'TYPE (x-mean)/sd.\tPARENTHESES MATTER.\tOR USE SOLVER.\n'
            'COMMUTE x=29:\t(29-11.5625)/7.6243\tABOUT 2.29.\tSTATISTICALLY HIGH.\n'
            'WRONG: x-mean/sd.\tWITHOUT PARENTHESES\tORDER OF OPERATIONS\tCHANGES ANSWER.\n'
            'S10/S11 USUAL VALUES\n'
            'ZSCORE'
            , field)

    if gid == 'G01':
        return STCORE.unpack_guide(
            'Right vs Left Skew\n'
            'TYPICAL START:\t"DESCRIBE THE BOXPLOT."\t"IS DATA SKEWED?"\t"LEFT, RIGHT, OR NORMAL?"\n'
            'LOOK AT TAIL.\t\tLONG TAIL RIGHT\t-> RIGHT SKEW.\t\tLONG TAIL LEFT\t-> LEFT SKEW.\n'
            '1. FIND BULK OF DATA.\t2. FIND SIDE THAT STRETCHES\t   FARTHER.\t3. NAME SKEW BY THAT TAIL.\n'
            'GRAPH WITH STAT PLOT.\tBOXPLOT OR HISTOGRAM.\tZOOMSTAT TO FIT.\n'
            'COMMUTE DATA HAD A LONGER\tHIGH-DISTANCE TAIL.\t-> RIGHT-SKEWED.\n'
            'DO NOT NAME SKEW BY\tWHERE THE BOX/BULK SITS.\tNAME IT BY TAIL.\n'
            'G02 NORMAL\tG03 OUTLIERS\n'
            ''
            , field)
    return None
