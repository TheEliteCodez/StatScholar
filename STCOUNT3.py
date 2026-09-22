# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Distribution-table task loop; helpers load back through the dispatcher.
import STCORE as c


def distribution_session(rows=None, approximate=False, source=None, first_word=None):
    if rows is None:
        rows, approximate = c.call('STCOUNT', 'read_distribution')
    while True:
        key = '1' if first_word else c.menu('R02-R06 TABLE TASK', [('1', 'EVENT PROBABILITY'), ('2', 'MEAN / VAR / SD'), ('3', 'X>=1 BY COMPLEMENT'), ('4', 'UNUSUAL EVENT'), ('5', 'CHECK / SHOW TABLE'), ('6', 'EXACT BINOMIAL MODEL'), ('7','CHANGE DATA'),('8','MARK TABLE AS ROUNDED'),('9','BAR HEIGHTS / DRAWING STEPS')])
        if key == '0':
            return
        if key == '9':
            c.call('STCOUNT7', 'heights_page', rows, approximate)
            continue
        if key == '8':
            approximate=True
            continue
        if key == '7':
            if source=='sample':
                rows = c.call('STCOUNT', 'read_sample_distribution')
                approximate=False
            else:
                rows,approximate = c.call('STCOUNT', 'read_distribution', approximate)
            continue
        if key == '6':
            c.call('STBWORD','wording_session')
            continue
        note = ['ENTERED P TOTAL=' + c.exact_text(c.rsum([p for x, p in rows]))]
        if approximate:
            note += ['ROUNDED TABLE: APPROXIMATE P', 'EXACT ANSWER UNAVAILABLE', 'ROUNDED ZERO NEED NOT BE IMPOSSIBLE', 'NO AUTOMATIC NORMALIZATION', 'USE MODEL IF ITS ASSUMPTIONS APPLY']
        if key == '2':
            if approximate or c.rsum(p for x,p in rows)!=(1,1):
                c.view('ROUNDED TABLE / TOTAL', note + ['EXACT MOMENTS REQUIRE KNOWN P SUMMING TO 1.', 'OPTION 8 MARKS ROUNDED INPUT.', 'OPTION 6: BINOMIAL ONLY IF JUSTIFIED.'])
                continue
            mean, var, sd = c.call('STCOUNT', 'distribution_moments', rows)
            c.results('R02/R03', [('mu', mean), ('VAR', var), ('sigma', sd)], note + ['mu=SUM(x*P(x))', 'VAR=SUM(x^2*P)-mu^2', 'SD=SQRT(VAR)'])
        elif key == '5':
            c.call('STCOUNT7', 'check_table', rows, note, approximate)
        else:
            counts_only = all((x[1] == 1 and x[0] >= 0 for x, p in rows))
            if first_word:
                ev=c.call('STBWE','read_event',first_word)
                first_word=None
            else:
                ev = (('=', 0, 0) if counts_only else ('<', 1, 0)) if key == '3' else c.event_input()
            if ev is None:
                continue
            p = c.call('STCOUNT', 'table_probability', rows, ev)
            if key == '3':
                p = c.radd((1, 1), (-p[0], p[1]))
            if key == '4' and (not approximate):
                c.call('STCOUNT', 'unusual_result', p)
            else:
                selected = [c.exact_text(x) for x, q in rows if c.event_match(x, *ev)]
                c.results('R04 TABLE EVENT', [('P APPROX' if approximate else 'P', p)], note + (['P=1-P(0)' if counts_only else 'P(X>=1)=1-P(X<1)'] if key == '3' else ['ADD MATCHING ROWS']) + ['ROWS: ' + ','.join(selected)])
