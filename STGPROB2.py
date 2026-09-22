# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGPROB2 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'P04':
        return STCORE.unpack_guide(
            'OR: General Addition Rule\n'
            'TYPICAL START:\t"FIND P(A OR B)."\tAND EVENTS CAN OVERLAP.\tMAY GIVE P(A AND B).\n'
            'NEED:\tP(A), P(B),\tP(A AND B).\t\tP(A OR B)=\tP(A)+P(B)-P(A AND B).\n'
            '1. FIND A.\t2. FIND B.\t3. FIND OVERLAP BOTH.\t4. ADD A+B.\t5. SUBTRACT BOTH ONCE.\n'
            'TYPE A+B-BOTH.\tOR USE GENERAL OR SOLVER.\n'
            'DICE:\tSUM=6 ->5/36.\tFIRST DIE=2 ->6/36.\tOVERLAP (2,4)->1/36.\tOR=10/36=5/18.\n'
            'ASK: CAN BOTH HAPPEN?\tIF YES, DO NOT JUST ADD.\n'
            'P03 MUT EXCLUSIVE\tP05 AND\n'
            'GENERAL_OR'
            , field)

    if gid == 'P05':
        return STCORE.unpack_guide(
            'AND: Independent\n'
            'TYPICAL START:\t"A AND B" OR "BOTH"\tAND EVENTS ARE INDEPENDENT.\n'
            'NEED P(A), P(B).\t\tINDEPENDENT MEANS\tONE DOES NOT CHANGE\tPROBABILITY OF OTHER.\t\tP(A AND B)=P(A)*P(B).\n'
            '1. FIND P(A).\t2. FIND P(B).\t3. CONFIRM INDEPENDENT.\t4. MULTIPLY.\n'
            'TYPE A*B.\tOR INDEP AND SOLVER.\n'
            'TWO DICE BOTH EVEN:\t(3/6)*(3/6)\t=9/36=1/4.\n'
            'AND DOES NOT MEAN ADD.\tDO NOT ASSUME INDEPENDENT\tIF QUESTION CHANGES\tPROBABILITY AFTER FIRST.\n'
            'P06 GENERAL AND\tP07 GIVEN\n'
            'INDEP_AND'
            , field)

    if gid == 'P06':
        return STCORE.unpack_guide(
            'AND: General Rule\n'
            'TYPICAL START:\t"A AND B"\tBUT SECOND EVENT DEPENDS\tON FIRST, OR P(B|A) GIVEN.\n'
            'NEED:\tP(A)\tP(B|A)\t\tP(A AND B)=\tP(A)*P(B|A).\n'
            '1. FIND P(A).\t2. FIND P(B GIVEN A).\t3. MULTIPLY.\n'
            'TYPE P(A)*P(B|A).\tOR GENERAL AND SOLVER.\n'
            'WITHOUT REPLACEMENT:\tSECOND DRAW OFTEN HAS\tDIFFERENT PROBABILITY.\n'
            'DO NOT USE P(A)*P(B)\tIF FIRST EVENT CHANGES\tSECOND EVENT.\n'
            'P05 INDEP AND\tP07 GIVEN\n'
            'GENERAL_AND'
            , field)
    return None
