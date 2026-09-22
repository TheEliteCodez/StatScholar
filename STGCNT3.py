# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGCNT3 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'R04':
        return STCORE.unpack_guide(
            'Probability from X/P Table\n'
            'TABLE ALREADY GIVES P(X)\tQ020 JURY EXACTLY / FEW\tQ022 WEBCAM DEFECT TABLE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ADD ONLY MATCHING ROWS\n'
            'USE ENTER VALUES / SOLVE\n'
            'P(2<=X<=4)=.024+.018+.005\tQ020: Exactly 5=.0004; <=5 approx .0004; unusual YES at .05. 0+ is rounded.\tQ022: .904; 1-.904=.096; 2..4=.047; exactly 1=.047 unusual at .05\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'DISTRIBUTION_SESSION'
            , field)

    if gid == 'R05':
        return STCORE.unpack_guide(
            'Missing Probability\n'
            'ONE BLANK IN P(X) COLUMN\tQ018 ONE MISSING P(X)\tQ019 COMPLETE P COLUMN\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            '1-SUM(KNOWN PROBABILITIES)\n'
            'USE ENTER VALUES / SOLVE\n'
            '1-(.18+.13+.2+.13+.2)=.16\tQ018: 1-.84=.16\tQ019: 1-(.1+.2+.2)=.5\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'MISSING_PROBABILITY'
            , field)

    if gid == 'R06':
        return STCORE.unpack_guide(
            'Unusual Event Probability\n'
            'IS AN EVENT UNUSUAL?\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'COMPARE EVENT P WITH CUTOFF\n'
            'USE ENTER VALUES / SOLVE\n'
            '.047<=.05: UNUSUAL\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'DISTRIBUTION_SESSION'
            , field)
    return None
