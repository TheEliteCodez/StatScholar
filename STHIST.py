# Author: Gregory King
# STHIST - loaded only when needed.
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
    saved_rows=rows if rows is not None else value_counts(values) if values is not None else None
    while True:
        key='4' if group_first else STCORE.menu('GRAPH > HISTOGRAM',[('1','RAW DATA'),('2','VALUE + FREQUENCY'),('3','X + P(X)'),('4','GROUP INTO CLASSES'),('5','CHANGE DATA')])
        group_first=False
        if key=='0': return
        if key=='5':
            saved_rows=None
            values=None
            continue
        if key=='3':
            import STCOUNT
            rows,approx=STCOUNT.read_distribution()
            STCORE.paged_results('GRAPH > PROB HISTOGRAM',len(rows),lambda i:(STCORE.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=P(x)', 'LABEL x AXIS AND PROBABILITY', 'APPROX: ROUNDED P' if approx else 'USE EQUAL-WIDTH BARS'])
            continue
        if saved_rows is not None: rows=saved_rows
        elif key=='2': rows=read_frequency_rows()
        elif key=='4' and values is None:
            source=STCORE.menu('GRAPH > GROUP SOURCE',[('1','RAW DATA'),('2','VALUE + FREQUENCY')])
            if source=='0': continue
            rows=read_frequency_rows() if source=='2' else value_counts(read_raw())
        else: rows=value_counts(read_raw() if values is None else values)
        saved_rows=rows
        if key!='4':
            total=sum(f for x,f in rows)
            STCORE.paged_results('GRAPH > FREQUENCIES',len(rows),lambda i:(STCORE.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=FREQUENCY','NUMERIC AXIS; BARS TOUCH', 'USE GROUP INTO CLASSES FOR BINS'])
            continue
        mode=STCORE.menu('GRAPH > CLASS METHOD',[('1','NUMBER OF CLASSES'),('2','CLASS WIDTH')])
        if mode=='0': continue
        start=STCORE.read_exact('FIRST LOWER LIMIT: ')
        unit=STCORE.read_exact('MEASURE UNIT (0=CONTINUOUS): ')
        if STCORE.compare_exact(unit,0)<0: raise ValueError('UNIT MUST BE NONNEGATIVE')
        xs=STCORE.exact_sorted(x for x,f in rows)
        if mode=='1':
            count=STCORE.read_size('NUMBER OF CLASSES: ',STCORE.MAX_ROWS)
            span=sub(xs[-1],start)
            if unit[0]:
                units=STCORE.rdiv(STCORE.radd(span,unit),STCORE.rmul((count,1),unit))
                width=STCORE.rmul((-(-units[0]//units[1]),1),unit)
            else:
                width=STCORE.rdiv(span,(count,1))
                if width[0]==0: width=STCORE.read_exact('ALL SAME: ENTER CLASS WIDTH: ')
                # Continuous classes use a closed final endpoint.
        else:
            width=STCORE.read_exact('CLASS WIDTH: ')
            ratio=STCORE.rdiv(sub(xs[-1],start),width)
            count=ratio[0]//ratio[1]+1
            if count>STCORE.MAX_ROWS: raise ValueError('MAX 25 CLASSES; INCREASE WIDTH')
        grouped=grouped_rows(rows,start,width,count,not unit[0])
        lines=[]
        for low,edge,f,rel,cum in grouped:
            upper=sub(edge,unit) if unit[0] else edge
            lines += ['LIMITS '+STCORE.exact_text(low)+' TO '+STCORE.exact_text(upper), 'f='+str(f)+' REL='+STCORE.answer_text(rel)+' CUM='+str(cum)]
            if unit[0]:
                half=STCORE.rdiv(unit,(2,1))
                lines.append('BOUNDARIES '+STCORE.exact_text(sub(low,half))+' TO '+STCORE.exact_text(sub(edge,half)))
        STCORE.view('GRAPH > GROUPED TABLE',lines+['CONTINUOUS: [LOW,HIGH)', 'FINAL CONTINUOUS BIN INCLUDES HIGH', 'DRAW TOUCHING BARS; HEIGHT=f'])

def group_session(): histogram_session(group_first=True)
