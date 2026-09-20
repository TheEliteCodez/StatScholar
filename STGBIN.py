# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN - compact guide records; only the selected record is decoded.
import STCORE

def get_guide(gid, field=None):
    if gid == 'B01':
        return STCORE.unpack_guide(
            'Identify a Binomial Problem\n'
            'TYPICAL START:\t"SUPPOSE ... ARE RANDOMLY\tSELECTED..."\t"OUT OF n..."\t"PROBABILITY p..."\t"HOW MANY SUCCESSES..."\tQ032 REPLACED CARDS BINOMIAL?\tQ036 DEPENDENT FLIGHT DELAYS\tQ038 26 FLU CALLERS\n'
            'CHECK ALL FOUR:\t1. FIXED n.\t2. TWO OUTCOMES.\t3. SAME p EACH TRIAL.\t4. INDEPENDENT TRIALS.\n'
            '1. FIND n.\t2. DEFINE SUCCESS.\t3. FIND p.\t4. CHECK 2 OUTCOMES.\t5. CHECK INDEPENDENCE.\t6. THEN READ WORDING:\t   EXACTLY/AT MOST/ETC.\n'
            'NO PDF/CDF UNTIL YOU\tDECIDE WHICH WORDING\tTHE QUESTION USES.\n'
            '12 JURORS, p=.41,\tCOUNT # WITH A TRAIT.\tIF CONDITIONS FIT,\tBINOMIAL.\tQ032: TRUE; n=15 p=13/52; independent draws\tQ036: NOT BINOMIAL: flights explicitly dependent\tQ038: Binomial(26,.16), assuming independence; second part missing\n'
            'DO NOT USE BINOMIAL\tJUST BECAUSE QUESTION\tHAS A COUNT.\n'
            'B02 EXACTLY\tB03 AT MOST\tB05 AT LEAST\n'
            'BINOMIAL_CONDITIONS'
            , field)
    if gid == 'B02':
        return STCORE.unpack_guide(
            'Binomial Exactly x\n'
            'TYPICAL START:\t"WHAT IS PROBABILITY\tTHAT EXACTLY 5..."\t"P(X=5)"\tQ039 18 PEOPLE ELECTRICITY\tQ043 39 STUDENTS MATH CLASS\tQ044 50 EAGLES SURVIVE\tQ048 148 BUILDING SUPPORTERS\n'
            'n = # TRIALS.\tp = SUCCESS PROB.\tx = EXACT SUCCESS COUNT.\t\tEXACTLY -> PDF.\n'
            '1. VERIFY BINOMIAL.\t2. IDENTIFY n,p,x.\t3. USE binompdf(n,p,x).\n'
            'DISTRIBUTION MENU.\tbinompdf(n,p,x).\tOR SOLVER.\n'
            'n=12,p=.41,x=5:\tbinompdf(12,.41,5).\tQ039: Binomial(18,.08); .1196,.8298,.1702,.4260\tQ043: p=.63; .1281,.6158,.7560,.7122\tQ044: p=.75; .0985,.9084,.3816,.7287\tQ048: n=148,p=.25; .0499,.1478,.8023,.0552,.2504,.8047\n'
            'DO NOT USE CDF.\tCDF ADDS 0 THROUGH x.\n'
            'B03 AT MOST\tB05 AT LEAST\tB07 FORMULA\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B03':
        return STCORE.unpack_guide(
            'Binomial At Most x\n'
            'TYPICAL START:\t"AT MOST 5"\t"NO MORE THAN 5"\t"X<=5"\tQ045 ACCEPT SHIPMENT\n'
            'AT MOST INCLUDES x.\tVALUES 0 THROUGH x.\t\tUSE CDF(n,p,x).\n'
            '1. VERIFY BINOMIAL.\t2. IDENTIFY n,p,x.\t3. TRANSLATE AT MOST -> <=.\t4. USE CDF AT x.\n'
            'binomcdf(n,p,x).\tOR SOLVER.\n'
            'AT MOST 5:\tCDF(...,5).\tQ045: Binomial approximation: n=23,p=.05; P(<=1)=.6794\n'
            'DO NOT USE x-1.\tAT MOST 5 INCLUDES 5.\n'
            'B04 LESS THAN\tB05 AT LEAST\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B04':
        return STCORE.unpack_guide(
            'Binomial Less Than x\n'
            'TYPICAL START:\t"LESS THAN 5"\t"FEWER THAN 5"\t"X<5"\tQ046 TORNADOES IN 11 YEARS\n'
            'LESS THAN EXCLUDES x.\tCDF INCLUDES ENDPOINT,\tSO STOP AT x-1.\n'
            '1. VERIFY BINOMIAL.\t2. IDENTIFY x.\t3. COMPUTE x-1.\t4. CDF(n,p,x-1).\n'
            'binomcdf(n,p,x-1).\n'
            'LESS THAN 5:\tVALUES 0..4.\tCDF(...,4).\tQ046: n=11,p=.04; P(<4)=P(<=3)=.9993265560\n'
            'CDF(...,5) WOULD MEAN\tAT MOST 5.\n'
            'B03 AT MOST\tB06 MORE THAN\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B05':
        return STCORE.unpack_guide(
            'Binomial At Least x\n'
            'TYPICAL START:\t"AT LEAST 5"\t"5 OR MORE"\t"NO FEWER THAN 5"\t"X>=5"\n'
            'AT LEAST INCLUDES x.\tREMOVE EVERYTHING BELOW x.\t\tP(X>=x)=\t1-CDF(n,p,x-1).\n'
            '1. VERIFY BINOMIAL.\t2. IDENTIFY n,p,x.\t3. x-1 = LAST VALUE BELOW x.\t4. COMPUTE CDF THROUGH x-1.\t5. SUBTRACT FROM 1.\n'
            '1-binomcdf(n,p,x-1).\tOR SOLVER.\n'
            'n=12,p=.41, AT LEAST 5:\tx-1=4.\t1-binomcdf(12,.41,4).\n'
            '1-CDF(...,5) IS WRONG\tFOR AT LEAST 5.\tTHAT REMOVES 5 TOO\tAND MEANS MORE THAN 5.\n'
            'B03 AT MOST\tB06 MORE THAN\tP09 AT LEAST ONE\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B06':
        return STCORE.unpack_guide(
            'Binomial More Than x\n'
            'TYPICAL START:\t"MORE THAN 5"\t"GREATER THAN 5"\t"X>5"\n'
            'MORE THAN EXCLUDES x.\tREMOVE 0 THROUGH x.\t\tP(X>x)=\t1-CDF(n,p,x).\n'
            '1. VERIFY BINOMIAL.\t2. IDENTIFY n,p,x.\t3. CDF THROUGH x.\t4. SUBTRACT FROM 1.\n'
            '1-binomcdf(n,p,x).\n'
            'MORE THAN 5:\t1-CDF(...,5).\n'
            'USING x-1 WOULD INCLUDE x\tAND MEAN AT LEAST x.\n'
            'B04 LESS THAN\tB05 AT LEAST\n'
            'BINOMIAL_SESSION'
            , field)
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
    if gid == 'B10':
        return STCORE.unpack_guide(
            'Binomial Between a and b\n'
            'TYPICAL START:\t"BETWEEN 3 AND 6\tINCLUSIVE"\t"3<=X<=6"\n'
            'a = LOW END.\tb = HIGH END.\t\tCDF(b) HAS 0..b.\tSUBTRACT CDF(a-1).\n'
            '1. IDENTIFY a,b.\t2. COMPUTE CDF(b).\t3. COMPUTE CDF(a-1).\t4. SUBTRACT.\n'
            'binomcdf(n,p,b)\t-binomcdf(n,p,a-1).\n'
            'P(3<=X<=6)=\tCDF(6)-CDF(2).\n'
            'CHECK WHETHER ENDPOINTS\tARE INCLUDED.\tSTRICTLY BETWEEN CHANGES\tTHE LIMITS.\n'
            'B03 AT MOST\tB04 LESS THAN\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B11':
        return STCORE.unpack_guide(
            'Full Binomial Distribution\n'
            'LIST X AND P(X) FOR TRIALS\tQ035 THREE FLIPS COUNT HEADS\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'X=0..n; P=nCx*p^x*(1-p)^(n-x)\n'
            'USE ENTER VALUES / SOLVE\n'
            '3 FAIR FLIPS: 1,3,3,1 OVER 8\tQ035: 1/8,3/8,3/8,1/8; symmetric; mu=1.500 heads; sigma=.866; P(<=2)=7/8\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'BINOMIAL_SESSION'
            , field)
    if gid == 'B12':
        return STCORE.unpack_guide(
            'Binomial Shape and Symmetry\n'
            'MATCH GRAPH TO p; SYMMETRY\tQ033 BINOMIAL TAIL SYMMETRY?\tQ042 MATCH THREE HISTOGRAMS\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'GRAPH CENTER=np\tREFLECTED TAILS MATCH IF p=.5\tFIXED n DOES NOT FIX p\tUSE COMPARE TAILS FOR EQUALITY\n'
            'USE ENTER VALUES / SOLVE\n'
            'n=10,p=.35: CENTER=3.5\tQ033: FALSE generally; matching opposite tails requires p=.5\tQ042: n=10; top-to-bottom p=.35,.25,.20; centers=3.5,2.5,2\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SHAPE_TASKS'
            , field)
    if gid == 'B13':
        return STCORE.unpack_guide(
            'Binomial Usual Counts\n'
            'RANGE RULE; FIRST UNUSUAL\tQ034 CHICKENPOX 123 ADULTS\tQ047 47 DAYS FORGET LUNCH\tQ049 ON-TIME BUSES\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'mu=np; SD=SQRT(np(1-p))\tUSUAL: mu +/- 2 SD\tINTEGERS: CEIL LOW, FLOOR HIGH\tFIRST HIGH=FLOOR(HIGH)+1\tEXACT TAIL: SUM BINOMIAL P\n'
            'USE ENTER VALUES / SOLVE\n'
            '47,.387: FIRST HIGH=25\tQ034: mu=110.7000; SD=3.3272; 100 unusually low; P(100)=.0013\tQ047: mu=18.189; SD=3.33914016; first high=25; P(>=25)=.03071365753; part a labels missing\tQ049: n MISSING; p=.64; mu=.64n; SD=.48sqrt(n); integer range then exact tails\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'BINOMIAL_SESSION'
            , field)
    raise KeyError(gid)
