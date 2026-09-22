# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC - guide records; selected record loads from a part module.
import STCORE


def get_guide(gid, field=None):
    for mod in ('STGDESC1', 'STGDESC2', 'STGDESC3', 'STGDESC4', 'STGDESC5', 'STGDESC6', 'STGDESC7', 'STGDESC8', 'STGDESC9'):
        result = STCORE.call(mod, 'get_guide', gid, field)
        if result is not None:
            return result
    return None
