# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGNEW2 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'S16':
        return STCORE.unpack_guide('Compare Two Data Sets\nCOMPARE GROUPS OR LISTS\nMEAN MEDIAN SD VAR RANGE IQR\nCOMPARE CENTERS AND SPREAD SEPARATELY\n1-VAR STATS FOR EACH LIST\n1,2,3 VS 2,4,6: MEANS 2,4; SDs 1,2\nUSE MORE THAN ONE MEASURE\nG04 G09\nS16', field)

    if gid == 'G04':
        return STCORE.unpack_guide('Boxplot Builder\nDRAW BOX AND WHISKERS\nFIVE NUMBER SUMMARY; IQR; FENCES\nBOX Q1 TO Q3; MEDIAN LINE; NON-OUTLIER WHISKERS\nSTAT PLOT MODIFIED BOXPLOT\n1,2,3,4,100: UPPER FENCE=127; NO OUTLIER\nFIVE NUMBERS MAY NOT IDENTIFY MODIFIED WHISKERS\nS13 S16\nG04', field)

    if gid == 'G05':
        return STCORE.unpack_guide('Dotplot Builder\nDRAW DOTS FOR DATA\nVALUE AND COUNT\nSTACK REPEATS; KEEP NUMERIC AXIS SPACING\nUSE COUNTS TO DRAW ON PAPER\n20,22,22: COUNTS 1,0,2 AT 20,21,22\nDO NOT OMIT SPACING FOR MISSING VALUES\nS13 G06\nG05', field)
    return None
