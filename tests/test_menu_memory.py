"""Fresh-process checks: the shared test facade disables module cleanup."""
import ast
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent


class MenuMemory(unittest.TestCase):
    def run_fresh(self, code):
        run = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                             capture_output=True, text=True, timeout=60)
        self.assertEqual(run.returncode, 0, run.stdout[-2000:] + run.stderr)

    def test_all_literal_dispatch_targets_exist(self):
        # Includes route dictionaries, positional route tuples and lazy calls.
        self.run_fresh('''
import ast, importlib
from pathlib import Path
checked=set()
for path in Path('.').glob('ST*.py'):
    for node in ast.walk(ast.parse(path.read_text())):
        values = node.args if isinstance(node,ast.Call) else node.elts if isinstance(node,(ast.Tuple,ast.List)) else ()
        if len(values)<2: continue
        if not all(isinstance(v,ast.Constant) and isinstance(v.value,str) for v in values[:2]): continue
        module,function = (v.value for v in values[:2])
        if not module.startswith('ST') or not module.isidentifier() or not module.isupper(): continue
        if not function.isidentifier() or not (function[0].islower() or function[0]=='_'): continue
        assert Path(module+'.py').exists(), (path,module,function)
        assert callable(getattr(importlib.import_module(module),function)), (path,module,function)
        checked.add((module,function))
assert len(checked)>150, len(checked)
''')

    def test_home_calculations_repeat_and_release_real_modules(self):
        self.run_fresh('''
import builtins, gc, sys, weakref
import STAT1, STCORE as c
original_import=builtins.__import__
def importing(name,*args,**kwargs):
    assert name!='STCI', 'A calculator route imported the legacy CI bundle'
    return original_import(name,*args,**kwargs)
builtins.__import__=importing
refs=[]
shown=[]
def view(title,lines):
    assert title!='CHECK ENTERED VALUES', lines
    shown.append(title)
    refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
    return 'exit'
c.view=view
c.cls=lambda:None
original_choice=c.read_choice
def choice():
    if sys._getframe(1).f_globals.get('__name__')=='STPAGE': return '0'
    return original_choice()
c.read_choice=choice
# All eight home categories, the seven CI procedures, and every distribution
# calculation. Real menus, inputs, math, result formatting and cleanup run.
cases=[
 ['2','1','20','.25','4','0','0'],
 ['2','2','20','.25','4','0','0'],
 ['2','3','20','.25','4','0','0'],
 ['2','4','20','.25','4','0','0'],
 ['2','5','20','.25','4','0','0'],
 ['2','6','20','.25','3','6','1','0','0'],
 ['2','7','20','.25','0','0'],
 ['2','8','20','.25','','0','0'],
 ['3','1','3','8','0','0'],
 ['3','2','.5','.4','.2','0','0'],
 ['3','3','.2','10','0','0'],
 ['3','7','.5','0','0'],
 ['3','9','2','.2','.3','0','0'],
 ['3','6','3','1','.99','10','1000','0','0','0'],
 ['3','6','4','100','2','50','3','0','0','0'],
 ['3','6','5','1','100','5','0','0','0'],
 ['3','6','5','2','10000','2','0','0','0'],
 ['3','6','5','3','3','2','3','4','0','0','0'],
 ['3','10','100','60','50','30','1','2','3','0','0','0'],
 ['3','11','3','100','40','3','0','0','0'],
 ['3','14','1','100','40','5','2','3','5','0','0','0'],
 ['4','7','250','12%','0','0'],
 ['5','8','100','15','1','1','110','','0','0','0'],
 ['5','8','100','15','1','2','110','','0','0','0'],
 ['5','8','100','15','1','3','90','110','','0','0','0'],
 ['5','8','100','15','2','3','70%','3','0','0','0'],
 ['5','9','0','20','1','2','1','5','2','2','5','2','3','5','10','3','3','70%','0','0','0'],
 ['5','10','1','95%','9','0','2','9','1','1.5','2','9','2','1.5','2','9','3','-1','1','3','9','3','70%','0','0','0'],
 ['6','1','1','0','0'], ['6','2','1','0','0'],
 ['6','3','1','9','0','0','0'], ['6','4','2','0','0'],
 ['6','5','1','2','0','0','0'], ['6','6','3','.01','.05','0','0','0'],
 ['6','7','4','0','0','0'], ['6','8','0','0'],
 ['6','9']+[str(i) for i in range(1,9)]+['0','0','0'],
 ['9','1','','100','15','36','1','','1','0','0'],
 ['9','2','','100','15','36','1','','1','3','95','105','0','0'],
 ['9','3','','.4','100','1','','0','0'],
 ['9','4','','.4','100','1','','2','.5','0','0'],
 ['10','1','95%','','5%','0'], ['10','2','95%','15','2','0'],
 ['11','1','60','100','95%','0','0'],
 ['11','2','','.6','100','95%','0','0'],
 ['11','3','1','100','15','36','95%','','0','0'],
 ['11','4','60','100','50','100','95%','0','0'],
 ['11','5','100','15','36','105','18','40','95%','0','0'],
 ['11','6','1','95%','60','100','0','0'],
 ['11','6','2','95%','15','36','0','0'],
 ['11','6','3','95%','.6','100','0','0'],
 ['11','7','1','.6','.05','0','0'],
 ['11','7','2','100','5','0','0'],
]
# Exercise maximum raw-list size through the deepest graph -> QQ plot path,
# with each plotting convention, and through a mean CI.
raw=['100']+[str(i) for i in range(100)]
for method in ('1','2','3'):
    cases.append(['4','1']+raw+['5','4',method,'0','0','0'])
cases.append(['11','3','2']+raw+['95%','','0','0'])
# Maximum-sized stored tables use ordinary small numbers, independently of
# frequency counts (no expansion into one object per observation).
frequency=['25']+[v for i in range(25) for v in (str(i),'1000000')]
cases.append(['4','2']+frequency+['0','0','0'])
cases.append(['4','3','25']+[v for i in range(25) for v in (str(i),'1/25')]+['0','0','0'])
cases.append(['4','4','10','10']+['R'+str(i) for i in range(10)]+['C'+str(i) for i in range(10)]+['1']*100+['1','1','0','0','0'])
cases.append(['4','5','60']+[v for i in range(60) for v in ('C'+str(i),'1')]+['T','0','0','0'])
for repeat in range(3):
    for index,answers in enumerate(cases):
        pending=iter(answers)
        def read(prompt=''):
            try: return next(pending)
            except StopIteration: raise AssertionError((index,prompt,answers))
        builtins.input=read
        STAT1.main()
        assert list(pending)==[], (index,answers)
        assert not c.topic_modules(), (index,c.topic_modules())
        assert c._call_depth==0
        # No explicit collection here: call() must release cycles itself.
        assert all(ref() is None for ref in refs), index
        refs=[]
assert shown
''')

    def test_permutations_do_not_allocate_factorials_and_raw_summary_streams(self):
        self.run_fresh('''
import STCORE as c, STCOMB, STDMATH1
def no_factorial(n): raise AssertionError('Temporary factorial allocated')
STCOMB.factorial=no_factorial
assert STCOMB.npr(100000,2)==9999900000
assert STCOMB.npr(100000,0)==1
assert STCOMB.npr(2,3)==0
def no_table(values): raise AssertionError('Temporary frequency table allocated')
STDMATH1.value_counts=no_table
stats=STDMATH1.descriptive([(i,1) for i in range(100)])
assert stats['n']==100 and stats['MEAN']==(99,2)
''')


if __name__ == '__main__':
    unittest.main()
