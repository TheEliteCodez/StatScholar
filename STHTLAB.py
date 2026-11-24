from STGINK import line,ink,tag
BLACK=(0,0,0);RED=(210,45,45);GREEN=(0,135,55);BLUE=(0,100,210)

def position(score,extent):
  return 8+303*(score+extent)/(2*extent)

def original(setup,result,score):
  return setup['null']+score*result['se']

def labels(setup,result,probability,critical,region,extent):
  import ti_plotlib as plt
  import math
  ts=result['ts'];df=result['df'];alt=setup['alternative'];alpha=setup['alpha']
  boundary=ts if region=='p' else (critical[0] if alt=='<' else critical[-1])
  at=lambda score:position(score,extent)
  y=lambda score:100-60*(math.exp(-score*score/2) if df is None else (1+score*score/df)**(-(df+1)/2))
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
