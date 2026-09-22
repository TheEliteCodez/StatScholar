# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Unusual-observation classifier for a data set.
import STCORE as c


def usual_data(values,stats,title,inclusive,population=False):
    variance=stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2']
    if variance=='DNE':
        c.view(title,['NEED TWO VALUES FOR SAMPLE SD'])
        return
    sd=c.as_ratio(str(stats['POPULATION SD' if population else 'SAMPLE SD Sx']))
    answers=[('MIN USUAL',c.call('STNORM','x_value',(-2,1),stats['MEAN'],sd)),('MAX USUAL',c.call('STNORM','x_value',(2,1),stats['MEAN'],sd))]
    for x in values:
        result=c.call('STNORM','usual_classification',x,stats['MEAN'],variance,inclusive)
        if result!='NOT UNUSUAL': answers.append((c.exact_text(x),result))
    if len(answers)==2: answers.append(('UNUSUAL OBSERVATIONS','NONE'))
    c.results(title,answers,['SAMPLE MEAN +/- 2s','BOUNDARIES ARE UNUSUAL' if inclusive else 'BOUNDARIES ARE USUAL','CLASSIFICATION USES UNROUNDED VARIANCE'])
