def step(index,setup,result,probability,critical,reject):
  null=setup['null'];alt=setup['alternative'];alpha=setup['alpha']
  parameter=setup['parameter'];kind='z' if result['df'] is None else 't'
  if index==4:
    area=alpha if alt=='<' else 1-alpha if alt=='>' else 1-alpha/2
    lines=['alpha=%.8g; LEFT-CDF AREA=%.8g' % (alpha,area),
       ('invNorm(area,0,1)' if kind=='z' else 'invT(area,df)'),
       'CV='+', '.join('%.8g' % v for v in critical)]
    if result['df'] is not None: lines.append('df=%.8g' % result['df'])
    lines.append('REJECT TO THE '+('LEFT OF CV' if alt=='<' else 'RIGHT OF CV' if alt=='>' else 'OUTSIDE THE TWO CVs'))
    return lines
  if index==5:
    return result.get('se_work',[])+[result['formula'],'SE UNDER H0=%.8g' % result['se'],
        'TS=(%.8g-%.8g)/%.8g=%.8g' % (result['estimate'],null,result['se'],result['ts']),
        'TI TEST: '+result['command']]
