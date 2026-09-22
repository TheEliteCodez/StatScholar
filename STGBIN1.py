# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN1 guide records.
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
    return None
