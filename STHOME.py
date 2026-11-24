import STCORE as c
def choose():
  routes=(('STNDIST', 'normal_menu'), ('STBWORD', 'wording_session'), ('STPROBM', 'probability_tasks'), ('STTASKS', 'data_tasks'), ('STTASKS', 'graph_tasks'), ('STSTUDY', 'study_menu'), ('STUNIF', 'uniform_menu'), ('STTDIST', 't_menu'), ('STCLT', 'clt_menu'), ('STSIZE', '_required_sample_size'), ('STCIMENU', 'menu'), ('STDESC', 'solver_zscore'), ('STCIIO', 'zstar_session'), ('STCIIO', 'tstar_session'), ('STHYP', 'menu'), ('STREGIO', 'menu'))
  key=c.menu('STAT1',(('1','NORMAL DISTRIBUTION'),('2','BINOMIAL'),('3','PROBABILITY'),('4','DATA / STATS'),('5','GRAPHS / DATA SHAPE'),('6','STUDY / CONCEPTS'),('7','UNIFORM DISTRIBUTION'),('8','STUDENT t DISTRIBUTION'),('9','CLT / SAMPLING DISTRIBUTIONS'),('10','SAMPLE SIZE CALCULATOR'),('11','CONFIDENCE INTERVAL / MOE'),('12','Z-SCORE CALCULATOR'),('13','Z* CRITICAL VALUE'),('14','T* CRITICAL VALUE'),('15','HYPOTHESIS TESTING'),('16','LINEAR REGRESSION / CORRELATION')),page_size=6)
  if key=='0': return
  module,func=routes[int(key)-1]
  args=()
  if key in ('3','4','5'):
    args=({'experiment_tasks':c.task('STHOME','experiment_tasks'),'money_tasks':c.task('STHOME','money_tasks'),'reference_call':c.task('STHOME','reference_call')},)
  return module,func,args

def quick_main():
  while True:
    route=choose()
    if route is None:return
    c.call(route[0],route[1],*route[2])

def experiment_tasks(word=None): return c.call('STTASKS','experiment_tasks',None,word)
def money_tasks(): return c.call('STPROBM','money_tasks',{'reference_call':reference_call})
def reference_call(name):
  key=c.menu('COUNT / CHOOSE / ARRANGE',[('1','CHOOSE nCr'),('2','ARRANGE nPr'),('3','TOTAL OUTCOMES')])
  if key!='0': c.call('STCOUNT',{'1':'solver_ncr','2':'solver_npr','3':'solver_sample_space'}[key])
