# Author: Gregory King
"""Expansion arithmetic, navigation, and lifecycle acceptance checks."""
import contextlib
import io
import math
from pathlib import Path
import statistics
import subprocess
import sys
import unittest
from fractions import Fraction
from unittest.mock import patch
import test_support
import STCORE as c
d = test_support.s
ref = test_support.s
import STAT1 as app
import STPROB as prob
import STBINOM as binom


def raw(seq): return c.exact_sorted(c.as_ratio(x) for x in seq)
def f(x): return Fraction(*x)


def flow(fn, inputs):
    pending=iter(inputs); outputs=[]; prompts=[]
    def read(prompt=''):
        prompts.append(prompt)
        return next(pending)
    with patch('builtins.input',side_effect=read), patch.object(c,'view',side_effect=lambda title,lines:outputs.append((title,list(lines)))),contextlib.redirect_stdout(io.StringIO()) as screen:
        fn()
    if list(pending): raise AssertionError('Unused inputs')
    return str(outputs)+screen.getvalue(),prompts


class Expansion(unittest.TestCase):
    def test_summary_odd_even_modes_and_singleton(self):
        a=d.descriptive(raw([1,2,3,4]))
        self.assertEqual([f(a[k]) for k in ('SUM','MEAN','Q1','MEDIAN','Q3','RANGE','IQR','MIDRANGE')],[10,Fraction(5,2),Fraction(3,2),Fraction(5,2),Fraction(7,2),3,2,Fraction(5,2)])
        self.assertEqual(f(a['SAMPLE VARIANCE s^2']),Fraction(5,3))
        self.assertAlmostEqual(a['SAMPLE SD Sx'],math.sqrt(5/3))
        self.assertEqual(a['MODE'],'DNE')
        self.assertEqual(d.quartiles(raw([1,2,3,4,5])),((3,2),(3,1),(9,2)))
        self.assertEqual(d.descriptive(raw([1,1,2,2,3]))['MODE'],'1,2')
        self.assertEqual(d.descriptive(raw([1,1,2,2,3,3,4]))['MODE'],'1,2,3')
        self.assertEqual(d.descriptive(raw([2,2,2]))['SAMPLE SD Sx'],0)
        self.assertEqual(d.descriptive(raw([2]))['SAMPLE VARIANCE s^2'],'DNE')

    def test_course_fixtures_and_ti_quartile_example(self):
        # Previously supplied delivery/rain data; expand only in desktop fixtures.
        deliveries=raw([3]+[6]*2+[9]*6+[12]*5)
        rain=raw([6]*5+[7]*6+[8]*3+[9]*4+[10]*2)
        self.assertEqual(d.descriptive(deliveries)['MEAN'],(129,14))
        self.assertEqual(d.quartiles(rain),((13,2),(7,1),(9,1)))
        self.assertEqual(d.descriptive(rain)['MODE'],'7')
        # TI knowledge-base 12185 published list, not reconstructed course data.
        values=raw([14,29,32,38,41,45,68,71,74,83,86,87])
        self.assertEqual(d.quartiles(values),((35,1),(113,2),(157,2)))

    def test_25_50_100_values(self):
        for n in (25,50,100):
            values=list(range(n))
            stats=d.descriptive(raw(values))
            self.assertEqual(stats['n'],n)
            self.assertEqual(f(stats['MEAN']),Fraction(n-1,2))
            self.assertAlmostEqual(c.number(stats['SAMPLE VARIANCE s^2']),statistics.variance(values))
            with patch('builtins.input',side_effect=[str(n)]+[str(x) for x in reversed(values)]),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(d.read_raw(),raw(values))

    def test_compare_centers_and_spreads(self):
        a,b=d.comparison(raw([1,2,3]),raw([2,4,6]))
        for key in ('MEAN','MEDIAN','RANGE','IQR'):
            self.assertEqual(f(b[key]),2*f(a[key]))
        self.assertEqual(b['SAMPLE SD Sx'],2*a['SAMPLE SD Sx'])
        self.assertEqual(f(b['SAMPLE VARIANCE s^2']),4*f(a['SAMPLE VARIANCE s^2']))

    def test_normal_and_relative(self):
        self.assertEqual(d.z_value((44,1),(40,1),(4,1)),(1,1))
        self.assertEqual(d.x_value((1,1),(40,1),(4,1)),(44,1))
        self.assertEqual([d.x_value((z,1),(40,1),(4,1))[0] for z in range(-3,4)],[28,32,36,40,44,48,52])
        out,prompts=flow(d.normal_session,['1','40','4','44','1','2','-2','1','3','1','46','1','','0'])
        self.assertIn('x=32.0000',out)
        self.assertIn('BETWEEN z=1 AND 2',out)
        self.assertEqual(prompts.count('MEAN: '),1)
        out,_=flow(d.relative_session,['44','40','4','70','50','10','1','0'])
        self.assertIn('HIGHER RELATIVE=B',out)

    def test_empirical_all_regions(self):
        for k,within in enumerate([68,95,Fraction(997,10)],1):
            self.assertEqual(f(d.empirical_percent(k)),within)
            self.assertEqual(f(d.empirical_percent(k,'outside')),100-within)
            self.assertEqual(f(d.empirical_percent(k,'tail')),(100-within)/2)
        out,_=flow(d.empirical_session,['7','2','1','5','1','0'])
        self.assertIn('APPROX PERCENT=2.5000',out)
        self.assertIn('APPROX NORMAL',out)

    def test_boxplots_shared_quartiles_and_fences(self):
        for values in ([1,2,3,4,5],[1,2,3,4,5,6,100]):
            xs=raw(values); box=d.boxplot_values(xs); stats=d.descriptive(xs)
            self.assertEqual(box[:3],d.quartiles(xs))
            self.assertEqual(box[3],stats['IQR'])
        box=d.boxplot_values(raw([1,2,3,4,5,6,100]))
        self.assertEqual(box[6:8],((1,1),(6,1)))
        self.assertEqual(box[8],[(100,1)])
        self.assertEqual(d.boxplot_values(raw([1,2,3,4,5]))[8],[])
        out,_=flow(d.boxplot_session,['2','1','2','4','6','100','5','1'])
        self.assertIn('REQUIRE RAW DATA',out)

    def test_dotplot_gaps(self):
        self.assertEqual(d.dotplot_rows(raw([20,22,22])),[((20,1),1),((21,1),0),((22,1),2)])
        self.assertEqual(d.dotplot_rows(raw(['.1','.1','.3'])),[((1,10),2),((3,10),1)])

    def test_grouped_raw_and_weighted_without_expansion(self):
        rows=d.grouped_rows(d.value_counts(raw([0,1,2,3])),(0,1),(2,1),2)
        self.assertEqual([r[2:] for r in rows],[(2,(1,2),2),(2,(1,2),4)])
        rows=d.grouped_rows([((0,1),1000000),((2,1),2000000)],(0,1),(2,1),2)
        self.assertEqual(rows[1][2:],(2000000,(2,3),3000000))
        rows=d.grouped_rows([((0,1),1),((1,1),1),((2,1),1)],(0,1),(1,1),2,True)
        self.assertEqual([r[2] for r in rows],[1,2])
        out,_=flow(d.histogram_session,['4','2','2','0','2','2','3','2','0','1','2','0'])
        self.assertIn('LIMITS 0 TO 1',out);self.assertIn('BOUNDARIES -0.5 TO 1.5',out)
        self.assertIn('CUM=5',out)

    def test_histogram_probability_and_reuse(self):
        out,prompts=flow(d.histogram_session,['1','4','0','1','2','3','1','4','2','0','1','2','0'])
        self.assertEqual(prompts.count('NUMBER OF VALUES (1..100): '),1)
        self.assertIn('LIMITS 2 TO 3',out)
        out,_=flow(d.histogram_session,['3','2','0','.4','1','.6','5','1','0'])
        self.assertIn('BAR HEIGHT=P(x)',out)

    def test_study_classifiers(self):
        # Definition pager uses ordinary input; final 0 closes it.
        for answers,want in [(['Y','0'],'PARAMETER'),(['N','0'],'STATISTIC')]:
            out,_=flow(ref.parameter_classifier,answers);self.assertIn(want,out)
        for answers,want in [(['Y','0'],'EXPERIMENT'),(['N','0'],'OBSERVATIONAL')]:
            out,_=flow(ref.experiment_classifier,answers);self.assertIn(want,out)
        for index,name in enumerate(('CONVENIENCE','SYSTEMATIC','STRATIFIED','CLUSTER','SIMPLE RANDOM','RANDOM SAMPLE')):
            out,_=flow(ref.sampling_menu,['1']+['N']*index+['Y','0'])
            self.assertIn(name,out)
        out,_=flow(ref.population_classifier,['0','3','0'])
        self.assertIn('NEED THE GROUP',out)
        out,_=flow(ref.significance_menu,['3','.01','.05','1'])
        self.assertIn('STATISTICALLY SIGNIFICANT=YES',out)
        self.assertIn('NEED EFFECT SIZE',out)

    def test_probability_concepts_and_at_least_one(self):
        for p,want in [('0','IMPOSSIBLE'),('1','CERTAIN'),('.5','POSSIBLE'),('-1','INVALID')]:
            self.assertEqual(prob.probability_class(c.as_ratio(p)),want)
        out,_=flow(binom.binomial_session,['25','.03','1','7','5','1','0'])
        self.assertIn('P=0.5330',out)
        self.assertIn('1-binomcdf(n,p,0)',out)
        out,_=flow(prob.supplied_session,['.6','.4','.2','1'])
        self.assertIn('P(NOT A)=0.4000',out);self.assertIn('P(NOT B)=0.6000',out)

    def test_search_language(self):
        cases={'shortest 25%':'S06','half are below':'S13','usual':'S10','statistically high':'S12','at least one':'P09','no more than':'B03','without replacement':'R07','every 10th':'D05','easiest people':'D05','sample every group':'D05','select classrooms':'D05','treatment':'D06','bell shaped':'G08'}
        for query,gid in cases.items():
            self.assertIn(gid,[g for label,g in ref.search_methods(query)],query)
        self.assertEqual(ref.search_methods('quartile')[0][1],'S13')
        self.assertTrue(all(any(gid==g for _,g,_ in ref.SEARCH_METHODS) for gid in ('G04','G05','G06','G07','G08','G09','F08')))

    def test_new_guides_and_menu_navigation(self):
        for gid in app.NEW_ROUTES:
            guide=app.get_guide(gid)
            self.assertEqual(guide['title'],app.GUIDES[gid][0])
            self.assertEqual(guide['solver'],gid)
        # Real data entry begins after the advertised menu choices.
        out,prompts=flow(app.main,['4','1','3','1','2','3','1','0','0'])
        self.assertIn('MEAN=2.0000',out)
        self.assertEqual(prompts[:3],['> ','> ','NUMBER OF VALUES (1..100): '])
        out,prompts=flow(app.main,['5','1','1','40','4','44','1','0','0'])
        self.assertEqual(prompts[:4],['> ','> ','> ','MEAN: '])
        self.assertIn('z=1.0000',out)
        out,_=flow(app.main,['5','1','4','2','1','0','0','0'])
        self.assertIn('APPROX PERCENT=95.0000',out)

    def test_raw_session_reuses_list(self):
        out,prompts=flow(d.raw_session,['3','1','2','3','1','2','3','1','0','4','1','0'])
        self.assertEqual(prompts.count('NUMBER OF VALUES (1..100): '),1)
        self.assertIn('z=1.0000',out)
        self.assertIn('LOW WHISKER=1.0000',out)

    def test_reference_callbacks_do_not_overwrite_local_functions(self):
        for name in ('ti84_methods','wizard_formula','browse_matrix','question_starters'):
            flow(lambda:app.reference_call(name),['0'])

    def test_graph_import_isolation_and_nested_cleanup(self):
        code="""
import sys,builtins,io,contextlib
import STAT1,STCORE
assert 'STQUEST' not in sys.modules
assert 'STDMATH' not in sys.modules
pending=iter(['5','1','1','40','4','44','1','0','0'])
def read(prompt=''):
 if prompt=='MEAN: ':
  assert 'STNORM' in sys.modules
  assert not {'STDESC','STDATA','STGRAPH','STHIST','STDMATH','STQUEST'}.intersection(sys.modules)
 return next(pending)
builtins.input=read
STCORE.view=lambda *args:None
with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
# Search metadata completes before entering the raw solver, even in FIND.
pending=iter(['1','N','N','9','1','shortest 25%','1','2','1','3','1','0','0','0','0','0'])
def read(prompt=''):
 if prompt.startswith('NUMBER OF VALUES'):
  assert 'STFIND' in sys.modules
  assert 'STQUEST' not in sys.modules
 return next(pending)
builtins.input=read
with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
print('ISOLATED')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=20,cwd=Path(__file__).resolve().parent.parent)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('ISOLATED',run.stdout)

    def test_expansion_probe_with_home_resident(self):
        code="import EVOPROBE; EVOPROBE.expansion_probe()"
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=20,cwd=Path(__file__).resolve().parent.parent)
        self.assertEqual(run.returncode,0,run.stderr)
        for text in ('RAW 25 MEAN=12','RAW 50 MEAN=24.5','RAW 100 MEAN=49.5','NORMAL z=1: True'):
            self.assertIn(text,run.stdout)

    def test_new_session_modules_reclaimed(self):
        code="""
import sys,io,contextlib,weakref
import STAT1,STCORE
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
for repeat in range(5):
 refs=[]
 def capture(title,lines):
  refs.extend(weakref.ref(sys.modules[n]) for n in STCORE.TOPIC_MODULES if n in sys.modules)
 STCORE.view=capture
 cases=[['4','1','3','1','2','3','1','0','0'],['5','1','4','2','1','0','0','0'],['1','N','N','9','1','shortest 25%','1','2','1','3','1','0','0','0','0','0']]
 for answers in cases:
  pending=iter(answers)
  import builtins
  builtins.input=lambda prompt='':next(pending)
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[]
  assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
 assert all(ref() is None for ref in refs)
print('PASS')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=20,cwd=Path(__file__).resolve().parent.parent)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('PASS',run.stdout)


if __name__=='__main__': unittest.main()
