# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGCNT1 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'C01':
        return STCORE.unpack_guide(
            'Multiplication Principle\n'
            'TYPICAL START:\t"HOW MANY POSSIBLE OUTCOMES"\t"STATE SIZE OF SAMPLE SPACE"\tFOR MULTIPLE STAGES.\n'
            'EACH STAGE HAS SOME\tNUMBER OF CHOICES.\t\tTOTAL OUTCOMES =\tPRODUCT OF CHOICES.\n'
            '1. COUNT CHOICES STAGE 1.\t2. COUNT CHOICES STAGE 2.\t3. CONTINUE FOR ALL STAGES.\t4. MULTIPLY.\n'
            'TYPE PRODUCT.\tOR SAMPLE SPACE SOLVER.\n'
            'DIE + COIN:\t6*2=12.\t\tTWO DICE:\t6*6=36.\n'
            'DO NOT ADD CHOICES\tFOR SEQUENTIAL STAGES.\n'
            'C02 DICE\tC03 nCr\tC04 nPr\n'
            'SAMPLE_SPACE'
            , field)

    if gid == 'C03':
        return STCORE.unpack_guide(
            'Combination nCr\n'
            'TYPICAL START:\t"CHOOSE..."\t"SELECT..."\t"PAIR..."\t"COMMITTEE..."\t\tORDER DOES NOT MATTER.\n'
            'n = TOTAL ITEMS.\tr = NUMBER CHOSEN.\t\tnCr=n!/[r!(n-r)!].\n'
            '1. IDENTIFY n.\t2. IDENTIFY r.\t3. ASK IF A,B SAME AS B,A.\t4. IF YES -> nCr.\n'
            'MATH > PRB > nCr.\tENTER n nCr r.\tOR SOLVER.\n'
            'CHOOSE 2 FROM 8:\t8C2=28.\t\t8*7=56 COUNTS EACH\tPAIR TWICE.\n'
            'IF ORDER MATTERS,\tUSE nPr INSTEAD.\n'
            'C04 nPr\tC01 MULTIPLICATION\n'
            'NCR'
            , field)

    if gid == 'C04':
        return STCORE.unpack_guide(
            'Permutation nPr\n'
            'TYPICAL START:\t"ARRANGE..."\t"ORDER..."\t"RANK..."\t"PRESIDENT AND VP..."\t\tORDER MATTERS.\n'
            'n = TOTAL ITEMS.\tr = POSITIONS FILLED.\t\tnPr=n!/(n-r)!.\n'
            '1. IDENTIFY n.\t2. IDENTIFY r.\t3. ASK IF A,B DIFFERENT\t   FROM B,A.\t4. IF YES -> nPr.\n'
            'MATH > PRB > nPr.\tENTER n nPr r.\tOR SOLVER.\n'
            '8 PEOPLE, PRESIDENT+VP:\t8P2=8*7=56.\n'
            'DO NOT USE nCr WHEN\tROLES/POSITIONS DIFFER.\n'
            'C03 nCr\n'
            'NPR'
            , field)
    return None
