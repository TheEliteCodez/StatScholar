import STCORE as c

def chi(ts,df,alpha,p,cv):
    key=c.menu('CHI-SQUARE GRAPH',[('1','REJECTION REGION'),('2','p-VALUE REGION')])
    if key=='0':return 'back'
    return c.call('STGCURV','show','CHI',0,df,'2',(cv if key=='1' else ts,),'chi-square CV' if key=='1' else 'chi-square TS',alpha if key=='1' else p,'alpha' if key=='1' else 'p-VALUE')

def correlation(ts,df,alpha,p,critical):
    key=c.menu('CORRELATION TEST GRAPH',[('1','REJECTION REGION'),('2','p-VALUE REGION')])
    if key=='0':return 'back'
    if ts is None:
        return c.view('PERFECT CORRELATION',['|t| IS INFINITE; p=0.','NO FINITE TEST-STATISTIC MARK.'])
    cutoff=critical if key=='1' else abs(ts)
    return c.call('STGCURV','show','t',0,df,'outside',(-cutoff,cutoff),'t CV' if key=='1' else 't TS',alpha if key=='1' else p,'alpha' if key=='1' else 'p-VALUE')
