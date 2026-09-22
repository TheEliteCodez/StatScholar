# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STHIST - histogram dispatcher; heavy code loads per group.
import STCORE



def grouped_rows(rows,start,width,count,closed_last=False):
    return STCORE.call('STHIST1', 'grouped_rows', rows, start, width, count, closed_last)



def histogram_session(values=None,group_first=False,rows=None):
    return STCORE.call('STHIST2', 'histogram_session', values, group_first, rows)



def group_session():
    return STCORE.call('STHIST2', 'group_session')
