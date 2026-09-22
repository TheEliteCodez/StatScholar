# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGCNT4 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'R07':
        return STCORE.unpack_guide(
            'Sample Without Replacement\n'
            'BOX; TARGET COUNT; SELECT n\tQ025 8 CAMERAS 5 DEFECTIVE\tQ026 6 CAMERAS 4 DEFECTIVE\tQ027 17 PENS 5 DEFECTIVE\tQ037 8 CAMERAS 3 DEFECTIVE\n'
            'N=ALL OBJECTS\tK=TARGET/DEFECTIVE OBJECTS\tn=OBJECTS DRAWN\tk=TARGET COUNT IN SAMPLE\tE(X)=n*K/N\n'
            'C(K,k)*C(N-K,n-k)/C(N,n)\n'
            'USE ENTER VALUES / SOLVE\n'
            'N=8 K=5 n=2: E=5/4\tQ025: P(0..2)=3/28,15/28,5/14; E=5/4\tQ026: .0667,.5333,.4000; E=1.3333\tQ027: 11/34,33/68,3/17,1/68; E=15/17\tQ037: 5/14,15/28,3/28; E=3/4\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SAMPLE_SESSION'
            , field)

    if gid == 'R08':
        return STCORE.unpack_guide(
            'Expected Profit or Loss\n'
            'PRIZES, COSTS, PROFIT, LOSS\tQ028 FOUR SUIT GUESSES\tQ029 MARBLE PRIZES AND COST\tQ030 INSURER EXPECTATION\tQ031 RAFFLE BUYER / PTO\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'SUM(NET PAYOFF*PROBABILITY)\n'
            'USE ENTER VALUES / SOLVE\n'
            'GOLD/SILVER/BLACK: E=-1/7\tQ028: P(win)=1/256; E=-1.93359375; SD=17.0291422\tQ029: NET outcomes 5,1,-1; P=3/42,9/42,30/42; E=-1/7\tQ030: 259-206000*(1-.999363)=127.78\tQ031: -1.67; eight=-13.33; PTO one=1.67; all=400\n'
            'CHOOSE WHOSE PROFIT\tSUBTRACT COST ONLY ONCE\tKEEP NEGATIVE LOSSES\tE(DOLLARS) IS NOT A WIN %\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'PAYOFF_SESSION'
            , field)
    raise KeyError(gid)
    return None
