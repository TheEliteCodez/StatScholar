"""Compare every PlotLib command with an earlier runtime; desktop only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
CODE=r'''
import hashlib,json,sys,types
import STHTPLOT as graph
class Plot(types.ModuleType):
 def __init__(self):super().__init__('ti_plotlib');self.commands=[]
 def __getattr__(self,name):return lambda *args:self.commands.append((name,args))
rows=[]
for parameter,null,se,df in [('p',.5,.05,None),('mu',65,2.3477742,9),('p1-p2',0,.04,None),('mu1-mu2',4,1.5,17),('mu_d',2,.5,9)]:
 for statistic in (-2,0,2):
  for alternative in ('<','>','!='):
   for region in ('p','alpha'):
    plt=Plot();sys.modules['ti_plotlib']=plt
    setup={'alternative':alternative,'alpha':.05,'parameter':parameter,'null':null}
    result={'ts':statistic,'df':df,'estimate':null+statistic*se,'se':se}
    critical=(-2,2) if alternative=='!=' else (-2,) if alternative=='<' else (2,)
    graph.show(setup,result,.02,critical,region)
    rows.append(dict(parameter=parameter,ts=statistic,alternative=alternative,region=region,commands=len(plt.commands),sha256=hashlib.sha256(json.dumps(plt.commands,separators=(',',':')).encode()).hexdigest()))
print(json.dumps(rows))
'''


if __name__=='__main__':
    baseline=Path(sys.argv[1]).resolve()
    traces=[]
    for tree in (baseline,ROOT):
        result=subprocess.run([sys.executable,'-B','-c',CODE],cwd=tree,capture_output=True,text=True,timeout=30)
        assert result.returncode==0,result.stderr
        traces.append(json.loads(result.stdout))
    assert traces[0]==traces[1],'PlotLib commands changed'
    result={'scope':'Exact command equivalence: five parameter axes, negative/zero/positive TS, three tails, p/rejection. Desktop stubs, not physical rendering.',
            'baseline_runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in baseline.glob('ST*.py')},
            'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('ST*.py')},'cases':traces[1]}
    (ROOT/'artifacts/hypothesis_graph_equivalence.json').write_text(json.dumps(result,indent=2)+'\n')
    print(len(traces[1]),'complete graph command traces identical')
