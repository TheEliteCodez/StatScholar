# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

import unittest
from fractions import Fraction
from unittest.mock import patch
from test_expansion import flow
import STAT1 as app
import STCORE as c
import STDICE as dice
import STVENN as venn
import STFIND as find
import STWORDS as words
import STPROB as prob


class Quiz4(unittest.TestCase):
    def test_two_dice_isolated_imports_and_release(self):
        import subprocess,sys
        code="""
import builtins,contextlib,io,sys
import STAT1,STCORE
STCORE.view=lambda *args:None
for repeat in range(3):
 pending=iter(['3','4','1','2','1','7','3','1','2','0','0','0','0','0'])
 seen=set()
 def read(prompt=''):
  assert not {'STEXPER','STMDICE','STSTUDY','STCOUNT','STCOMB'}.intersection(sys.modules)
  seen.update(set(STCORE.TOPIC_MODULES).intersection(sys.modules))
  return next(pending)
 builtins.input=read
 with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
 assert list(pending)==[]
 assert 'STDICE' in seen and 'STPAGE' in seen
 assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_dice_subsets_match_counts(self):
        cases=[(('sum','=',3),None,'AND',2),(('sum','=',7),None,'AND',6),
               (('sumodd','=',0),None,'AND',18),(('sumeven','=',0),None,'AND',18),
               (('sum','=',3),('sum','=',7),'OR',8),(('anyeven','=',0),None,'AND',27),
               (('face','=',3),None,'AND',11)]
        for a,b,op,count in cases:
            outcomes=list(dice.pair_outcomes(a,b,op))
            self.assertEqual(len(outcomes),count)
            self.assertEqual(len(set(outcomes)),count)
            self.assertEqual(Fraction(*dice.pair_probability(a,b,op)),Fraction(count,36))
        self.assertEqual(dice.dice_event_count(5,'5'),4651)

    def test_dice_home_matching_pairs(self):
        out,_=flow(app.main,(['3','4','1','2','1','7','3','1','2','1','0','0','0'])+['0', '0'])
        self.assertIn('11/36',out)
        self.assertIn('(3,3)',out)
        self.assertIn('ENTER/1 NEXT',out)
        out,_=flow(app.main,(['3','4','1','2','1','10','1','2','1','0','0','0'])+['0', '0'])
        self.assertIn('PAGE 2/',out)
        self.assertIn('3/4',out)

    def test_multi_dice_count_of_face_any_wording(self):
        import STMDICE as multi
        # At least 2 fours of 3 dice: 16/216 = 2/27.
        out,_=flow(lambda:multi.solver_multi_dice(3),['15','4','4','2','1','0'])
        self.assertIn('P=0.0741',out)
        self.assertIn('SUCCESSFUL=16',out)
        # At most 1 four of 3 dice: 200/216 = 25/27.
        out,_=flow(lambda:multi.solver_multi_dice(3),['15','4','2','1','1','0'])
        self.assertIn('P=0.9259',out)
        self.assertIn('SUCCESSFUL=200',out)

    def test_selection_exact_changed_inputs_and_limits(self):
        self.assertEqual(Fraction(*venn.all_probability(450,238,3,False)),Fraction(238,450)*Fraction(237,449)*Fraction(236,448))
        self.assertEqual(Fraction(*venn.all_probability(450,238,3,True)),Fraction(238,450)**3)
        self.assertEqual(venn.all_probability(10,2,3,False),(0,1))
        self.assertEqual(venn.all_probability(10,2,0,False),(1,1))
        self.assertEqual(venn.regions(100,40,30,10),(10,30,20,40))
        with self.assertRaises(ValueError):venn.regions(100,40,30,50)

    def test_venn_home_reuses_counts(self):
        out,prompts=flow(app.main,(['3','10','450','184','238','123','1','5','1','2','0','3','1','5','3','1','0','0','0'])+['0'])
        for text in ['A ONLY=61','NEITHER=151','A OR B=299','184+238-123=299','0.1356','0.6685','0.1471','0.1479']:
            self.assertIn(text,out)
        self.assertEqual(prompts.count('TOTAL PEOPLE / ITEMS: '),1)
        self.assertNotIn('POPULATION TOTAL: ',prompts)

    def test_existing_table_reuses_group_total(self):
        with patch.object(prob,'read_two_way',return_value=(['C','NOT C'],['R','NOT R'],[[123,61],[115,151]])):
            out,prompts=flow(prob.two_way_session,['S','3','3','1','0','0'])
        self.assertIn('WITHOUT REPLACEMENT=0.1471',out)
        self.assertNotIn('NUMBER IN TARGET GROUP: ',prompts)

    def test_search_and_words_routes(self):
        for query,gid in [('venn','X:venn'),('compost recycle','X:venn'),('cumbersome','X:all'),('5%','X:all'),('sum odd','X:dice'),('quiz 4','X:quiz4')]:
            self.assertIn(gid,[gid for label,gid in find.search_methods(query)])
        out,_=flow(lambda:words.words_menu({}),['N','N','N','1','450','184','238','123','0','0'])
        self.assertIn('VENN / SAME COUNTS',out)
        # Search result dispatch, rather than merely matching an index entry.
        with patch.object(find,'GUIDES',{},create=True):
            out,_=flow(find.search_words,['cumbersome','1','450','238','3','1','0','0'])
        self.assertIn('0.1471',out)

    def test_guideline_boundary(self):
        for n,answer in [('5','YES'),('6','NO')]:
            out,_=flow(lambda:venn.selection_session(100,50),[n,'1','0'])
            self.assertIn('WITHIN 5% GUIDELINE='+answer,out)


if __name__=='__main__': unittest.main()
