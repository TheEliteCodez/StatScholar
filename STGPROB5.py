# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGPROB5 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'P13':
        return STCORE.unpack_guide(
            'Valid Probability Value\n'
            'CAN THIS BE A PROBABILITY?\tQ007 VALID PROBABILITY?\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            '0<=p<=1\n'
            'USE ENTER VALUES / SOLVE\n'
            '0 AND 1 VALID; 1.2 INVALID\tQ007: Missing value; valid iff 0<=p<=1\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'VALID_PROBABILITY'
            , field)

    if gid == 'P14':
        return STCORE.unpack_guide(
            'Two-Way Table Events\n'
            'ROW/COLUMN TABLE; ONE EVENT\tQ009 GRADE TABLE: MALE\tQ014 GRADES NOT B\tQ015 MEDIUM CONCERN\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ROW OR COLUMN / GRAND TOTAL\n'
            'USE ENTER VALUES / SOLVE\n'
            'MALE 36 / ALL 81 = 4/9\tQ009: 36/81=.4444\tQ014: 41/62=.6613\tQ015: 21/65=.3231\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'TWO_WAY_SESSION'
            , field)
    raise KeyError(gid)
    return None
