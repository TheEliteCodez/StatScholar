import math
from STGPEN import wait, FONT, BLACK, RED, GREEN, BLUE, line, position, ink, tag

def height(x,degrees):
    if degrees is None: return math.exp(-x*x/2)
    return (1+x*x/degrees)**(-(degrees+1)/2)

def shaded(x,statistic,alternative):
    if alternative=='<': return x<=statistic
    if alternative=='>': return x>=statistic
    return abs(x)>=abs(statistic)

def original(setup,result,score):
    return setup['null']+score*result['se']

def show(setup,result,probability,critical,region='p'):
    try: import ti_plotlib as plt
    except ImportError: return False
    ts=result['ts'];df=result['df'];alt=setup['alternative'];alpha=setup['alpha']
    extent=max(3.5,abs(ts)+.7,max(abs(v) for v in critical)+.7)
    at=lambda score:position(score,extent)
    y=lambda score:100-60*height(score,df)
    plt.cls();plt.window(0,319,0,209)
    plt.pen('medium','solid');plt.color(*(BLUE if region=='p' else RED))
    boundary=ts if region=='p' else (critical[0] if alt=='<' else critical[-1])
    for i in range(241):
        score=-extent+2*extent*i/240
        if shaded(score,boundary,alt): line(plt,at(score),100,at(score),y(score))
    for score in ((boundary,) if alt!='!=' else (-abs(boundary),abs(boundary))):
        line(plt,at(score),100,at(score),y(score))
    plt.pen('thin','solid');plt.color(*BLACK)
    previous=(-extent,y(-extent))
    for i in range(1,241):
        score=-extent+2*extent*i/240
        line(plt,at(previous[0]),previous[1],at(score),y(score));previous=(score,y(score))
    line(plt,8,100,311,100);line(plt,8,132,311,132)
    plt.color(140,140,140);line(plt,at(0),100,at(0),y(0))
    for score in (0,ts)+tuple(critical):
        line(plt,at(score),100,at(score),132)
    for score in (0,)+tuple(critical)+(ts,):
        plt.color(*(GREEN if score==ts else RED if score in critical else BLACK))
        line(plt,at(score),100,at(score),104);line(plt,at(score),132,at(score),136)
    boxes=[]
    for score in critical:
        plt.color(*RED);line(plt,at(score),100,at(score),max(36,y(score)-8))
        tag(plt,'CV=%.4g' % score,at(score),max(36,y(score)-8),RED,boxes)
    plt.color(*GREEN);line(plt,at(ts),100,at(ts),max(36,y(ts)-8))
    tag(plt,'TS=%.4g' % ts,at(ts),max(36,y(ts)-8),GREEN,boxes)
    bounds=(boundary,) if alt!='!=' else (-abs(boundary),abs(boundary))
    for i,score in enumerate(bounds):
        middle=(score-extent)/2 if alt=='<' or (alt=='!=' and i==0) else (score+extent)/2
        text=('p' if region=='p' else 'alpha')+('/2' if alt=='!=' else '')+'=%.4g' % ((probability if region=='p' else alpha)/(2 if alt=='!=' else 1))
        tag(plt,text,at(middle),100-(100-y(middle))/2,BLUE if region=='p' else RED,boxes)
    kind='z' if df is None else 't'
    symbol={'mu':'x-bar','p':'p-hat','mu1-mu2':'x1bar-x2bar','p1-p2':'p1hat-p2hat','mu_d':'d-bar'}[setup['parameter']]
    ink(plt,kind,1,91,BLACK);ink(plt,symbol,1,124,BLACK)
    ink(plt,kind+'=0',at(0)-9,107,BLACK)
    ink(plt,'H0=%.5g' % setup['null'],at(0)-3*len('H0=%.5g' % setup['null']),139,BLACK)
    for score in critical:
        text=kind+'=%.4g' % score;ink(plt,text,at(score)-3*len(text),107,RED)
        text='%.5g' % original(setup,result,score);ink(plt,text,at(score)-3*len(text),139,RED)
    text=kind+'=%.4g' % ts;ink(plt,text,at(ts)-3*len(text),117,GREEN)
    text='%.5g' % result['estimate'];ink(plt,text,at(ts)-3*len(text),149,GREEN)
    plt.color(*BLACK)
    plt.text_at(1,'STANDARD NORMAL (z)' if df is None else 't DISTRIBUTION df=%.5g' % df,'center')
    tail={'<':'LEFT','>':'RIGHT','!=':'TWO-TAILED'}[alt]
    plt.text_at(2,tail+(' REJECTION REGION' if region!='p' else ' p-VALUE REGION'),'center')
    if region=='p':
        plt.text_at(10,'SHADE '+('LEFT OF TS' if alt=='<' else 'RIGHT OF TS' if alt=='>' else 'BEYOND +/-abs(TS)'),'center')
        plt.color(*BLUE);plt.text_at(11,'p-VALUE=%.6g' % probability,'center')
    else:
        comparison=('TS' if alt!='!=' else '|TS|')
        a,b=(abs(ts),critical[-1]) if alt=='!=' else (ts,critical[0])
        comparison+=' > CV' if a>b else ' < CV' if a<b else ' = CV'
        plt.text_at(10,comparison+(': REJECT H0' if probability<=alpha else ': FAIL TO REJECT H0'),'center')
        plt.color(*RED);plt.text_at(11,'SHADE '+('LEFT OF CV' if alt=='<' else 'RIGHT OF CV' if alt=='>' else 'BOTH OUTSIDE CVs')+'; alpha=%.4g' % alpha,'center')
    plt.color(*BLACK);plt.text_at(12,'LEFT/CLEAR:BACK ENTER:NEXT','center')
    return wait(plt)

def screens(setup,result,probability,critical):
    for region in ('alpha','p'):
        action=show(setup,result,probability,critical,region)
        if not action or action=='back': return action
    return 'next'
