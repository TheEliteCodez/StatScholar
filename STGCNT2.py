# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGCNT2 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'R01':
        return STCORE.unpack_guide(
            'Valid Probability Distribution\n'
            'TYPICAL START:\tTABLE WITH x AND P(x).\t"IS THIS A VALID\tPROBABILITY DISTRIBUTION?"\n'
            'CHECK TWO THINGS:\t1. EACH P(x) BETWEEN 0 AND 1.\t2. SUM OF P(x)=1.\n'
            '1. INSPECT EACH P(x).\t2. ADD ALL PROBABILITIES.\t3. IF ANY OUTSIDE 0..1\t   -> INVALID.\t4. IF TOTAL !=1 -> INVALID.\n'
            'USE + OR LIST SUM.\tEXPECTED VALUE SOLVER\tALSO REPORTS SUM P(x).\n'
            '.2 + .5 + .3 = 1.\tALL ARE BETWEEN 0 AND 1.\t-> VALID.\n'
            'DO NOT USE EXPECTED VALUE\tTO DECIDE VALIDITY.\n'
            'R02 EXPECTED VALUE\tR03 VAR/SD\n'
            ''
            , field)

    if gid == 'R02':
        return STCORE.unpack_guide(
            'Expected Value E(X)\n'
            'TYPICAL START:\tTABLE WITH x AND P(x).\t"FIND THE EXPECTED VALUE\tOF X."\t"FIND E(X)."\tQ021 SCORE EXPECTED VALUE\tQ023 RAFFLE EV IS WIN %?\tQ024 GAME EV IS WIN %?\n'
            'x = POSSIBLE VALUE.\tP(x) = ITS PROBABILITY.\t\tE(X)=SUM[x*P(x)].\n'
            '1. CHECK PROBS SUM TO 1.\t2. MULTIPLY EACH x*P(x).\t3. ADD ALL PRODUCTS.\t4. RESULT IS LONG-RUN MEAN.\n'
            'OPTION 1:\tL1=x VALUES.\tL2=P(x).\t1-VAR STATS, FREQ=L2.\txbar=E(X).\t\tOPTION 2: PROGRAM SOLVER.\n'
            'x: 0,1,2\tP: .2,.5,.3\tE=0(.2)+1(.5)+2(.3)\t=1.1.\tQ021: SUM(score*probability)=6.37\tQ023: FALSE: dollars are not a probability\tQ024: FALSE: long-run average dollars per play\n'
            'DO NOT SIMPLY AVERAGE x.\tP(x) VALUES ARE WEIGHTS.\tEXPECTED VALUE CAN BE\tA NON-POSSIBLE DECIMAL.\tEXPECTED DOLLARS ARE NOT %\tE=.85 DOES NOT MEAN 85% WIN\n'
            'R01 VALID DISTRIBUTION\tR03 VAR/SD\n'
            'DISTRIBUTION_SESSION'
            , field)

    if gid == 'R03':
        return STCORE.unpack_guide(
            'Variance / SD of Distribution\n'
            'TYPICAL START:\tx,P(x) TABLE.\t"FIND VARIANCE"\tOR "STANDARD DEVIATION".\n'
            'mu=E(X).\tE(X^2)=SUM[x^2P(x)].\t\tVAR=E(X^2)-mu^2.\tSD=sqrt(VAR).\n'
            '1. FIND E(X).\t2. FIND E(X^2).\t3. SUBTRACT mu^2.\t4. SQRT FOR SD.\n'
            'USE EXPECTED VALUE\tPROGRAM SOLVER FOR\tmu, VAR, SD.\n'
            'IF mu=2 AND E(X^2)=5:\tVAR=5-4=1.\tSD=1.\n'
            'DO NOT FORGET SQRT\tWHEN QUESTION ASKS SD.\n'
            'R02 EXPECTED VALUE\tB09 BINOM SD\n'
            'DISTRIBUTION_SESSION'
            , field)
    return None
