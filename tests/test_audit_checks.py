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

    def test_range_rule_home_menu_solves_both_inputs(self):
        import STAT1
        out, prompts = capture(STAT1.main, ['S10','50','5','1','','0'])
        self.assertIn('MIN USUAL=40.0000', str(out))
        self.assertIn('MAX USUAL=60.0000', str(out))
        out, prompts = capture(STAT1.main, ['B13','47','.387','4','1','','0','0'])
        self.assertIn('MIN USUAL=11.5107', str(out))
        self.assertIn('MAX USUAL=24.8673', str(out))
        self.assertIn('MIN USUAL COUNT=12', str(out))
        self.assertIn('MAX USUAL COUNT=24', str(out))
        self.assertIn('FIRST UNUSUALLY HIGH=25', str(out))

    def test_range_rule_checks_number_and_exact_boundaries(self):
        import STAT1
        for value, label in [('39.99','UNUSUALLY LOW'), ('40','NOT UNUSUAL'),
                             ('60','NOT UNUSUAL'), ('60.01','UNUSUALLY HIGH')]:
            out, _ = capture(STAT1.main, ['S10','50','5','1',value,'1','0'])
            self.assertIn('CLASSIFICATION='+label, str(out))
        for value, label in [('88','NOT UNUSUAL'), ('87','UNUSUALLY LOW'), ('106','UNUSUALLY HIGH')]:
            out, _ = capture(STAT1.main, ['B13','121','.8','4','1',value,'1','0','0'])
            self.assertIn('CLASSIFICATION='+label, str(out))

    def test_A01_range_includes_exact_lower_endpoint(self):
        # mu=96.8, sigma=4.4, hence exact lower endpoint=88.
        actual=s.usual_counts(121,.8)
        self.assertEqual(actual[4:6],(88,105),"Floating arithmetic excluded the valid count 88")

    def test_A02_at_least_one_with_negative_values(self):
        # P(X>=1)=.25, while P(X!=0)=.5; these are different events.
        rows=[(s.as_ratio(x),s.as_ratio(p)) for x,p in [('-1','.25'),('0','.5'),('1','.25')]]
        output,_=capture(lambda:s.distribution_session(rows),['3','5','1','0'])
        self.assertIn('P=0.2500',str(output))

    def test_A03_direct_guide_id_does_not_silently_disappear(self):
        # R01 has real guide content but no solver name.
        with patch('STNAV.show_identified') as guide:
            output,_=capture(s.main,['R01','0'])
        self.assertTrue(guide.called or output,"Home accepted R01 but displayed no guide or result")

    def test_A04_q038_solver_accepts_distribution_parameters(self):
        output,prompts=capture(lambda:s.question_lookup('Q038'),['1','26','.16','1','0','0'])
        data_prompts=[p for p in prompts if p not in ('> ','Y/N: ')]
        self.assertTrue(data_prompts,"Solve-with-your-numbers must accept parameters")
        self.assertIn("X~Binomial(26,0.16)",str(output))

    def test_A05_roulette_zero_label_is_not_double_zero(self):
        wheel=[(str(k),k) for k in range(1,37)]+[('0',0),('00',0)]
        selected=s.experiment_indices(wheel,'roulette','=0')
        self.assertEqual([wheel[i][0] for i in selected],['0'])

    def test_A06_legacy_direct_solver_has_claimed_format_selection(self):
        with patch.object(s,'results') as formatter:
            output,_=capture(s.main,['P01','1','3','0'])
        self.assertTrue(formatter.called,"P01 bypasses shared formatting and returns straight home")

    def test_A07_exact_table_value_is_less_than_one_third(self):
        # 3333333333333333/10^16 is strictly smaller than 1/3.
        rows=[(s.as_ratio('.3333333333333333'),(1,1))]
        output,_=capture(lambda:s.distribution_session(rows),['1','3','1/3','1','0'])
        self.assertIn('P=1.0000',str(output))


    def test_all_question_solve_and_method_routes(self):
        # Changed-number fixtures exercise real dispatch and solvers. They do
        # not reconstruct missing source questions or replace original oracles.
        fixtures={
          'F05':(['2','1','1','3','1','1'],'MEAN=2.0000'),
          'F06':(['2','1','1','3','1','1'],'MEDIAN=2.0000'),
          'ROULETTE':(['2','36','=00','3','1','BACK'],'1/38'),
          'C05':(['6','3 OR H','1','BACK'],'0.5833'),
          'CATEGORY':(['2','YES','1','NO','3','1','1','0'],'0.2500'),
          'CONCEPT':([], 'EXPECTED'),
          'P13':(['1/4','1'],'YES'),
          'CARDS':(['4S','1','BACK'],'0.0192'),
          'P14':(['2','2','A','B','C','D','1','2','3','4','1','1','1','0'],'0.1000'),
          'P12':(['2','2','A','B','C','D','1','2','3','4','1','1','1','0'],'0.1000'),
          'SPINNER':(['2','1','1','2','3','EVEN','1','BACK'],'0.7500'),
          'P10':(['.6','.63','.43','1'],'0.6825'),
          'P11':(['.57','.69','.46','1'],'INDEPENDENT=NO'),
          'R05':(['3','.1','.2','.2','1'],'0.5000'),
          'R04':(['3','-1','.25','0','.5','1','.25','3','1','0'],'P=0.2500'),
          'R02':(['2','1','.25','3','.75','2','1','0'],'mu=2.5000'),
          'R07':(['8','5','2','3','1','0'],'3/28'),
          'WIN_LOSS':(['1/4','4','270','3','2','6','1','0'],'-1.933594'),
          'R08':(['1','PLAYER','1','3','6','3','2','9','0','30','1','0'],'-0.14'),
          'INSURANCE':(['1','.999363','259','206000','1'],'127.78'),
          'RAFFLE':(['240','2','80','8','1'],'-13.33'),
          'B01':(['Y','Y','Y','Y','1'],'BINOMIAL=YES'),
          'SYMMETRY':(['20','4','16','','1'],'ALWAYS EQUAL=NO'),
          'B13':(['121','.8','4','1','88','1','0'],'USUAL'),
          'B11':(['3','.5','3','3','1','0'],'P(0)=1/8'),
          'BINOMIAL_MODEL':(['8','25%','1','1','1','2','1','0'],'X~Binomial(8,0.25)'),
          'B02':(['4','.5','1','1','2','1','0'],'0.3750'),
          'B09':(['4','.5','2','1','0'],'sigma=1.0000'),
          'B08':(['4','.5','2','1','0'],'mu=2.0000'),
          'B12':(['1','10','3','.35','.25','.2','N','N','N'],'CENTER=3.5'),
          'B03':(['4','.5','1','2','2','1','0'],'0.6875'),
          'B04':(['4','.5','1','3','2','1','0'],'0.3125')}
        for qid,title,route,example in s.QUESTION_DATA:
            with self.subTest(qid=qid,branch='solve'):
                inputs,expected=fixtures[route]
                out,_=capture(lambda:s.question_lookup(qid),['1']+inputs+['0'])
                self.assertIn(expected,str(out))
            with self.subTest(qid=qid,branch='method'):
                out,_=capture(lambda:s.question_lookup(qid),['3','2','0','0'])
                self.assertIn(s.QUESTION_METHODS[qid]+' RECOGNIZE',str(out))

    def test_all_fifteen_reference_only_home_routes(self):
        ids=['D01','D02','D03','D04','S01','S02','S03','S05','S06','S07','S09','G01','G02','P08','R01']
        for gid in ids:
            with self.subTest(gid=gid):
                out,_=capture(s.main,[gid,'1','0','0'])
                self.assertIn(gid+' RECOGNIZE',str(out))

    def test_legacy_numeric_routes_reformat_without_reentry(self):
        fixtures={'P01':(['1','3'],'1/3'),'P02':(['.25'],'3/4'),
          'P03':(['.2','.3'],'1/2'),'P04':(['.6','.63','.43'],'4/5'),
          'P05':(['.5','.25'],'1/8'),'P06':(['.5','.25'],'1/8'),
          'P07':(['1','.2','.4'],'1/2'),'P09':(['.5','3'],'7/8'),
          'F04':(['7','20'],'7/20'),'B07':(['4','.5','2'],'3/8'),
          'S04':(['1','8','2'],'6/1'),'S08':(['2','8','2'],'6/1'),
          'S10':(['5','1'],'3/1'),'S11':(['5','1'],'3/1'),
          'S12':(['8','4','2'],'2/1'),'G03':(['2','4'],'2/1'),
          'C01':(['2','6','2'],'12/1'),'C02':(['5'],'7776/1'),
          'C03':(['5','2'],'10/1'),'C04':(['5','2'],'20/1')}
        for gid,(inputs,expected) in fixtures.items():
            with self.subTest(gid=gid):
                out,_=capture(s.main,[gid]+inputs+['3','2','4','4','2','1']+([''] if gid in ('S10','S11') else [])+['0'])
                self.assertIn(expected,str(out))
                self.assertIn('%',str(out))

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
            cases=[(['Q001','1','4','3','1','6','2','9','6','12','5','d','u','b','1','0','0'],['MEAN=9.2143']),
                   (['Q038','1','8','25%','b','1','1','1','2','b','1','0','0','0'],['X~Binomial(8,0.25)','P=0.3115']),
                   (['B13','121','.8','4','d','d','d','d','b','1','88','b','1','0','0'],['USUAL INTEGERS=88..105','UNUSUAL=NO'])]
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
                               input='Q032\n1\nY\nY\nY\nY\n0\n1\n0\n0\n',
                               text=True,capture_output=True,cwd=folder,timeout=10)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertIn('BINOMIAL=YES',run.stdout)


    def test_guide_content_preserved_after_lazy_split(self):
        import hashlib,json
        guides={gid:s.get_guide(gid) for gid in s.GUIDES if gid not in s.NEW_ROUTES}
        self.assertEqual(len(guides),67)
        for gid,guide in guides.items():
            self.assertEqual(s.GUIDES[gid],(guide['title'],guide['solver']),gid)
            for field in guide:
                self.assertEqual(s.get_guide(gid,field),guide[field],(gid,field))
        self.assertEqual(hashlib.sha256(json.dumps(guides,sort_keys=True).encode()).hexdigest(),
                         '8d5695bbd5954a95fe872fcec0dbcd5c442727daae7bab3ad520c8511d89563d')
        self.assertEqual(len(s.STARTERS),43)

    def test_lazy_startup_and_repeated_topic_release(self):
        # Fresh process: never imports test_support or disables module release.
        code = r"""
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
builtins.input=lambda prompt='':'0'
with contextlib.redirect_stdout(io.StringIO()): STAT1.question_wizard()
original_import=builtins.__import__
def no_guides(name,*args,**kwargs):
 if name.startswith('STG'): raise AssertionError('Guide menu loaded text before section selection')
 return original_import(name,*args,**kwargs)
builtins.__import__=no_guides
with contextlib.redirect_stdout(io.StringIO()):
 for gid in STAT1.GUIDES: STAT1.show_identified(gid)
builtins.__import__=original_import
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
checks=[
 ('STDESC',['F05','2','1','1','3','1','b','1','0']),
 ('STPROB',['P01','1','3','b','1','0']),
 ('STEXPER',['3','4','5','2','36','ODD','b','1','BACK','0']),
 ('STBEXTRA',['Q032','1','Y','Y','Y','Y','b','1','0','0']),
 ('STSAMPLE',['R07','8','5','2','b','1','0','0']),
 ('STGDESC',['S01','2','b','0','0']),
 ('STGPROB',['Q003','3','2','b','0','0','0']),
 ('STGBIN',['Q032','3','2','b','0','0','0']),
 ('STSTUDY',['6','7','5','binomial','1','0','0','0','0','0'])]
for repeat in range(3):
 for expected,answers in checks:
  pending=iter(answers); refs=[];seen=set()
  def read(prompt=''):
   for name in STCORE.TOPIC_MODULES:
    if name in sys.modules:
     seen.add(name);refs.append(weakref.ref(sys.modules[name]))
   return next(pending)
  builtins.input=read
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[],expected
  # Guide modules unload before the returned guide is displayed.
  if not expected.startswith('STG'): assert expected in seen,(expected,seen)
  assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules),(expected,seen)
  assert all(ref() is None for ref in refs),expected
# The actual cleanup also runs when an entered-value operation raises.
def fail(prompt=''): raise ValueError('test interruption')
builtins.input=fail
try:
 with contextlib.redirect_stdout(io.StringIO()): STCORE.call('STDESC','frequency_stats')
except TypeError: pass
else: raise AssertionError('Expected input interruption')
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
print('LAZY_STARTUP_AND_RELEASE=PASS')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],text=True,capture_output=True,
                           cwd=Path(__file__).resolve().parent.parent,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('LAZY_STARTUP_AND_RELEASE=PASS',run.stdout)


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
        # Membership containers must be passed unchanged, with no concatenation.
        with patch.object(STCORE,'menu',return_value='0') as menu:
            STAT1.quick_main()
            args=menu.call_args.args
            self.assertIs(args[2],STAT1.GUIDES)
            self.assertIs(args[3],STAT1.QUESTION_INDEX)
        result=[]
        capture(lambda:result.append(STCORE.read_size('ROWS: ',25)),['101','26','25'])
        self.assertEqual(result,[25])
        with self.assertRaisesRegex(ValueError,'MAX 25'):
            STCOUNT.hyper_distribution(200,100,100)
        # Bound checking occurs before any row/sector storage is constructed.
        fixtures=[(s.frequency_session,['26','1','2','1','1']),
                  (s.category_session,['61','1','ONLY','1','0']),
                  (lambda:s.experiment_session('coin'),['31','1','BACK']),
                  (lambda:s.experiment_session('spinner'),['61','1','1','1','BACK']),
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
        self.assertNotIn('NEW_GUIDES',Path(__file__).resolve().parent.parent.joinpath('STREF.py').read_text())

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
