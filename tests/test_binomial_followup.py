# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

import contextlib
from fractions import Fraction
import io
from math import comb
import unittest
from unittest.mock import patch
import STCORE as c
import STBWORD as wording
import STBINFO as info


class BinomialFollowup(unittest.TestCase):
    def test_quantiles_against_exact_distribution(self):
        for n in (0,1,4,10,39):
            for p in ((0,1),(1,20),(1,2),(63,100),(1,1)):
                probabilities=[Fraction(comb(n,k))*Fraction(*p)**k*(1-Fraction(*p))**(n-k) for k in range(n+1)]
                expected=[]
                for q in (Fraction(1,4),Fraction(3,4)):
                    total=0
                    for k,value in enumerate(probabilities):
                        total+=value
                        if total>=q:
                            expected.append(k)
                            break
                self.assertEqual(info.binomial_quartiles(n,p),tuple(expected))

    def test_stats_cutoff_and_distinct_unusual_rules(self):
        lines=info.followup(10,(1,20),('=',1,0),(3151247048623047,10**16))
        for value in ('MEAN=0.5000','VARIANCE=0.4750','SD=0.6892',
                      'MIN USUAL=-0.8784','MAX USUAL=1.8784',
                      'z=0.7255','2 SD: NOT UNUSUAL','EVENT UNUSUAL=NO',
                      'LOWER FENCE=-1.5','UPPER FENCE=2.5'):
            self.assertIn(value,lines)
        lines=info.followup(4,(1,2),('[]',0,4),(1,1))
        self.assertIn('LOWER CUTOFF=0',lines)
        self.assertIn('UPPER CUTOFF=4',lines)
        self.assertIn('z=-2.0000',lines)
        self.assertIn('z=2.0000',lines)
        self.assertEqual(lines.count('2 SD: NOT UNUSUAL'),2)
        self.assertIn('z=DNE (SD=0)',info.followup(10,(0,1),('=',0,0),(1,1)))

    def test_answer_next_page_stats_previous_page_answer(self):
        # Real viewer, physical arrows. No data re-entry to see the second page.
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[1,2,9,9],create=True),patch('builtins.input',side_effect=['10','.05','1']) as entry,contextlib.redirect_stdout(io.StringIO()) as output:
            wording.wording_session('=')
        text=output.getvalue()
        self.assertEqual(entry.call_count,3)
        self.assertEqual(text.count('ANSWER=0.3151'),2)
        self.assertIn('1-7/7',text)
        self.assertIn('MEAN=0.5000',text)
        self.assertIn('MAX USUAL=1.8784',text)

    def test_all_wordings_get_followup_pages(self):
        for op,event_input in [('=',['1']),('<=',['1']),('>=',['1']),('<',['1']),('>',['1']),('one',[]),('[]',['1','3','1'])]:
            views=[]
            with patch.object(c,'HAS_KEYS',False),patch.object(c,'view',side_effect=lambda title,lines:views.append(list(lines))),patch('builtins.input',side_effect=['10','.05']+event_input+['0']),contextlib.redirect_stdout(io.StringIO()):
                wording.wording_session(op)
            self.assertTrue(views[0][0].startswith('ANSWER='))
            self.assertEqual(views[1][0],'MEAN / SD / USUAL LIMITS')
            lines=[line for page in views for line in page]
            self.assertIn('LOWER FENCE=-1.5',lines)
            self.assertIn('REQUESTED EVENT / PROBABILITY',lines)


if __name__=='__main__': unittest.main()
