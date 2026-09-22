# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC8 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'G02':
        return STCORE.unpack_guide(
            'Does Data Look Normal?\n'
            'TYPICAL START:\t"DOES THE DATA APPEAR TO\tCOME FROM A NORMALLY\tDISTRIBUTED POPULATION? WHY?"\n'
            'LOOK FOR:\tROUGH SYMMETRY,\tBELL SHAPE,\tNO STRONG OUTLIERS,\tNO STRONG SKEW.\n'
            '1. LOOK AT HISTOGRAM.\t2. CHECK SYMMETRY.\t3. CHECK TAILS.\t4. CHECK OUTLIERS.\t5. EXPLAIN USING GRAPH.\n'
            'STAT1 GIVES PLOT VALUES.\tDRAW HISTOGRAM/BOXPLOT\tOR USE NATIVE STAT PLOT.\tINTERPRET SHAPE YOURSELF.\n'
            'A CLEAR RIGHT-SKEWED\tCOMMUTE GRAPH IS NOT\tVERY NORMAL-LOOKING.\n'
            'DO NOT SAY NORMAL JUST\tBECAUSE A MEAN AND SD\tCAN BE CALCULATED.\n'
            'G01 SKEW\tG03 OUTLIERS\n'
            ''
            , field)

    if gid == 'G03':
        return STCORE.unpack_guide(
            'Outlier Fences\n'
            'TYPICAL START:\t"ARE THERE OUTLIERS?"\t"USE THE 1.5 IQR RULE."\t"FIND LOWER/UPPER FENCE."\n'
            'NEED Q1 AND Q3.\tIQR=Q3-Q1.\t\tLOW=Q1-1.5(IQR).\tHIGH=Q3+1.5(IQR).\n'
            '1. FIND Q1,Q3.\t2. COMPUTE IQR.\t3. COMPUTE LOW FENCE.\t4. COMPUTE HIGH FENCE.\t5. VALUES OUTSIDE ARE\t   POTENTIAL OUTLIERS.\n'
            '1-VAR STATS FOR Q1,Q3.\tTHEN USE SOLVER OR\tTYPE FENCE FORMULAS.\n'
            'Q1=10,Q3=18.\tIQR=8.\tLOW=-2.\tHIGH=30.\n'
            'FENCES ARE CUTPOINTS,\tNOT NECESSARILY ACTUAL\tDATA VALUES.\n'
            'S08 IQR\tG01 BOXPLOT\n'
            'OUTLIER'
            , field)

    if gid == 'F05':
        return STCORE.unpack_guide(
            'Mean from Frequency Table\n'
            'VALUES + FREQUENCY; MEAN\tQ001 DELIVERIES: FREQUENCY MEAN\n'
            'x=DATA VALUE\tf=HOW OFTEN IT OCCURS\tn=SUM(f), NOT NUMBER OF ROWS\tWEIGHTED TOTAL=SUM(x*f)\n'
            'SUM(x*f)/SUM(f)\n'
            '1-VAR STATS: DATA LIST L1\tFREQUENCY LIST L2\tL1: VALUES, L2: COUNTS\tREAD xbar; LABELS MAY VARY\n'
            '3,6,9,12; f=1,2,6,5: 9.2143\tQ001: 129/14=9.2143; n=14\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)
    return None
