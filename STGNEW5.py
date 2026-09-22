# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGNEW5 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'D06':
        return STCORE.unpack_guide('Observational vs Experiment\nDID RESEARCHERS IMPOSE TREATMENT?\nEXPERIMENT: ASSIGNED TREATMENT\nOTHERWISE OBSERVATIONAL\nUSE CLASSIFIER\nSURVEY ONLY: OBSERVATIONAL\nMEASURING IS NOT ASSIGNING TREATMENT\nD05\nD06', field)

    if gid == 'D07':
        return STCORE.unpack_guide('Measurement Levels\nNOMINAL ORDINAL INTERVAL RATIO\nORDER; MEANINGFUL GAPS; TRUE ZERO\nCLASSIFY BY WHAT VALUES MEAN\nUSE DEFINITIONS\nCELSIUS: INTERVAL; WEIGHT: RATIO\nNUMBER LABELS ARE NOT QUANTITATIVE\nD01 D02\nD07', field)

    if gid == 'D08':
        return STCORE.unpack_guide('Statistical vs Practical\nSIGNIFICANCE OR ERROR\np-VALUE COMPARED WITH alpha; EFFECT SIZE\nPRACTICAL IMPORTANCE NEEDS CONTEXT\nUSE SIGNIFICANCE MENU\nTINY EFFECT MAY BE STATISTICALLY SIGNIFICANT\nSTATISTICAL DOES NOT IMPLY PRACTICAL\nD09\nD08', field)
    return None
