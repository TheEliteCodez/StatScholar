# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGBIN - guide records; selected record loads from a part module.
import STCORE


def get_guide(gid, field=None):
    for mod in ('STGBIN1', 'STGBIN2', 'STGBIN3', 'STGBIN4', 'STGBIN5'):
        result = STCORE.call(mod, 'get_guide', gid, field)
        if result is not None:
            return result
    return None
