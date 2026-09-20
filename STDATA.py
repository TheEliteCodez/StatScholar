# STDATA - loaded only when needed.
import STCORE
from STDMATH import *
SUMMARY_KEYS = ('n', 'SUM', 'MEAN', 'SAMPLE SD Sx', 'SAMPLE VARIANCE s^2', 'MIN', 'Q1', 'MEDIAN', 'Q3', 'MAX', 'MODE', 'RANGE', 'IQR', 'MIDRANGE')


def summary_results(stats, title='DATA > RAW > SUMMARY'):
    STCORE.results(title, [(k,stats[k]) for k in SUMMARY_KEYS], ['MEAN=SUM/n', 's^2=SUM((x-MEAN)^2)/(n-1)', 'Sx=SQRT(s^2)', 'QUARTILES: MEDIANS OF HALVES', 'ODD n: OMIT CENTER FROM HALVES', 'n=1: SD, VAR, Q1/Q3 UNDEFINED'])

def raw_session(values=None):
    values = read_raw() if values is None else values
    stats = descriptive(values)
    summary_results(stats)
    while True:
        key = STCORE.menu('DATA > RAW > NEXT', [('1','FULL SUMMARY'),('2','Z-SCORE A VALUE'),('3','USUAL / UNUSUAL'),('4','OUTLIERS'),('5','GRAPH THIS DATA'),('6','COMPARE ANOTHER LIST'),('7','CHANGE DATA')])
        if key=='0': return
        if key=='1': summary_results(stats)
        elif key in ('2','3'):
            if stats['SAMPLE SD Sx']=='DNE':
                STCORE.view('DATA > RAW', ['NEED AT LEAST TWO VALUES'])
            else:
                STCORE.call('STNORM','normal_session',stats['MEAN'], STCORE.as_ratio(str(stats['SAMPLE SD Sx'])), '1' if key=='2' else '5', stats['SAMPLE VARIANCE s^2'])
        elif key=='4': STCORE.call('STGRAPH','boxplot_data',values)
        elif key=='5': STCORE.call('STGRAPH','graph_data',values)
        elif key=='6': compare_session(values)
        elif key=='7':
            values = read_raw()
            stats = descriptive(values)
            summary_results(stats)

def comparison(a,b):
    return descriptive(a), descriptive(b)

def compare_session(a=None, boxes=False):
    a = read_raw('DATA > COMPARE > A') if a is None else a
    b = read_raw('DATA > COMPARE > B')
    while True:
        sa,sb = comparison(a,b)
        if boxes:
            STCORE.results('GRAPH > SAME SCALE', [('AXIS MIN',min_exact(a[0],b[0])),('AXIS MAX',max_exact(a[-1],b[-1]))], ['USE SAME AXIS AND TICK SPACING'])
            STCORE.call('STGRAPH','boxplot_data',a,'GRAPH > BOX A')
            STCORE.call('STGRAPH','boxplot_data',b,'GRAPH > BOX B')
        else:
            summary_results(sa,'DATA > COMPARE > A')
            summary_results(sb,'DATA > COMPARE > B')
            for title, keys in [('CENTERS',('MEAN','MEDIAN')),('SPREAD',('SAMPLE SD Sx','SAMPLE VARIANCE s^2','IQR','RANGE'))]:
                STCORE.results('DATA > COMPARE > '+title, [(name+' '+label,stats[label]) for label in keys for name,stats in [('A',sa),('B',sb)]], ['COMPARE EACH MEASURE IN CONTEXT'])
        key=STCORE.menu('DATA > COMPARE', [('1','SHOW AGAIN'),('2','CHANGE SET A'),('3','CHANGE SET B'),('4','SIDE-BY-SIDE BOXPLOTS'),('5','COMPARE CENTERS / SPREAD'),('6','USUAL / UNUSUAL BOTH SETS')])
        if key=='0': return
        if key=='6':
            rule=STCORE.call('STNORM','boundary_rule')
            if rule is not None:
                STCORE.call('STNORM','usual_data',a,sa,'USUAL > A',rule)
                STCORE.call('STNORM','usual_data',b,sb,'USUAL > B',rule)
        if key=='4': boxes=True
        if key=='5': boxes=False
        if key=='2': a=read_raw('DATA > COMPARE > A')
        if key=='3': b=read_raw('DATA > COMPARE > B')

def frequency_data_session():
    rows=read_frequency_rows()
    STCORE.call('STDESC','frequency_session',rows)
    while True:
        key=STCORE.menu('DATA > FREQUENCY > NEXT',[('1','SHOW STATISTICS'),('2','HISTOGRAM / GROUP CLASSES'),('3','CHANGE DATA'),('4','RELATIVE / CUM / EVENT')])
        if key=='0': return
        if key=='3': rows=read_frequency_rows()
        if key in ('1','3'): STCORE.call('STDESC','frequency_session',rows)
        if key=='2': STCORE.call('STHIST','histogram_session',None,False,rows)
        if key=='4': STCORE.call('STQUIZ','frequency_tools',rows)
