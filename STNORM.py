import STCORE
def sub(a,b):
    return STCORE.radd(a,(-b[0],b[1]))
def z_value(x,mean,sd): return STCORE.rdiv(sub(x,mean),sd) if sd[0] else 'DNE (SD=0)'
def x_value(z,mean,sd): return STCORE.radd(mean,STCORE.rmul(z,sd))
def axis_lines(mean,sd,start,observations=()):
    return STCORE.call('STNORM1','axis_lines',mean,sd,start,observations)
def show_axes(title,mean,sd,observations=()):
    return STCORE.call('STNORM1','show_axes',title,mean,sd,observations)
def empirical_percent(k, region='within'):
    return STCORE.call('STNORM2','empirical_percent',k,region)
def empirical_session(mean=None,sd=None):
    return STCORE.call('STNORM2','empirical_session',mean,sd)
def normal_session(mean=None,sd=None,first=None,variance=None,single=False):
    return STCORE.call('STNORM3','normal_session',mean,sd,first,variance,single)
def relative_session():
    return STCORE.call('STNORM4','relative_session')
def axes_session(): return STCORE.call('STNORM3','normal_session',None,None,'3')
def boundary_rule():
    key=STCORE.menu('UNUSUAL BOUNDARIES',[('1','STRICT: x<LOW OR x>HIGH'),('2','INCLUSIVE: x<=LOW OR >=HIGH')])
    return None if key=='0' else key=='2'
def usual_classification(x,mean,variance,inclusive=False):
    delta=sub(x,mean)
    cmp=STCORE.compare_exact(STCORE.rmul(delta,delta),STCORE.rmul((4,1),variance))
    if cmp<0 or (cmp==0 and not inclusive): return 'NOT UNUSUAL'
    if delta[0]==0: return 'BOTH LOW AND HIGH'
    return 'UNUSUALLY LOW' if delta[0]<0 else 'UNUSUALLY HIGH'
def usual_data(values,stats,title,inclusive,population=False):
    return STCORE.call('STNORM4','usual_data',values,stats,title,inclusive,population)
def observation_report(x,mean,sd,variance=None,inclusive=False):
    return STCORE.call('STNORM1','observation_report',x,mean,sd,variance,inclusive)

def z_menu():
    while True:
        key=STCORE.menu('Z-SCORE / FIND x',[('1','FIND z FROM x'),('2','FIND x FROM z')])
        if key=='0': return
        normal_session(first=key,single=True)
