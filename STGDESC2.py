# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC2 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'D04':
        return STCORE.unpack_guide(
            'Parameter vs Statistic\n'
            'TYPICAL START:\t"IS THIS VALUE A PARAMETER\tOR STATISTIC?"\t\tFIRST ASK WHETHER VALUE\tCOMES FROM POPULATION\tOR SAMPLE.\n'
            'PARAMETER:\tNUMBER DESCRIBING POPULATION.\t\tSTATISTIC:\tNUMBER DESCRIBING SAMPLE.\n'
            '1. IDENTIFY GROUP USED.\t2. WHOLE POPULATION?\t   -> PARAMETER.\t3. SAMPLE?\t   -> STATISTIC.\n'
            'NO CALCULATOR NEEDED.\n'
            'MEAN OF OUR 16 COMMUTES\tIS A STATISTIC.\tTRUE MEAN FOR ENTIRE TARGET\tPOPULATION IS A PARAMETER.\n'
            'MEAN/SD/PROPORTION CAN EACH\tBE PARAMETER OR STATISTIC.\tGROUP SOURCE DECIDES.\n'
            'D03 POPULATION/SAMPLE\n'
            ''
            , field)

    if gid == 'F01':
        return STCORE.unpack_guide(
            'Frequency\n'
            'TYPICAL START:\t"FIND THE FREQUENCY..."\t"HOW MANY OBSERVATIONS..."\tOR A FREQUENCY TABLE.\n'
            'f = NUMBER OF TIMES\tCATEGORY/VALUE OCCURS.\t\tNO DIVISION YET.\n'
            '1. IDENTIFY CATEGORY.\t2. COUNT OCCURRENCES.\t3. THAT COUNT IS f.\n'
            'NO SPECIAL CALCULATOR CMD.\n'
            'IF 6 OF 44 STUDENTS ARE\tIN CATEGORY A:\tFREQUENCY = 6.\n'
            'DO NOT DIVIDE BY n UNLESS\tQUESTION ASKS RELATIVE\tFREQUENCY.\n'
            'F02 RELATIVE FREQUENCY\tF03 CUMULATIVE\n'
            'FREQUENCY_SESSION'
            , field)

    if gid == 'F02':
        return STCORE.unpack_guide(
            'Relative Frequency\n'
            'TYPICAL START:\t"FIND THE RELATIVE\tFREQUENCY..."\t"WHAT PROPORTION IS IN\tTHIS CATEGORY?"\tLONG-RUN PROPORTION\tESTIMATES EVENT PROBABILITY\tQ005 SCRATCHED LENSES\tQ006 LONG-RUN PROPORTION\tQ011 GREEN PEAS\n'
            'f = CATEGORY COUNT.\tn = TOTAL SAMPLE SIZE.\t\tFORMULA:\tREL FREQ = f/n.\n'
            '1. FIND f.\t2. FIND TOTAL n.\t3. DIVIDE f/n.\t4. IF PERCENT ASKED,\t   MULTIPLY BY 100.\n'
            'TYPE f/n ENTER.\tOR CHOOSE SOLVE NOW.\t\tANSWER IS USUALLY DECIMAL\tOR PERCENT.\n'
            'HOMEWORK:\t6 OUT OF 44.\t6/44=.13636...\tREL FREQ=.13636.\tPERCENT=13.636%.\tQ005: 5840/12712=730/1589=0.459 (3 places)\tQ006: Relative frequency estimates event probability\tQ011: 465/609=76.35%; comparison target missing\n'
            'WRONG: n/f.\tPART GOES ON TOP.\t\tDO NOT MULTIPLY BY 100\tUNLESS PERCENT IS WANTED.\n'
            'F01 FREQUENCY\tF03 CUMULATIVE\tF04 PROPORTION\n'
            'CATEGORY_SESSION'
            , field)
    return None
