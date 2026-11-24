def step(index,setup,result,probability,critical,reject):
  null=setup['null'];alt=setup['alternative'];alpha=setup['alpha']
  parameter=setup['parameter'];kind='z' if result['df'] is None else 't'
  if index==1:
    return [result['name'],'SRS / RANDOM INDEPENDENT: '+setup['random']]+result['checks']
  if index==2:
    lines=['CLAIM: '+parameter+' '+setup['claim']+' %.8g' % null,
       'H0: '+parameter+' = %.8g' % null,'H1: '+parameter+' '+alt+' %.8g' % null,
       'TAIL: '+{'<':'LEFT-TAILED TEST','>':'RIGHT-TAILED TEST','!=':'TWO-TAILED TEST'}[alt]]
    if parameter in ('p1-p2','mu1-mu2') and null==0:
      lines.append('H0: '+('p1 = p2' if parameter=='p1-p2' else 'mu1 = mu2'))
    return lines
  if index==3:
    return result['inputs']+['POINT ESTIMATE PE=%.8g' % result['estimate'],
      'PE=p-hat OR p1-hat-p2-hat FOR PROPORTIONS; x-bar OR x1-bar-x2-bar FOR MEANS.',
      'RAW MEANS USE THE SAME n, MEAN AND SAMPLE SD AS 1-Var Stats.']
