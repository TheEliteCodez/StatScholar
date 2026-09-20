# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

import unittest
import contextlib
import io
from unittest.mock import patch
from test_expansion import flow
import STAT1 as app
import STCOUNT as count
import STCORE as c
import STBMATH as bm
import STFIND as find


class Quiz5(unittest.TestCase):
    def test_probability_guided_none_and_overlap(self):
        out,_=flow(app.main,['3','H','5','3','4','.5','0','0','0','0'])
        self.assertIn('NONE MEANS EXACTLY ZERO',out)
        self.assertIn('ANSWER=0.0625',out)
        out,_=flow(app.main,['3','H','3','5','100','40','30','10','3','1','0','0','0'])
        self.assertIn('A OR B=0.6000',out)
        self.assertIn('A BUT NOT B=0.3000',out)

    def test_probability_then_stats_then_next_probability(self):
        out,prompts=flow(app.main,['2','1','10','.05','1','7','1','','1','2','1','0','0'])
        for answer in ['ANSWER=0.3151','MEAN=0.5000','SD=0.6892','VARIANCE=0.4750','ANSWER=0.9139']:
            self.assertIn(answer,out)
        self.assertEqual(prompts.count('TRIALS n: '),1)
        self.assertEqual(prompts.count('CHANCE p (DECIMAL OR %): '),1)

    def test_credit_card_moments_and_events(self):
        rows=[((i,1),c.as_ratio(p)) for i,p in enumerate(['.07','.68','.21','.03','.01'])]
        mean,var,sd=count.distribution_moments(rows)
        self.assertEqual(mean,(123,100));self.assertEqual(var,(4371,10000))
        self.assertAlmostEqual(sd,.6611353870426238)
        self.assertEqual(count.table_probability(rows,('<=',2,0)),(24,25))
        self.assertEqual(count.table_probability(rows,('>=',3,0)),(1,25))

    def test_rounded_input_and_invalid_total_moments(self):
        values=['0','.001','.006','.022','.061','.122','.183','.209','.183','.122','.061','.022','.006','.001','0']
        rows=[((i,1),c.as_ratio(p)) for i,p in enumerate(values)]
        out,_=flow(lambda:count.distribution_session(rows),['2','8','2','0'])
        self.assertIn('EXACT MOMENTS REQUIRE',out)
        self.assertNotIn('mu=6.993',out)
        self.assertIn('ROUNDED TABLE: APPROXIMATE P',out)
        with patch('builtins.input',side_effect=['2','0','~0.000','1','.999']),contextlib.redirect_stdout(io.StringIO()):
            parsed,rounded=count.read_distribution()
        self.assertTrue(rounded)
        self.assertEqual(parsed[0][1],(0,1))
        out,_=flow(lambda:count.distribution_session(rows,True,first_word='>='),['12','5','1','0'])
        self.assertIn('P APPROX=0.0070',out)
        self.assertIn('ENTERED P TOTAL=0.999',out)
        self.assertIn('ROUNDED ZERO NEED NOT BE IMPOSSIBLE',out)

    def test_girls_exact_model(self):
        for event,want in [(('=',10,0),'0.0611'),(('<=',4,0),'0.0898'),(('>=',10,0),'0.0898'),(('>=',12,0),'0.0065')]:
            self.assertEqual(c.fixed(bm.binomial_exact_event(14,(1,2),event),4),want)

    def test_unusual_reuses_event_and_np(self):
        out,prompts=flow(app.main,['2','2','60','.74','38','6','','5','1','1','1','38','0','0'])
        self.assertIn('UNUSUAL=YES',out)
        self.assertIn('P(EVENT)=0.0447',out)
        self.assertEqual(prompts.count('TRIALS n: '),1)
        self.assertIn('NOT THE MEAN +/- 2 SD RULE',out)
        out,_=flow(app.main,['2','2','14','.5','4','6','','1','0','0'])
        self.assertIn('UNUSUAL=NO',out)

    def test_quiz_home_and_rounded_entry(self):
        out,_=flow(app.main,['3','13','7','2','0','0.000','1','.999','2','0','0','0'])
        self.assertIn('ROUNDED TABLE: APPROXIMATE P',out)
        self.assertNotIn('mu=',out)
        for term in ['quiz 5','credit cards','rounded table','girls','merta']:
            self.assertIn('X:quiz5',[gid for label,gid in find.search_methods(term)])

    def test_payoff_no_double_subtraction(self):
        out,_=flow(count.payoff_session,['PLAYER','2','2','4','2','0','4','1','0'])
        self.assertIn('EXPECTED PROFIT=-0.67',out)


if __name__=='__main__': unittest.main()
