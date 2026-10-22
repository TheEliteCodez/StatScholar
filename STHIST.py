import STCORE
from STDMATH import *
def grouped_rows(rows,start,width,count,closed_last=False):
    if STCORE.compare_exact(width,0)<=0: raise ValueError('WIDTH MUST BE POSITIVE')
    frequencies=[0]*count
    for x,f in rows:
        offset=STCORE.rdiv(sub(x,start),width)
        index=offset[0]//offset[1]
        if closed_last and index==count and offset[0]==count*offset[1]: index=count-1
        if index<0 or index>=count: raise ValueError('CLASSES DO NOT COVER DATA')
        frequencies[index]+=f
    total=sum(frequencies)
    if total<=0: raise ValueError('NO OBSERVATIONS')
    cumulative=0
    result=[]
    for i,f in enumerate(frequencies):
        low=STCORE.radd(start,STCORE.rmul((i,1),width)); high=STCORE.radd(low,width)
        cumulative+=f
        result.append((low,high,f,STCORE.ratio(f,total),cumulative))
    return result
def histogram_session(values=None,group_first=False,rows=None):
    return STCORE.call('STHIST2', 'histogram_session', values, group_first, rows)
def group_session():
    return STCORE.call('STHIST2', 'group_session')
