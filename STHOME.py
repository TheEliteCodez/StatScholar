import STCORE as c
def quick_main():
    routes={'2':('STBWORD','wording_session'),'3':('STPROBM','probability_tasks'),'4':('STTASKS','data_tasks'),'5':('STTASKS','graph_tasks'),'6':('STSTUDY','study_menu'),'9':('STCLT','clt_menu'),'10':('STSIZE','_required_sample_size'),'11':('STCIMENU','menu'),'12':('STDESC','solver_zscore'),'13':('STCIIO','zstar_session'),'14':('STCIIO','tstar_session')}
    context={'experiment_tasks':experiment_tasks,'money_tasks':money_tasks,'reference_call':reference_call,}
    while True:
        key=c.menu('STAT1',[('2','BINOMIAL'),('3','PROBABILITY'),('4','DATA / STATS'),('5','NORMAL / Z / GRAPHS'),('6','STUDY / CONCEPTS'),('9','CLT / SAMPLING DISTRIBUTIONS'),('10','SAMPLE SIZE CALCULATOR'),('11','CONFIDENCE INTERVAL / MOE'),('12','Z-SCORE CALCULATOR'),('13','Z* CRITICAL VALUE'),('14','T* CRITICAL VALUE')],page_size=6)
        if key=='0': return
        try:
            module,func=routes[key]
            if key in ('3','4','5'): c.call(module,func,context)
            else: c.call(module,func)
        except (ValueError,ZeroDivisionError,IndexError) as exc:
            c.view('CHECK ENTERED VALUES',[str(exc)])
def experiment_tasks(word=None): return c.call('STTASKS','experiment_tasks',None,word)
def money_tasks(): return c.call('STPROBM','money_tasks',{'reference_call':reference_call})
def reference_call(name):
    key=c.menu('COUNT / CHOOSE / ARRANGE',[('1','CHOOSE nCr'),('2','ARRANGE nPr'),('3','TOTAL OUTCOMES')])
    if key!='0': c.call('STCOUNT',{'1':'solver_ncr','2':'solver_npr','3':'solver_sample_space'}[key])
