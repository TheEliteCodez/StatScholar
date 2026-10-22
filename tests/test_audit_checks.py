# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

"""Regression acceptance checks for source-audit findings A01-A07.
Run from project root: python -B -m unittest discover -s tests -p test_audit_checks.py
"""
import builtins
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from fractions import Fraction
from decimal import Decimal, localcontext
import math
import subprocess
import sys
import tempfile
from unittest.mock import patch

from test_support import s


def capture(function,answers):
    outputs=[];prompts=[];pending=iter(answers)
    def read(prompt=""):
        prompts.append(prompt)
        return next(pending)
    with patch.object(builtins,"input",read),patch.object(s,"view",lambda t,l:outputs.append((t,l))),contextlib.redirect_stdout(io.StringIO()):
        function()
    remaining=list(pending)
    if remaining: raise AssertionError("Unused inputs: "+repr(remaining))
    return outputs,prompts


class AuditRegressions(unittest.TestCase):
    def test_definition_pages_reach_every_wrapped_line(self):
        import STSTUDY as STREF, STCORE
        for entries in (STREF.SAMPLING_DEFINITIONS, STREF.MEASUREMENT_DEFINITIONS,
                        STREF.STUDY_DEFINITIONS):
            for title, definition in entries:
                expected = list(STCORE.wrapped_lines((definition,)))
                pages = (len(expected)+5)//6
                output = io.StringIO()
                keys = ['1' if i % 2 else 'N' for i in range(pages-1)] + ['0']
                with patch('builtins.input', side_effect=keys), contextlib.redirect_stdout(output):
                    STREF.definition_pages(title, definition)
                shown = output.getvalue()
                for line in expected:
                    self.assertIn(line, shown)
                self.assertIn('PAGE '+str(pages)+'/'+str(pages), shown)
                self.assertTrue(all(len(line)<=30 for line in expected))
        with patch('builtins.input', side_effect=['1','2','N','P','0']), contextlib.redirect_stdout(io.StringIO()) as out:
            STREF.definition_pages('LONG', ' '.join(['WORD']*70))
        self.assertEqual(out.getvalue().count('PAGE 1/'), 3)

    def test_definitions_menu_routes_and_search(self):
        import STSTUDY as STREF
        cases = [(['1','1','0','0'], 'simple random sample'),
                 (['2','3','0','0'], 'interval'),
                 (['3','4','0','0'], 'practically significant'),
                 (['4','0'], 'outlier'),
                 (['5','convienience','1','0','0'], 'convenience sample')]
        for keys, expected in cases:
            with patch('builtins.input', side_effect=keys), patch.object(STREF, 'definition_pages') as show, contextlib.redirect_stdout(io.StringIO()):
                STREF.definitions_menu()
            self.assertEqual(show.call_args.args[0], expected)



    def test_A01_range_includes_exact_lower_endpoint(self):
        # mu=96.8, sigma=4.4, hence exact lower endpoint=88.
        actual=s.usual_counts(121,.8)
        self.assertEqual(actual[4:6],(88,105),"Floating arithmetic excluded the valid count 88")

    def test_A02_at_least_one_with_negative_values(self):
        # P(X>=1)=.25, while P(X!=0)=.5; these are different events.
        rows=[(s.as_ratio(x),s.as_ratio(p)) for x,p in [('-1','.25'),('0','.5'),('1','.25')]]
        output,_=capture(lambda:s.distribution_session(rows),['3','5','1','0'])
        self.assertIn('P=0.2500',str(output))



    def test_A05_roulette_zero_label_is_not_double_zero(self):
        wheel=[(str(k),k) for k in range(1,37)]+[('0',0),('00',0)]
        selected=s.experiment_indices(wheel,'roulette','=0')
        self.assertEqual([wheel[i][0] for i in selected],['0'])


    def test_A07_exact_table_value_is_less_than_one_third(self):
        # 3333333333333333/10^16 is strictly smaller than 1/3.
        rows=[(s.as_ratio('.3333333333333333'),(1,1))]
        output,_=capture(lambda:s.distribution_session(rows),['1','3','1/3','1','0'])
        self.assertIn('P=1.0000',str(output))





    def test_range_sweep_against_independent_rational_membership(self):
        for n in range(1,151):
            for numerator in range(0,101,5):
                p=Fraction(numerator,100);mu=n*p;v=n*p*(1-p)
                valid=[k for k in range(n+1) if (k-mu)**2<=4*v]
                actual=s.usual_counts(n,(p.numerator,p.denominator))
                self.assertEqual(actual[4:6],(min(valid),max(valid)),(n,p))
        out,_=capture(s.binomial_session,['121','.8','4','1','88','1','0'])
        self.assertIn('USUAL INTEGERS=88..105',str(out))
        self.assertIn('UNUSUAL=NO',str(out))

    def test_exact_event_engine_against_decimal_oracle(self):
        with localcontext() as ctx:
            ctx.prec=80
            for n,p,a,b in [(121,'.8',88,105),(148,'.25',0,32),(39,'.63',19,26),(18,'.08',3,18)]:
                dp=Decimal(p)
                expected=sum(Decimal(math.comb(n,k))*dp**k*(1-dp)**(n-k) for k in range(a,b+1))
                got=s.binomial_exact_event(n,s.as_ratio(p),('[]',(a,1),(b,1)))
                # Use the public event code for inclusive between.
                self.assertLess(abs(Decimal(got[0])/Decimal(got[1])-expected),Decimal('1e-70'))

    def test_zero_labels_and_general_table_domains(self):
        wheel=[(str(k),k) for k in range(1,37)]+[('0',0),('00',0)]
        for expr,labels in [('=0',['0']),('=00',['00']),('0 OR 00',['0','00'])]:
            self.assertEqual(sorted(wheel[i][0] for i in s.experiment_indices(wheel,'roulette',expr)),labels)
        for expr in ['!=0','NOT 0']:
            self.assertEqual(len(s.experiment_indices(wheel,'roulette',expr)),37)
        for pairs,expected in [([('-3','255/256'),('270','1/256')],'0.0039'),
                               ([('0','.25'),('.5','.5'),('1','.25')],'0.2500')]:
            rows=[(s.as_ratio(x),s.as_ratio(p)) for x,p in pairs]
            out,_=capture(lambda:s.distribution_session(rows),['3','5','1','0'])
            self.assertIn('P='+expected,str(out))
            self.assertIn('1-P(X<1)',str(out))

    def test_exact_thresholds_sorting_and_symmetry(self):
        lo=s.as_ratio('.3333333333333333');hi=s.as_ratio('1/3')
        self.assertEqual(s.exact_sorted([hi,lo]),[lo,hi])
        out,_=capture(s.valid_probability,['1.00000000000000001','1'])
        self.assertIn('CAN BE PROBABILITY=NO',str(out))
        out,_=capture(lambda:s.unusual_result(s.as_ratio('.050000000000000001')),['','1'])
        self.assertIn('UNUSUAL=NO',str(out))
        for p,want in [('.5','YES'),('.3','NO')]:
            out,_=capture(s.symmetry_session,['20','4','16',p,'1'])
            self.assertIn('EQUAL='+want,str(out))
        self.assertEqual(s.binomial_shape(s.as_ratio('.50000000000000001')),'LEFT SKEW')


    def test_standalone_console_only_runtime_modules(self):
        with tempfile.TemporaryDirectory(prefix='stat1-check-') as folder:
            runtime=Path(folder)/'STAT1.py'
            from test_support import MODULE_NAMES
            for name in MODULE_NAMES:
                (Path(folder)/(name+'.py')).write_bytes(Path(__file__).resolve().parent.parent.joinpath(name+'.py').read_bytes())
            cases=[(['10','1','95%','','5%','','0','0'],['ROUND UP: n=385']),
                   (['11','1','60','100','95%','','','0','0','0'],['MARGIN OF ERROR=0.0960'])]
            for inputs,expected in cases:
                run=subprocess.run([sys.executable,'-B',str(runtime)],input='\n'.join(inputs)+'\n',
                                   text=True,capture_output=True,cwd=folder,timeout=10)
                self.assertEqual(run.returncode,0,run.stderr)
                for value in expected:self.assertIn(value,run.stdout.replace("\n",""))
            self.assertEqual(sorted(f.name for f in Path(folder).iterdir()),sorted(name+'.py' for name in MODULE_NAMES))


    def test_support_imports_and_calculator_style_launch(self):
        from test_support import MODULE_NAMES
        with tempfile.TemporaryDirectory(prefix='stat1-import-') as folder:
            for name in MODULE_NAMES:
                (Path(folder)/(name+'.py')).write_bytes(Path(__file__).resolve().parent.parent.joinpath(name+'.py').read_bytes())
            # Fresh interpreters catch import-order/circular-import dependencies.
            for name in MODULE_NAMES:
                run=subprocess.run([sys.executable,'-B','-c','import '+name],
                                   input='',text=True,capture_output=True,cwd=folder,timeout=10)
                self.assertEqual(run.returncode,0,run.stderr)
                self.assertEqual(run.stdout,'',name)
            # TI launches by importing. Simulate only its key API, not hardware.
            code="import sys,types; ti=types.ModuleType('ti_system'); ti.wait_key=lambda:(_ for _ in ()).throw(AssertionError('Do not use legacy wait_key')); sys.modules['ti_system']=ti; import STAT1"
            run=subprocess.run([sys.executable,'-B','-c',code],
                               input='10\n1\n95%\n\n5%\n\n0\n0\n',
                               text=True,capture_output=True,cwd=folder,timeout=10)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertIn('ROUND UP: n=385',run.stdout)



    def test_lazy_startup_and_repeated_topic_release(self):
        code = """
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE
assert not STCORE.topic_modules()
for repeat in range(5):
 refs=[]
 def capture(title,lines):
  refs.extend(weakref.ref(sys.modules[n]) for n in STCORE.topic_modules())
 STCORE.view=capture
 cases=[['10','1','95%','','5%','0'],['11','1','60','100','95%','0','0'],['9','1','','100','15','36','1','','2','0','0']]
 for answers in cases:
  pending=iter(answers)
  builtins.input=lambda prompt='':next(pending)
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[]
  assert not STCORE.topic_modules()
 assert all(ref() is None for ref in refs)
try:
 STCORE.call('STCOMB','does_not_exist')
except AttributeError:
 pass
assert not STCORE.topic_modules()
print('PASS')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('PASS',run.stdout)


    def test_numeric_arrow_reader_and_page_navigation(self):
        import STCORE
        for style,keys in [('scan',[25,34,24,26,105,45]),('ce',[3,4,2,1,5,9])]:
            with patch.object(STCORE,'KEY_STYLE',style):
                self.assertEqual([STCORE.normalize_key(k) for k in keys],
                                 ['up','down','left','right','enter','esc'])
        with patch.object(STCORE,'HAS_KEYS',True),patch.object(STCORE,'KEY_STYLE','scan'), \
             patch.object(STCORE,'get_key',side_effect=[0,999,34,26,25,24,45],create=True) as reader, \
             patch.object(builtins,'input',side_effect=AssertionError('Arrow navigation must not use input')), \
             contextlib.redirect_stdout(io.StringIO()) as out:
            STCORE.view('ARROW CHECK',[str(k) for k in range(10)])
        self.assertEqual(reader.call_count,7)
        for page in ['1-7/10','2-8/10','3-9/10']:self.assertIn(page,out.getvalue())
        for code in [105,45]:
            with patch.object(STCORE,'HAS_KEYS',True),patch.object(STCORE,'KEY_STYLE','scan'), \
                 patch.object(STCORE,'get_key',return_value=code,create=True):
                self.assertEqual(STCORE.wait_key(),'enter' if code==105 else 'esc')

    def test_ce_wait_key_only_import_and_navigation(self):
        code="import sys,types; ti=types.ModuleType('ti_system'); keys=iter([4,3,1,2,9]); ti.wait_key=lambda:next(keys); sys.modules['ti_system']=ti; import STCORE; assert STCORE.ON_TI and not STCORE.HAS_KEYS; STCORE.HAS_KEYS=True; STCORE.view('CE ARROWS',[str(k) for k in range(10)])"
        run=subprocess.run([sys.executable,'-B','-c',code],input='',text=True,capture_output=True,
                           cwd=Path(__file__).resolve().parent.parent,timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('2-8/10',run.stdout)


    def test_full_binomial_pages_and_format_reuse(self):
        # Exercise all 149 rows without constructing an n+1 results list.
        import STCORE,STBINOM
        out,_=capture(lambda:STCORE.paged_results('B11',149,
                lambda k:('P('+str(k)+')',STBINOM.binomial_exact_ratio(148,(1,4),k))),
                ['N']*21+['0'])
        self.assertEqual(len(out),22)
        seen=[]
        for title,lines in out:
            rows=[line for line in lines if line.startswith('P(')]
            self.assertLessEqual(len(rows),7)
            seen.extend(int(line.split(')')[0][2:]) for line in rows)
        self.assertEqual(seen,list(range(149)))
        self.assertIn('ROWS 148..149/149',str(out[-1]))
        out,prompts=capture(STBINOM.binomial_session,
                           ['8','25%','3','3','N','P','2','6','N','4','2','0','0'])
        self.assertIn('P(0)=6561/65536',str(out))
        self.assertIn('P(7)=3/8192',str(out))
        self.assertIn('P(8)=0.000015',str(out))
        self.assertIn('P(8)=0.00%',str(out))
        self.assertEqual(prompts.count('HOW MANY TRIALS n: '),1)
        # B12 uses the same bounded viewer for its optional bar table.
        out,_=capture(s.shape_session,['148','1','.25','Y','N','0'])
        self.assertIn('ROWS 8..14/149',str(out))

    def test_large_dice_against_independent_convolution(self):
        import STDICE
        # Desktop oracle can use larger lists; production uses scalar sums.
        for n in (17,25,40):
            counts=[1]
            for die in range(n):
                updated=[0]*(len(counts)+6)
                for i,count in enumerate(counts):
                    for face in range(1,7):updated[i+face]+=count
                counts=updated
            for cutoff in (n-1,n,3*n,6*n,6*n+1):
                self.assertEqual(STDICE.dice_event_count(n,'2',cutoff),
                                 counts[cutoff] if cutoff<len(counts) else 0)
                self.assertEqual(STDICE.dice_event_count(n,'3',cutoff),sum(counts[:cutoff+1]))
                self.assertEqual(STDICE.dice_event_count(n,'4',cutoff),sum(counts[cutoff:]))

    def test_allocation_limits_and_home_shortcuts(self):
        import STCORE,STAT1,STCOUNT
        result=[]
        capture(lambda:result.append(STCORE.read_size('ROWS: ',25)),['101','26','25'])
        self.assertEqual(result,[25])
        with self.assertRaisesRegex(ValueError,'MAX 25'):
            STCOUNT.hyper_distribution(200,100,100)
        # Bound checking occurs before any row/sector storage is constructed.
        fixtures=[(s.frequency_session,['26','1','2','1','1']),
                  (s.category_session,['61','1','ONLY','1','0']),
                  (lambda:s.experiment_session('coin'),['31','1','0']),
                  (lambda:s.experiment_session('spinner'),['61','1','1','1','0']),
                  (s.two_way_session,['11','1','11','1','ROW','COLUMN','1','0']),
                  (s.distribution_session,['26','1','0','1','0'])]
        for fun,answers in fixtures:capture(fun,answers)
        # Long lines may wrap beyond 100 display lines without a wrapping list.
        with patch.object(STCORE,'wait_key',return_value='b'),contextlib.redirect_stdout(io.StringIO()) as output:
            STCORE.view('LONG',['x'*3300])
        self.assertIn('1-7/110',output.getvalue())

    def test_runtime_has_no_test_only_binomial_or_guide_fixture(self):
        import ast
        for filename,removed in [('STBINOM.py',{'bin_pdf','bin_cdf','read_binomial','binomial_probs','binomial_event'}),
                                 ('STDICE.py',{'dice_sum_counts'})]:
            tree=ast.parse(Path(__file__).resolve().parent.parent.joinpath(filename).read_text())
            self.assertFalse(removed.intersection(n.name for n in tree.body if isinstance(n,ast.FunctionDef)))
        self.assertFalse(Path(__file__).resolve().parent.parent.joinpath('STREF.py').exists())

    def test_probe_runs_with_simulated_key_api(self):
        code="import sys,types; ti=types.ModuleType('ti_system'); keys=iter([25,34,24,26,92,93,94,102,105,45]); ti.get_key=lambda *a:next(keys); sys.modules['ti_system']=ti; import EVOPROBE"
        run=subprocess.run([sys.executable,'-B','-c',code],input='\n\nN\n',text=True,capture_output=True,
                           cwd=Path(__file__).resolve().parent.parent,timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)
        for expected in ['LIST 100: OK','LIST 101: OK','CACHE DELETE: True','FRESH REIMPORT: True',
                         'UP = 25','DOWN = 34','LEFT = 24','RIGHT = 26','ENTER = 105']:
            self.assertIn(expected,run.stdout)


    def test_between_is_visible_on_first_event_page(self):
        import STCORE
        answers=iter(['6','19','26','1'])
        with patch.object(builtins,'input',lambda prompt='':next(answers)),contextlib.redirect_stdout(io.StringIO()) as screen:
            event=STCORE.event_input()
        first=screen.getvalue().split('INCLUDE ENDPOINTS?')[0]
        self.assertIn('6 BETWEEN x AND y',first)
        self.assertEqual(event,('[]',(19,1),(26,1)))
        self.assertEqual(s.fixed(s.binomial_exact_event(39,s.as_ratio('63%'),event),4),'0.7122')


if __name__=='__main__':
    unittest.main(verbosity=2)
