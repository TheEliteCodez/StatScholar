# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Editing helpers and frequency-row entry.
import STCORE as c


def edit_raw(values):
    c.paged_results('SORTED VALUES / EDIT INDEX',len(values),lambda i:(str(i+1),values[i]))
    index=c.read_size('SORTED INDEX TO CHANGE: ',len(values))-1
    values[index]=c.read_exact('NEW VALUE: ')
    return c.exact_sorted(values)


def edit_frequency(rows):
    c.paged_results('FREQUENCY ROWS',len(rows),lambda i:(str(i+1),c.exact_text(rows[i][0])+' COUNT='+str(rows[i][1])))
    index=c.read_size('ROW TO CHANGE: ',len(rows))-1
    x=c.read_exact('VALUE: ');f=c.read_int('FREQUENCY: ')
    if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
    rows[index]=(x,f)
    return rows


def read_frequency_rows():
    print('EXACT VALUES, NOT CLASS LIMITS')
    rows=[]
    for i in range(c.read_size('NUMBER OF ROWS: ',c.MAX_ROWS)):
        x=c.read_exact('VALUE: '); f=c.read_int('FREQUENCY: ')
        if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
        rows.append((x,f))
    return rows


def probe_summary(size):
    values=[(i,1) for i in range(size)]
    stats=c.call('STDMATH1','descriptive',values)
    print('RAW '+str(size)+' MEAN='+c.exact_text(stats['MEAN']))
    return stats['MEAN']
