# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGNEW6 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'D09':
        return STCORE.unpack_guide('Law of Large Numbers\nRELATIVE FREQUENCY OVER MANY TRIALS\nINDEPENDENT TRIALS WITH SAME p\nRELATIVE FREQUENCY TENDS TOWARD TRUE p\nUSE RELATIVE FREQUENCY f/n\nMANY FAIR COIN FLIPS: HEAD FRACTION NEAR .5\nA WIN IS NOT DUE AFTER LOSSES\nF02 F04\nD09', field)

    if gid == 'P15':
        return STCORE.unpack_guide('Certain / Impossible\nCAN A VALUE BE A PROBABILITY?\n0<=p<=1\n0 IMPOSSIBLE; 1 CERTAIN; BETWEEN POSSIBLE\nENTER DECIMAL FRACTION OR PERCENT\np=1: CERTAIN\nVALID SINGLE p DOES NOT VALIDATE WHOLE TABLE\nP13 R01\nP15', field)
    return None
