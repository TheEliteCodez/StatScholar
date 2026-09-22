# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGPROB3 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'P07':
        return STCORE.unpack_guide(
            'Conditional Probability / GIVEN\n'
            'TYPICAL START:\t"FIND P(E|F)."\t"PROBABILITY OF E GIVEN F."\t"AMONG THOSE WHO ARE F..."\t\tTHE | SYMBOL MEANS GIVEN.\n'
            'IF P(A|B):\tA = EVENT YOU WANT.\tB = EVENT YOU ALREADY KNOW.\tA AND B = OVERLAP.\t\tFORMULA:\tP(A|B)=P(A AND B)/P(B).\n'
            '1. READ A|B AS A GIVEN B.\t2. EVENT AFTER | IS B.\t3. FIND OVERLAP A AND B.\t4. FIND TOTAL PROB OF B.\t5. DIVIDE BOTH/B.\t\tWITH COUNTS:\t# BOTH / # B.\n'
            'IF PROBS GIVEN:\tTYPE BOTH/B.\t\tIF TABLE COUNTS:\tDIVIDE BOTH-CELL COUNT\tBY TOTAL COUNT FOR B.\n'
            'P(E AND F)=.18.\tP(F)=.42.\tP(E|F)=.18/.42\t=.428571...\t=42.86%.\n'
            'WRONG: P(E)/P(F).\tNUMERATOR MUST BE BOTH.\t\tWRONG: P(E)+P(F).\tTHAT IS NOT GIVEN.\t\tMEMORY:\tAFTER | = DENOMINATOR.\n'
            'P04 OR\tP06 AND\tINDEPENDENCE\n'
            'CONDITIONAL'
            , field)

    if gid == 'P08':
        return STCORE.unpack_guide(
            'Venn / Survey A OR B\n'
            'TYPICAL START:\t"IN A SURVEY OF ..."\t"... SAID A, ... SAID B,\tAND ... SAID BOTH."\n'
            'VALUES:\t#A\t#B\t#BOTH\tTOTAL n IF PROBABILITY\tOR NEITHER IS ASKED.\n'
            '1. ADD #A + #B.\t2. SUBTRACT #BOTH ONCE.\t3. RESULT = #(A OR B).\t4. DIVIDE BY n IF\t   PROBABILITY ASKED.\n'
            'BASIC +,-,/.\tGENERAL OR SOLVER CAN\tALSO BE USED WITH\tPROPORTIONS.\n'
            '184 COMPOST.\t238 RECYCLE.\t123 BOTH.\tA OR B:\t184+238-123=299.\n'
            'DO NOT COUNT BOTH TWICE.\tFOR NEITHER:\tTOTAL-(A OR B).\n'
            'P04 GENERAL OR\tP02 COMPLEMENT\n'
            ''
            , field)

    if gid == 'P09':
        return STCORE.unpack_guide(
            'At Least One\n'
            'TYPICAL START:\t"WHAT IS THE PROBABILITY\tTHAT AT LEAST ONE..."\n'
            'AT LEAST ONE = 1 OR MORE.\tOPPOSITE EVENT = NONE.\t\tIF EACH TRIAL SUCCESS p:\tFAIL=1-p.\tP(NONE)=(1-p)^n.\n'
            '1. FIND p SUCCESS.\t2. FIND 1-p FAILURE.\t3. RAISE FAILURE TO n.\t4. SUBTRACT FROM 1.\n'
            'TYPE 1-(1-p)^n.\tOR USE SOLVER.\n'
            '5 DICE, AT LEAST ONE 3:\tp=1/6.\tP=1-(5/6)^5.\n'
            "DO NOT CONFUSE WITH\tBINOMIAL 'AT LEAST x'.\tTHIS SPECIAL CASE IS\tAT LEAST ONE.\n"
            'P02 COMPLEMENT\tB05 AT LEAST x\n'
            'AT_LEAST_ONE'
            , field)
    return None
