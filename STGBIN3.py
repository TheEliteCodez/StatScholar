# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN3 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'B07':
        return STCORE.unpack_guide(
            'Binomial Formula Printed\n'
            'TYPICAL START:\tQUESTION PRINTS:\tnCx*p^x*(1-p)^(n-x)\tOR ASKS TO USE BINOMIAL\tPROBABILITY FORMULA.\n'
            'n = TRIALS.\tx = SUCCESSES.\tp = SUCCESS PROB.\t1-p = FAILURE PROB.\tnCx = WAYS TO CHOOSE\tWHICH TRIALS SUCCEED.\n'
            '1. IDENTIFY n,x,p.\t2. COMPUTE nCx.\t3. COMPUTE p^x.\t4. COMPUTE (1-p)^(n-x).\t5. MULTIPLY ALL.\t\tTHIS IS EXACTLY x.\n'
            'EASIER CHECK:\tbinompdf(n,p,x).\tIF WORK REQUIRED, WRITE\tFORMULA SUBSTITUTION.\n'
            'n=6,p=.2,x=2:\t6C2*(.2)^2*(.8)^4.\n'
            'USE nCr, NOT nPr.\tTHIS FORMULA IS FOR\tEXACTLY x.\n'
            'B02 EXACTLY\tC03 nCr\n'
            'BIN_EXACT'
            , field)

    if gid == 'B08':
        return STCORE.unpack_guide(
            'Binomial Mean\n'
            'TYPICAL START:\t"FIND THE MEAN OF A\tBINOMIAL DISTRIBUTION."\t"EXPECTED # SUCCESSES."\tQ041 BLOOD TYPE EXPECTATION\n'
            'n = TRIALS.\tp = SUCCESS PROB.\t\tmu=n*p.\n'
            '1. IDENTIFY n.\t2. IDENTIFY p.\t3. MULTIPLY n*p.\n'
            'TYPE n*p.\tOR BINOM MEAN/SD SOLVER.\n'
            'n=12,p=.41:\tmu=4.92.\tQ041: 23*.099=2.277\n'
            'MEAN CAN BE DECIMAL\tEVEN THOUGH X IS WHOLE.\n'
            'B09 BINOM SD\tR02 EXPECTED VALUE\n'
            'BINOMIAL_SESSION'
            , field)

    if gid == 'B09':
        return STCORE.unpack_guide(
            'Binomial Variance / SD\n'
            'TYPICAL START:\t"FIND STANDARD DEVIATION\tOF BINOMIAL DISTRIBUTION."\tQ040 BLOOD TYPE STANDARD DEV\n'
            'n = TRIALS.\tp = SUCCESS.\tq=1-p.\t\tVAR=npq.\tSD=sqrt(npq).\n'
            '1. FIND q=1-p.\t2. COMPUTE n*p*q.\t3. THAT IS VARIANCE.\t4. SQRT FOR SD.\n'
            'TYPE sqrt(n*p*(1-p)).\tOR SOLVER.\n'
            'n=12,p=.41,q=.59.\tSD=sqrt(12*.41*.59).\tQ040: SQRT(19*.108*.892)=1.3529168489\n'
            'DO NOT REPORT VARIANCE\tWHEN QUESTION ASKS SD.\tSD NEEDS SQUARE ROOT.\n'
            'B08 MEAN\tR03 VAR/SD\n'
            'BINOMIAL_SESSION'
            , field)
    return None
