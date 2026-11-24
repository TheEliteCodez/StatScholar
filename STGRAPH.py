import STCORE
from STDMATH import *
def boxplot_values(values):
  q1,med,q3 = quartiles(values)
  if q1 is None: raise ValueError('BOXPLOT NEEDS TWO VALUES')
  iqr=sub(q3,q1)
  low=sub(q1,STCORE.rmul(iqr,(3,2)))
  high=STCORE.radd(q3,STCORE.rmul(iqr,(3,2)))
  inside=[x for x in values if STCORE.compare_exact(x,low)>=0 and STCORE.compare_exact(x,high)<=0]
  outside=[x for x in values if STCORE.compare_exact(x,low)<0 or STCORE.compare_exact(x,high)>0]
  return q1,med,q3,iqr,low,high,inside[0],inside[-1],outside
def boxplot_data(values,title='BOXPLOT VALUES / DRAWING',direct=False):
  q1,med,q3,iqr,low,high,wl,wh,out=boxplot_values(values)
  graph=('STGBOX','show',(((tuple(STCORE.number(x) for x in (values[0],q1,med,q3,values[-1],wl,wh)),tuple(STCORE.number(x) for x in out)),),))
  if direct and STCORE.ON_TI: STCORE.show_graph(graph)
  STCORE.results(title, [('MIN',values[0]),('Q1',q1),('MEDIAN',med),('Q3',q3),('MAX',values[-1]),('IQR',iqr),('LOWER FENCE',low),('UPPER FENCE',high),('LOW WHISKER',wl),('HIGH WHISKER',wh),('OUTLIERS',','.join(STCORE.exact_text(x) for x in out) or 'NONE')], ['BOX Q1 TO Q3; LINE AT MEDIAN', 'WHISKERS TO NON-OUTLIER ENDS', 'PLOT OUTLIERS SEPARATELY'],drawing=['HOW TO DRAW: BOXPLOT','DRAW A SCALED NUMBER LINE.','BOX FROM Q1 TO Q3; MEDIAN LINE.','WHISKERS TO LOW/HIGH WHISKER.','SEPARATE DOTS AT OUTLIERS.'],graph=graph)
def boxplot_session():
  key=STCORE.menu('BOXPLOT VALUES / DRAWING',[('1','FROM RAW DATA'),('2','FROM 5-NUMBER SUMMARY'),('3','SIDE-BY-SIDE BOXPLOTS')])
  if key=='1': boxplot_data(read_raw(),direct=True)
  elif key=='3': STCORE.call('STDATA','compare_session',None,True)
  elif key=='2':
    five=[STCORE.read_exact(k+': ') for k in ('MIN','Q1','MEDIAN','Q3','MAX')]
    iqr=sub(five[3],five[1]); low=sub(five[1],STCORE.rmul(iqr,(3,2))); high=STCORE.radd(five[3],STCORE.rmul(iqr,(3,2)))
    out=STCORE.compare_exact(five[0],low)<0 or STCORE.compare_exact(five[-1],high)>0
    graph=('STGBOX','show',(((tuple(STCORE.number(x) for x in five+[five[0],five[-1]]),()),),))
    if STCORE.ON_TI: STCORE.show_graph(graph)
    STCORE.results('GRAPH > BOX > SUMMARY', list(zip(('MIN','Q1','MEDIAN','Q3','MAX'),five))+[('IQR',iqr),('LOWER FENCE',low),('UPPER FENCE',high)], ['BOX Q1 TO Q3; MEDIAN LINE', 'MODIFIED WHISKERS/OUTLIER LIST REQUIRE RAW DATA' if out else 'WHISKERS TO MIN AND MAX', 'ORDINARY BOXPLOT: MIN TO MAX'],drawing=['HOW TO DRAW: BOXPLOT','SCALED AXIS; BOX Q1 TO Q3.','MARK MEDIAN WITHIN THE BOX.','ORDINARY WHISKERS: MIN/MAX.','MODIFIED WHISKERS NEED RAW DATA.'],graph=graph)
def dotplot_rows(values):
  rows=value_counts(values)
  if all(x[1]==1 for x,f in rows) and rows[-1][0][0]-rows[0][0][0]<RAW_LIMIT:
    counts=dict(rows)
    return [((x,1),counts.get((x,1),0)) for x in range(rows[0][0][0],rows[-1][0][0]+1)]
  return rows
def dotplot_session(values=None):
  values=read_raw('GRAPH > DOTPLOT') if values is None else values
  rows=dotplot_rows(values)
  graph=('STGDATA','show',(rows,'dot','DOTPLOT'))
  if STCORE.ON_TI: STCORE.show_graph(graph)
  STCORE.paged_results('GRAPH > DOTPLOT COUNTS',len(rows),lambda i:(STCORE.exact_text(rows[i][0]),rows[i][1]),['VALUE=COUNT; INCLUDE ZERO GAPS', 'ONE DOT PER OBSERVATION', 'STACK REPEATS AT SAME VALUE', 'KEEP NUMERIC SPACING ON AXIS'],drawing=['HOW TO DRAW: DOTPLOT','SCALED x AXIS; LEAVE ZERO GAPS.','STACK ONE DOT PER OBSERVATION.','USE THE COUNTS IN THIS TABLE.'],graph=graph)
def graph_data(values):
  key=STCORE.menu('DATA > DRAWING VALUES',[('1','BOXPLOT'),('2','DOTPLOT'),('3','HISTOGRAM'),('4','NORMAL PROBABILITY PLOT VALUES')])
  if key=='1': boxplot_data(values,direct=True)
  elif key=='2': dotplot_session(values)
  elif key=='3': STCORE.call('STHIST','histogram_session',values)
  elif key=='4': STCORE.call('STDIST','normal_probability_plot',values)
def raw_outliers(): boxplot_data(read_raw('GRAPH > OUTLIERS'))
def shape_guide():
  while True:
    key=STCORE.menu('INTERPRET GRAPH SHAPE',[('1','NORMAL / SKEW GUIDANCE'),('2','HISTOGRAM DRAWING VALUES'),('3','BOXPLOT DRAWING VALUES')])
    if key=='0': return
    if key=='1': STCORE.view('SHAPE / NORMALITY',['RIGHT SKEW: LONG RIGHT TAIL','LEFT SKEW: LONG LEFT TAIL','NORMAL-LIKE: SYMMETRIC BELL','CHECK GAPS AND OUTLIERS','MEAN / SD ALONE DO NOT SHOW NORMALITY','USE TI STAT PLOT FOR A DRAWN GRAPH'])
    elif key=='2': STCORE.call('STHIST','histogram_session')
    else: boxplot_session()
