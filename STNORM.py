# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STNORM - loaded only when needed.
import STCORE
from STCORE import radd, rmul, rdiv

def sub(a,b):
    return radd(a,(-b[0],b[1]))


def z_value(x,mean,sd): return STCORE.rdiv(sub(x,mean),sd)

def x_value(z,mean,sd): return STCORE.radd(mean,STCORE.rmul(z,sd))


def axis_lines(mean,sd,start,observations=()):
    # Three ticks per panel fit the 30-column shell; adjacent panels overlap.
    def labels(values):
        line=''
        for value in values:
            gap=10-len(value)
            line+=' '*(gap//2)+value+' '*(gap-gap//2)
        return line.rstrip()
    ticks=range(start,start+3)
    values=[STCORE.fixed(x_value((z,1),mean,sd),4).rstrip('0').rstrip('.') for z in ticks]
    keys=[]
    for i,value in enumerate(values):
        if len(value)>9:
            name=chr(65+i)
            keys.append(name+'='+value)
            values[i]=name
    marks=[' ']*30
    for x in observations:
        z=z_value(x,mean,sd)
        offset=STCORE.rdiv(sub(z,(start,1)),(2,1))
        if STCORE.compare_exact(offset,0)>=0 and STCORE.compare_exact(offset,1)<=0:
            marks[4+int(round(20*offset[0]/offset[1]))]='*'
    axis='    |---------|---------|'
    lines=['z: '+str(start)+' TO '+str(start+2),labels([str(z) for z in ticks]),axis,axis,labels(values),'x: SAME TICKS AS z']
    if observations: lines.insert(0,''.join(marks).rstrip() or 'NO OBSERVATION IN THIS PANEL')
    return lines+keys


def show_axes(title,mean,sd,observations=()):
    lines=[]
    for start in (-3,-1,1):
        panel=axis_lines(mean,sd,start,observations)
        lines+=panel+['']*((-len(panel))%STCORE.VIEW_LINES)
    STCORE.view(title,lines)


def empirical_percent(k, region='within'):
    within=((68,1),(95,1),(997,10))[k-1]
    outside=sub((100,1),within)
    return within if region=='within' else outside if region=='outside' else STCORE.rdiv(outside,(2,1))

def empirical_session(mean=None,sd=None):
    while True:
        key=STCORE.menu('GRAPH > EMPIRICAL RULE',[(str(i),label) for i,label in enumerate(('WITHIN 1 SD','WITHIN 2 SD','WITHIN 3 SD','OUTSIDE 1 SD','OUTSIDE 2 SD','OUTSIDE 3 SD','ONE TAIL'),1)])
        if key=='0': return
        k=(int(key)-1)%3+1
        region='within' if int(key)<=3 else 'outside'
        if key=='7':
            k=STCORE.read_size('HOW MANY SD (1..3): ',3)
            side=STCORE.menu('GRAPH > TAIL',[('1','BELOW -k SD'),('2','ABOVE +k SD')])
            if side=='0': continue
            region='tail'
        label=(('BELOW -' if side=='1' else 'ABOVE +')+str(k)+' SD') if region=='tail' else region.upper()+' '+str(k)+' SD'
        answers=[('APPROX PERCENT',empirical_percent(k,region)),('REGION',label)]
        if mean is not None:
            if region=='tail':
                answers.append(('BELOW x' if side=='1' else 'ABOVE x',x_value((-k if side=='1' else k,1),mean,sd)))
            else:
                answers += [('LOW x',x_value((-k,1),mean,sd)),('HIGH x',x_value((k,1),mean,sd))]
        STCORE.results('GRAPH > EMPIRICAL ANSWER',answers,['PERCENT UNITS, NOT PROBABILITY', 'APPROX NORMAL / BELL-SHAPED ONLY', '68 / 95 / 99.7 WITHIN', 'OUTSIDE=100-WITHIN', 'ONE TAIL=OUTSIDE/2'])

def normal_session(mean=None,sd=None,first=None,variance=None):
    inclusive=False
    while True:
        key=first or STCORE.menu('GRAPH > NORMAL / Z',[('1','FIND Z FROM x'),('2','FIND x FROM Z'),('3','LABEL x AND Z AXES'),('4','EMPIRICAL RULE'),('5','USUAL RANGE +/- 2 SD'),('6','CHANGE MEAN / SD'),('7','BOUNDARY RULE < OR <='),('8','SEVERAL x: Z / USUAL / AXES')])
        first=None
        if key=='0': return
        if key=='7':
            rule=boundary_rule()
            if rule is not None: inclusive=rule
            continue
        if key=='4':
            empirical_session(mean,sd)
            continue
        if mean is None or key=='6':
            mean=STCORE.read_exact('MEAN: '); sd=STCORE.read_exact('SD: ')
            variance=None
            if key=='6': continue
        if key=='8':
            STCORE.call('STZLIST','z_list',mean,sd,variance if variance is not None else STCORE.rmul(sd,sd),inclusive)
            continue
        if key=='1':
            x=STCORE.read_exact('x: ')
            STCORE.results('GRAPH > Z-SCORE',[('z',z_value(x,mean,sd))],['z=(x-MEAN)/SD','('+STCORE.exact_text(x)+'-'+STCORE.exact_text(mean)+')/'+STCORE.exact_text(sd)])
        elif key=='2':
            z=STCORE.read_exact('z: ')
            STCORE.results('GRAPH > FIND x',[('x',x_value(z,mean,sd))],['x=MEAN+z*SD',STCORE.exact_text(mean)+'+'+STCORE.exact_text(z)+'*'+STCORE.exact_text(sd)])
        elif key=='3':
            show_axes('ALIGNED x / z AXES',mean,sd)
            STCORE.results('GRAPH > AXES', [('z='+str(z)+' x',x_value((z,1),mean,sd)) for z in range(-3,4)],['DRAW BELL CENTERED AT z=0', 'x=MEAN+z*SD; EVEN TICK SPACING'])
            while True:
                raw=input('OBSERVATION x (ENTER=DONE): ').strip()
                if not raw: break
                x=STCORE.as_ratio(raw)
                z=z_value(x,mean,sd)
                show_axes('AXES (* = OBSERVATION)',mean,sd,(x,))
                import math
                v=STCORE.number(z)
                place='AT z='+STCORE.exact_text(z) if v==int(v) else 'BETWEEN z='+str(math.floor(v))+' AND '+str(math.ceil(v))
                STCORE.results('GRAPH > PLACE OBSERVATION',[('z',z),('PLACE',place)],['LEFT OF MEAN IF z<0', 'RIGHT OF MEAN IF z>0'])
        elif key=='5':
            STCORE.results('GRAPH > USUAL RANGE',[('MIN USUAL',x_value((-2,1),mean,sd)),('MAX USUAL',x_value((2,1),mean,sd)),('UNUSUAL RULE','x<=MIN OR x>=MAX' if inclusive else 'x<MIN OR x>MAX')],['MEAN +/- 2 SD','CHANGE RULE: NORMAL MENU 7'])
            raw=input('CHECK NUMBER (ENTER=SKIP): ').strip()
            if raw:
                x=STCORE.as_ratio(raw)
                position=usual_classification(x,mean,variance if variance is not None else STCORE.rmul(sd,sd),inclusive)
                STCORE.results('GRAPH > UNUSUAL',[('UNUSUAL','NO' if position=='NOT UNUSUAL' else 'YES'),('CLASSIFICATION',position)],['BOUNDARIES ARE UNUSUAL' if inclusive else 'BOUNDARIES ARE USUAL'])

def relative_session():
    vals=[]
    inputs=[]
    for name in ('A','B'):
        STCORE.heading('GRAPH > POSITION '+name)
        x=STCORE.read_exact('x: '); mean=STCORE.read_exact('MEAN: '); sd=STCORE.read_exact('SD: ')
        inputs.append((x,mean,sd))
        vals.append(z_value(x,mean,sd))
    cmp=STCORE.compare_exact(vals[0],vals[1])
    STCORE.results('GRAPH > RELATIVE POSITION',[('z A',vals[0]),('z B',vals[1]),('HIGHER RELATIVE','A' if cmp>0 else 'B' if cmp<0 else 'TIE')],['COMPARE Z-SCORES, NOT RAW x', 'HIGHER z = HIGHER RELATIVE POSITION', 'WHETHER HIGHER IS BETTER DEPENDS ON CONTEXT'])

    while STCORE.menu('RELATIVE > NEXT',[('1','LABEL BOTH x / Z AXES')])=='1':
        for name,(x,mean,sd) in zip(('A','B'),inputs):
            show_axes('AXES '+name+' (* = OBSERVATION)',mean,sd,(x,))
            STCORE.results('AXES '+name, [('z='+str(z)+' x',x_value((z,1),mean,sd)) for z in range(-3,4)]+[('OBSERVATION x',x),('OBSERVATION z',z_value(x,mean,sd))],['DRAW BELL CENTERED AT z=0','MATCH x TICKS TO Z TICKS','MARK OBSERVATION AT ITS Z-SCORE'])

def axes_session(): normal_session(first='3')


def boundary_rule():
    key=STCORE.menu('UNUSUAL BOUNDARIES',[('1','STRICT: x<LOW OR x>HIGH'),('2','INCLUSIVE: x<=LOW OR >=HIGH')])
    return None if key=='0' else key=='2'


def usual_classification(x,mean,variance,inclusive=False):
    delta=sub(x,mean)
    cmp=STCORE.compare_exact(STCORE.rmul(delta,delta),STCORE.rmul((4,1),variance))
    if cmp<0 or (cmp==0 and not inclusive): return 'NOT UNUSUAL'
    if delta[0]==0: return 'BOTH LOW AND HIGH'
    return 'UNUSUALLY LOW' if delta[0]<0 else 'UNUSUALLY HIGH'


def usual_data(values,stats,title,inclusive):
    if stats['SAMPLE VARIANCE s^2']=='DNE':
        STCORE.view(title,['NEED TWO VALUES FOR SAMPLE SD'])
        return
    sd=STCORE.as_ratio(str(stats['SAMPLE SD Sx']))
    answers=[('MIN USUAL',x_value((-2,1),stats['MEAN'],sd)),('MAX USUAL',x_value((2,1),stats['MEAN'],sd))]
    for x in values:
        result=usual_classification(x,stats['MEAN'],stats['SAMPLE VARIANCE s^2'],inclusive)
        if result!='NOT UNUSUAL': answers.append((STCORE.exact_text(x),result))
    if len(answers)==2: answers.append(('UNUSUAL OBSERVATIONS','NONE'))
    STCORE.results(title,answers,['SAMPLE MEAN +/- 2s','BOUNDARIES ARE UNUSUAL' if inclusive else 'BOUNDARIES ARE USUAL','CLASSIFICATION USES UNROUNDED VARIANCE'])
