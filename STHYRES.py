import STCORE as c

def inference(ts,alpha,alternative,degrees=None):
    return c.call('STHYP','inference',ts,alpha,alternative,degrees)

def conclusion(setup,reject):
    return c.call('STHYEND','conclusion',setup,reject)

def drawing(setup,result,critical):
    return c.call('STHYDRAW','drawing',setup,result,critical)

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
    if index==6: return drawing(setup,result,critical)
    return c.call('STHYEND','step',index,setup,result,probability,critical,reject)

def show(setup,result,inference_result=None):
    return c.call('STHYP','show',setup,result,inference_result)
