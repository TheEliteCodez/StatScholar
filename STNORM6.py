# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Single-observation z / usual report.
import STCORE as c


def observation_report(x,mean,sd,variance=None,inclusive=False):
    variance=c.rmul(sd,sd) if variance is None else variance
    position=c.call('STNORM','usual_classification',x,mean,variance,inclusive)
    c.results('VALUE / Z / USUAL', [('x',x),('z',c.call('STNORM','z_value',x,mean,sd)),
        ('MIN USUAL',c.call('STNORM','x_value',(-2,1),mean,sd)),('MAX USUAL',c.call('STNORM','x_value',(2,1),mean,sd)),
        ('UNUSUAL','NO' if position=='NOT UNUSUAL' else 'YES'),('CLASSIFICATION',position)],
        ['z=(x-MEAN)/SD','BOUNDARIES UNUSUAL' if inclusive else 'BOUNDARIES USUAL','NORMAL MENU 7 CHANGES < / <='])
