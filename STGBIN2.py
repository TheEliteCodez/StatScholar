# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN2 guide records.
import STCORE


def get_guide(gid, field=None):
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
    return None
