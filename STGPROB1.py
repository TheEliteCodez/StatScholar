# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGPROB1 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'P01':
        return STCORE.unpack_guide(
            'Basic Probability\n'
            'TYPICAL START:\t"FIND THE PROBABILITY..."\tAND YOU CAN COUNT\tFAVORABLE / TOTAL\tEQUALLY LIKELY OUTCOMES.\tQ003 ROULETTE 0 AND 00\tQ008 52-CARD DECK\tQ012 SPINNER EVEN\n'
            'NEED:\tFAVORABLE OUTCOMES.\tTOTAL OUTCOMES.\t\tP(E)=FAVORABLE/TOTAL.\n'
            '1. DEFINE EVENT E.\t2. COUNT FAVORABLE.\t3. COUNT TOTAL.\t4. DIVIDE.\t5. REDUCE IF ASKED.\n'
            'TYPE favorable/total.\tSOLVER SHOWS REDUCED\tFRACTION, DECIMAL, PERCENT.\n'
            'TWO DICE SUM=6:\t5 FAVORABLE.\t36 TOTAL.\tP=5/36.\tROULETTE 0,00,1..36:\tP(1)=1/38; P(ODD)=18/38\tCARDS: P(4S)=1/52\tACE OR 2: 8/52\tQ003: 38 spaces; single=1/38; odd=9/19\tQ008: 4S=.0192; S OR D=.5000; ace or 2=.1538\tQ012: 6/12=.5000 IF equal sectors 1..12\n'
            'DO NOT REVERSE FRACTION.\tONLY USE COUNT/TOTAL\tWHEN OUTCOMES ARE\tEQUALLY LIKELY.\n'
            'P02 COMPLEMENT\tP04 OR\tP05 AND\n'
            'BASIC_PROB'
            , field)

    if gid == 'P02':
        return STCORE.unpack_guide(
            'Complement / NOT\n'
            'TYPICAL START:\t"PROBABILITY THAT IT IS NOT..."\t"DOES NOT..."\t"NONE..."\tQ013 SURVEY NOT BELIEVING\n'
            'NEED P(E) OR PROBABILITY\tOF OPPOSITE EVENT.\t\tP(NOT E)=1-P(E).\n'
            '1. IDENTIFY ORIGINAL EVENT.\t2. FIND P(E).\t3. SUBTRACT FROM 1.\n'
            'TYPE 1-P(E).\tSOLVER ACCEPTS .18,\t18%, OR 18/100.\n'
            'P(WRONG PD)=.18.\tP(NOT WRONG PD)\t=1-.18=.82.\tQ013: 448/678=.6608\n'
            'USE 1 FOR PROBABILITY\tDECIMALS, OR 100%\tONLY IF WORKING ENTIRELY\tIN PERCENT.\n'
            'P09 AT LEAST ONE\tP01 BASIC\n'
            'COMPLEMENT'
            , field)

    if gid == 'P03':
        return STCORE.unpack_guide(
            'OR: Mutually Exclusive\n'
            'TYPICAL START:\t"E AND F ARE MUTUALLY\tEXCLUSIVE EVENTS."\t"FIND P(E OR F)."\n'
            'MUTUALLY EXCLUSIVE =\tCANNOT BOTH HAPPEN.\t\tP(E AND F)=0.\n'
            '1. SEE MUTUALLY EXCLUSIVE.\t2. KNOW OVERLAP=0.\t3. ADD P(E)+P(F).\n'
            'TYPE P(E)+P(F).\tOR USE MUT EXCL SOLVER.\n'
            'P(E)=.31, P(F)=.22.\tP(E OR F)=.53.\n'
            'MUTUALLY EXCLUSIVE IS\tNOT THE SAME AS\tINDEPENDENT.\n'
            'P04 GENERAL OR\tP05 INDEPENDENT\n'
            'MUT_OR'
            , field)
    return None
