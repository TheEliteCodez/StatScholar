import STCORE as c
def raw_session(values=None):
  values = c.call('STDMATH','read_raw') if values is None else values
  stats = c.call('STDMATH','descriptive',values)
  population=False
  c.call('STDATA','summary_results',stats,'DATA > RAW > SUMMARY',False,values)
  while True:
    key = c.menu('DATA > RAW > NEXT', [('1','FULL SUMMARY'),('2','Z-SCORE A VALUE'),('3','USUAL / UNUSUAL'),('4','OUTLIERS / FENCES'),('5','GRAPH THIS DATA'),('6','COMPARE ANOTHER LIST'),('7','CHANGE DATA'),('8','SAMPLE / POPULATION'),('9','EDIT ONE VALUE'),('10','CHECK ALL VALUES'),('11','LOAD L1'),('12','CONFIDENCE INTERVAL: MEAN')])
    if key=='0': return
    if key=='1': c.call('STDATA','summary_results',stats,'DATA > RAW > SUMMARY',population,values)
    elif key=='12': c.call('STCIMEAN','_one_mean',stats)
    elif key in ('2','3'): c.call('STDATA','data_normal',stats,'1' if key=='2' else '5',population)
    elif key=='4': c.call('STGRAPH','boxplot_data',values)
    elif key=='5': c.call('STGRAPH','graph_data',values)
    elif key=='6': c.call('STDATA','compare_session',values)
    elif key in ('7','11'):
      values = c.call('STDMATH1','read_os_list','1') if key=='11' else c.call('STDMATH','read_raw')
      stats = c.call('STDMATH','descriptive',values)
      c.call('STDATA','summary_results',stats,'DATA > RAW > SUMMARY',population,values)
    elif key=='8': population=c.call('STDATA','choose_population',population)
    elif key=='9':
      values=c.call('STDMATH','edit_raw',values);stats=c.call('STDMATH','descriptive',values)
      c.call('STDATA','summary_results',stats,'DATA > RAW > SUMMARY',population,values)
    elif key=='10':
      rule=c.call('STNORM','boundary_rule')
      if rule is not None:
        if stats['n']>1 or population:
          c.call('STZLIST','z_list',stats['MEAN'],c.as_ratio(str(stats['POPULATION SD' if population else 'SAMPLE SD Sx'])),stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2'],rule,values)
        else: c.view('DATA',['NEED TWO VALUES FOR SAMPLE SD'])
def comparison(a,b):
  return c.call('STDMATH','descriptive',a), c.call('STDMATH','descriptive',b)
