# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

"""Course-driven UI, probability, source records and import regressions."""
import contextlib
from decimal import Decimal,localcontext
import io
import math
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_expansion import flow,raw
import STAT1 as app
import STCORE as c
import STBWORD as w
import STBMATH as bm
import STDICE as dice
import STQUEST as questions
import STFIND as find
import STDMATH as data
import STHIST as hist
import STNORM as normal
import STPROB as prob


class Course(unittest.TestCase):
    def test_primary_binomial_translation_matrix(self):
        for choice,cutoff,want,command in [('1','2','0.3750','binompdf(4,0.5,2)'),('2','2','0.6875','binomcdf(4,0.5,2)'),('4','2','0.3125','binomcdf(4,0.5,1)'),('3','2','0.6875','1-binomcdf(4,0.5,1)'),('5','2','0.3125','1-binomcdf(4,0.5,2)')]:
            out,prompts=flow(app.main,['2',choice,'4','.5',cutoff,'3','0','0'])
            self.assertIn('ANSWER='+want,out);self.assertIn(command,out)
            self.assertEqual(prompts[:3],['> ','> ','TRIALS n: '])
        out,_=flow(app.main,['2','6','4','.5','1','3','1','3','0','0'])
        self.assertIn('ANSWER=0.8750',out)
        self.assertIn('binomcdf(4,0.5,3) - binomcdf(4,0.5,0)',out)
        out,_=flow(app.main,['2','7','4','.5','0','0'])
        self.assertIn('ANSWER=0.9375',out)

    def test_multipart_course_once_per_np(self):
        fixtures=[('18','.08',[('1','3'),('4','3'),('3','3'),('6','2','5','1')],['.1196','.8298','.1702','.4260']),
                  ('39','.63',[('1','24'),('2','25'),('3','23'),('6','19','26','1')],['.1281','.6158','.7560','.7122']),
                  ('50','.75',[('1','40'),('2','41'),('3','39'),('6','36','43','1')],['.0985','.9084','.3816','.7287'])]
        for n,p,events,expected in fixtures:
            inputs=['2',events[0][0],n,p]+list(events[0][1:])+['1']
            for event in events[1:-1]: inputs+=list(event)+['1']
            inputs+=list(events[-1])+['0','0']
            out,prompts=flow(app.main,inputs)
            for answer in expected:self.assertIn('ANSWER=0'+answer,out)
            self.assertEqual(prompts.count('TRIALS n: '),1)
            self.assertEqual(prompts.count('CHANCE p (DECIMAL OR %): '),1)

    def test_metra_packaging_tornado_with_independent_oracle(self):
        for n,p,key,r,want in [(60,'.74','2',38,'.0447'),(700,'.68','3',521,'.0001'),(11,'.04','4',4,'.9993')]:
            out,_=flow(app.main,['2',key,str(n),p,str(r),'2','0','0'])
            self.assertIn('ANSWER=0'+want,out)
        with localcontext() as ctx:
            ctx.prec=70
            p=Decimal('.68')
            oracle=sum(Decimal(math.comb(700,k))*p**k*(1-p)**(700-k) for k in range(521,701))
            exact=bm.binomial_exact_event(700,(17,25),('>=',521,0))
            self.assertLess(abs(Decimal(exact[0])/exact[1]-oracle),Decimal('1e-65'))
        self.assertEqual(c.fixed(exact,4),'0.0001')
        self.assertIn('SOURCE .0002 IS INCORRECT',questions.get_record('PT002')['mistake'])

    def test_context_narrowing_and_no_blind_binomial(self):
        out,_=flow(app.main,['1','3','1','39','.63','23','3','0','0','0'])
        self.assertIn('AT LEAST: X>=r',out)
        self.assertIn('1-binomcdf(39,0.63,22)',out)
        out,_=flow(app.main,['1','N','1','2','3','0','.904','1','.047','2','.049','1','0','0','0'])
        self.assertIn('P=0.0960',out)
        out,_=flow(app.main,['1','N','2','8','3','2','5','1','0','0','0'])
        self.assertIn('5/14',out);self.assertIn('15/28',out);self.assertIn('3/28',out)

    def test_given_airline_table_once(self):
        inputs=['1','7','1','2','2','PODUNK','UPSTATE','ON TIME','LATE','33','6','43','5','2','1','1','0','0','0']
        out,prompts=flow(app.main,inputs)
        for text in ('COLUMN GIVEN ROW=0.8958','P(BOTH)=0.4943','P(OR)=0.9310','P(COLUMN)=0.8736','TWO COLUMN REPLACED=0.7631','TWO COLUMN NOT REPLACED=0.7618','INDEPENDENT=NO'):
            self.assertIn(text,out)
        self.assertEqual(prompts.count('ROW COUNT (NO TOTAL): '),1)

    def test_q1_and_median_word_routes(self):
        men=[120,77,89,97,124,68,72,96];women=[115,86,49,56,78,76,78,95]
        for key,values,expected in [('6',men,'Q1=74.5000'),('7',women,'MEDIAN=78.0000')]:
            out,_=flow(app.main,['1','N',key,'8']+[str(x) for x in values]+['1','0','0','0'])
            self.assertIn(expected,out)
        a=data.descriptive(raw(men));b=data.descriptive(raw(women))
        self.assertEqual(a['SAMPLE VARIANCE s^2'],(3489,8))
        self.assertAlmostEqual(b['SAMPLE SD Sx'],20.84252178326112)
        self.assertEqual(normal.z_value((2834,10),(260,1),(26,1)),(9,10))

    def test_dice_course_events_and_ui(self):
        cases=[(('sum','=',6),None,'AND',(5,36)),(('first','=',2),None,'AND',(1,6)),(('even','=',0),None,'AND',(1,4)),(('doubles','=',0),('even','=',0),'AND',(1,12)),(('doubles','=',0),('even','=',0),'OR',(1,3)),(('first','=',2),('second','=',2),'AND',(1,36))]
        for a,b,join,want in cases:self.assertEqual(dice.pair_probability(a,b,join),want)
        out,_=flow(app.main,['3','4','1','2','3','4','5','1','0','0'])
        self.assertIn('FRACTION=1/3',out)
        out,_=flow(app.main,['3','4','1','5','5','3','5','1','0','0'])
        self.assertIn('P=0.5981',out);self.assertIn('P(NOT FACE)=5/6',out)
        # Changed numbers, first and second positions stay distinct.
        self.assertEqual(dice.pair_probability(('first','=',4),('sum','<=',6)),(1,18))

    def test_grouped_fixture_and_changed_data(self):
        rows=[((x,1),f) for x,f in zip(range(10,22),[1,3,7,18,10,4,2,7,16,10,6,2])]
        for width,count,want in [(3,4,[11,32,25,18]),(2,6,[4,25,14,9,26,8])]:
            self.assertEqual([r[2] for r in hist.grouped_rows(rows,(10,1),(width,1),count)],want)
        self.assertEqual([r[2] for r in hist.grouped_rows([((1,1),7),((3,1),9)],(1,1),(2,1),2)],[7,9])

    def test_search_methods_and_practice_records(self):
        for text,token,qid in [('38 or fewer','<=','PT001'),('at least 521','>=','PT002'),('fewer than 4','<',None),('19 through 26','[]',None),('given Democrat','given',None)]:
            self.assertEqual(find.search_methods(text)[0][1],'W:'+token)
            if qid:self.assertIn(qid,[q for q,title in questions.search_questions(text)])
        self.assertEqual(find.recognition('no fewer than 4'),'>=')
        for text,qid in [('39 students','Q043'),('tornado','Q046'),('eagles','Q044'),('chickenpox','Q034')]:
            self.assertIn(qid,[q for q,title in questions.search_questions(text)])
        self.assertIn('PT021',[q for q,title in questions.search_questions('without replacement')])
        for qid in list(app.QUESTION_INDEX)+['PT'+str(i).zfill(3) for i in range(1,25)]:
            record=questions.get_record(qid)
            for field in ('id','title','description','words','methods','parameters','event','command','answer','mistake','completeness'):
                self.assertTrue(record[field],(qid,field))
        for qid in ('Q007','Q011','Q012','Q038','Q047','Q049'):
            self.assertIn('partial',questions.get_record(qid)['completeness'])
        self.assertIn('missing',questions.get_record('PT014')['completeness'])
        out,_=flow(app.main,['PT001','2','4','0','0'])
        self.assertIn('binomcdf(60,.74,38)',out)

    def test_discrete_endpoint_translation(self):
        # Fractional cutoffs use integer boundaries without floating rounding.
        self.assertEqual(w.translation(4,(1,2),('>=',(30000000000000001,10000000000000000),0))[2],'1-binomcdf(4,0.5,3)')
        self.assertEqual(w.translation(4,(1,2),('()',1,3))[2],'binomcdf(4,0.5,2) - binomcdf(4,0.5,1)')
        self.assertEqual(w.translation(4,(1,2),('=',(3,2),0))[2],'0')

    def test_binomial_and_dice_do_not_import_counting_ui(self):
        code="""
import sys,builtins,contextlib,io
import STAT1,STCORE
STCORE.view=lambda *args:None
cases=[(['2','3','39','.63','23','0','0'],'TRIALS n: '),(['3','4','1','2','3','4','5','1','0','0'],'HOW MANY FAIR 6-SIDED DICE: ')]
for repeat in range(5):
 for answers,entry in cases:
  pending=iter(answers)
  def read(prompt=''):
   if prompt==entry:
    assert 'STCOUNT' not in sys.modules
    assert 'STBINOM' not in sys.modules
    assert not any(name.startswith('STPT') or name.startswith('STQ') for name in sys.modules)
   return next(pending)
  builtins.input=read
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[]
  assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
print('ISOLATION PASS')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=20,cwd=Path(__file__).resolve().parent.parent)
        self.assertEqual(run.returncode,0,run.stderr)


if __name__=='__main__':unittest.main()
