import contextlib
from fractions import Fraction
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_expansion import flow
import STCORE as c
import STPROB1 as solver
import STPROBM


class ConditionalSolver(unittest.TestCase):
    def test_direct_and_reverse_given_only_collect_required_values(self):
        cases=[(['1','1','1','.4','.2','1','0'],'P(A|B)=0.5000'),
               (['1','2','1','.6','.2','1','0'],'P(B|A)=0.3333'),
               (['1','1','2','40','20','1','0'],'P(A|B)=0.5000'),
               (['2','1','.4','.5','1','0'],'P(A AND B)=0.2000'),
               (['2','2','.6','1/3','1','0'],'P(A AND B)=0.2000')]
        for inputs,answer in cases:
            out,prompts=flow(solver.solver_conditional,inputs)
            self.assertIn(answer,out)
            self.assertIn('GIVEN GROUP IS',out)
            self.assertEqual(len([p for p in prompts if p!='> ']),2)

    def test_equivalent_given_models_produce_same_union_intersection_and_conditionals(self):
        for given in [['3','.6','.4','.2'],['4','.6','.4','.8'],
                      ['5','.6','.4','.5'],['6','.6','.4','1/3'],
                      ['7','100','60','40','20']]:
            out,_=flow(solver.solver_conditional,given+['1','1','0','0'])
            for answer in ['P(A AND B)=0.2000','P(A OR B)=0.8000',
                           'P(A|B)=0.5000','P(B|A)=0.3333',
                           'P(NEITHER)=0.2000','P(EXACTLY ONE)=0.6000',
                           'P(A|NOT B)=0.6667','P(B|NOT A)=0.5000']:
                self.assertIn(answer,out)

    def test_event_masks_and_all_conditionals_against_enumerated_population(self):
        for cells in [(2,4,2,2),(0,1,3,0),(5,0,0,0),(0,0,0,7),(1,2,3,4)]:
            total=sum(cells)
            a=Fraction(cells[0]+cells[1],total)
            b=Fraction(cells[0]+cells[2],total)
            parts=solver._regions((a.numerator,a.denominator),(b.numerator,b.denominator),(cells[0],total))
            for event in range(16):
                expected=sum(Fraction(count,total) for i,count in enumerate(cells) if event&(1<<i))
                self.assertEqual(Fraction(*solver._area(parts,event)),expected)
                for group in range(16):
                    numerator=sum(count for i,count in enumerate(cells) if (event&group)&(1<<i))
                    denominator=sum(count for i,count in enumerate(cells) if group&(1<<i))
                    result=solver._given(solver._area(parts,event&group),solver._area(parts,group))
                    if denominator: self.assertEqual(Fraction(*result),Fraction(numerator,denominator))
                    else: self.assertIn('UNDEFINED',result)

    def test_compound_event_builder_and_complement_conditioning(self):
        for target,given,answer in [('1','4','0.6667'),('5','6','0.2500'),('9','3','0.5000')]:
            out,_=flow(solver.solver_conditional,
                       ['3','.6','.4','.2','2',target,'2',given,'1','0','0'])
            self.assertIn('='+answer,out)
        out,_=flow(solver.solver_conditional,
                   ['3','.6','.4','.2','2','7','1','1','0','0'])
        self.assertIn('P(A AND NOT B)=0.4000',out)

    def test_zero_given_group_is_undefined_not_zero(self):
        out,_=flow(solver.solver_conditional,['1','1','1','0','0','1','0'])
        self.assertIn('UNDEFINED (GIVEN GROUP HAS P=0)',out)

    def test_relationships_require_explicit_inputs(self):
        for mode,independent,exclusive in [('10','YES','NO'),('11','NO','YES')]:
            out,_=flow(solver.solver_conditional,[mode,'.3','.4','4','1','0','0'])
            self.assertIn('INDEPENDENT='+independent,out)
            self.assertIn('MUTUALLY EXCLUSIVE='+exclusive,out)

    def test_venn_table_and_symbol_guide(self):
        out,_=flow(solver.solver_conditional,
                   ['9','3','.6','.4','.2','3','0','0'])
        for text in ['cap B: INTERSECTION','cup B: UNION','B IS THE GIVEN GROUP',
                     'TABLE COLUMNS: B, NOT B, TOTAL','A ONLY=0.4','NEITHER=0.2']:
            self.assertIn(text,out)

    def test_impossible_marginals_overlap_are_rejected(self):
        for a,b,both in [((1,5),(1,5),(3,10)),((9,10),(9,10),(1,10))]:
            with self.assertRaises(ValueError): solver._regions(a,b,both)

    def test_probability_menu_routes_and_back_before_data(self):
        with patch.object(c,'menu',side_effect=['12','0']),patch.object(c,'call') as call:
            STPROBM.probability_tasks({})
        call.assert_called_once_with('STPROB','solver_conditional')
        out,prompts=flow(solver.solver_conditional,['1','0','1','1','0','0'])
        self.assertEqual(set(prompts),{'> '})

    def test_real_home_workflow_releases_modules(self):
        code="""
import builtins,io,contextlib,STAT1,STCORE as c
c.view=lambda *args:'exit'
for inputs in (['3','12','1','1','1','.4','.2','0','0','0'],
               ['3','12','3','.6','.4','.2','2','1','2','4','0','0','0','0']):
 for repeat in range(3):
  pending=iter(inputs)
  builtins.input=lambda prompt='':next(pending)
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[]
  assert not c.topic_modules(),c.topic_modules()
  assert c._call_depth==0
"""
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=Path(__file__).resolve().parent.parent,capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
