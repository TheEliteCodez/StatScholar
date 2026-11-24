import STCORE as c

def summary(ts,df,alpha,p,cv):
  return ['TS (chi-square)=%.8g' % ts,
    'CV (right tail)=%.8g' % cv,
    'p-VALUE=%.8g' % p,
    'df=%d; alpha=%.8g' % (df,alpha),
    'REJECT H0' if p<=alpha else 'FAIL TO REJECT H0',
    'p %.6g %s alpha %.6g' % (p,'<=' if p<=alpha else '>',alpha)]

def work(data,plotted):
  table,label,random,alpha,nc,observed,expected,ts,df,p,cv,fitted,rt,ct=data
  hypotheses=(['H0: ROW AND COLUMN VARIABLES ARE INDEPENDENT.',
    'H1: ROW AND COLUMN VARIABLES ARE ASSOCIATED.'] if table else
    ['H0: POPULATION CATEGORY PROBABILITIES MATCH THE SPECIFIED MODEL.',
    'H1: AT LEAST ONE CATEGORY PROBABILITY DIFFERS.'])
  work=(['Eij=ROW TOTAL*COLUMN TOTAL/n',
    'df=(%d-1)*(%d-1)=%d' % (len(rt),nc,df)] if table else
    ['Ei=n*pi; EQUAL MODEL pi=1/k','df=%d-1-%d=%d' % (nc,fitted,df)])
  prefix=[label or 'CHI-SQUARE TEST','RANDOM INDEPENDENT: '+random]+hypotheses+[
    'EXPECTED >=5: '+('PASS' if min(expected)>=5 else 'NOT MET; ASYMPTOTIC RESULT MAY BE UNRELIABLE'),
    'COUNT CHECKS AND SAMPLING CONDITIONS MUST HOLD.']+work+[
    'chi-square=SUM((O-E)^2/E)=%.10g' % ts,'df=%d; alpha=%.8g' % (df,alpha),
    'RIGHT-TAIL CV=%.10g' % cv,'p=P(chi-square_%d >= %.10g)=%.10g' % (df,ts,p),
    'REJECT H0' if p<=alpha else 'FAIL TO REJECT H0',
    ('SUFFICIENT' if p<=alpha else 'INSUFFICIENT')+' EVIDENCE OF '+('AN ASSOCIATION.' if table else 'A DIFFERENCE FROM THE MODEL.'),
    'IF H0 WERE TRUE, A chi-square VALUE THIS LARGE OR LARGER WOULD OCCUR ABOUT %.6g%% OF THE TIME. THIS IS NOT THE CHANCE H0 IS TRUE.' % (100*p),
    'CELL WORK / EXPECTED MATRIX (ROW-MAJOR)']
  drawing=[] if plotted else [
    'HOW TO DRAW: chi-square AXIS >=0; df=%d' % df,
    'RIGHT-SKEWED FOR SMALL df; NO NEGATIVE TAIL.',
    'REJECTION GRAPH: MARK CV=%.8g; SHADE RIGHT; AREA=%.8g' % (cv,alpha),
    'p GRAPH: MARK TS=%.8g; SHADE RIGHT; AREA=%.8g' % (ts,p),
    'NO ASSOCIATION DOES NOT MEAN PROVEN INDEPENDENCE.' if table else 'FAILURE TO REJECT DOES NOT PROVE THE MODEL.']
  return c.call('STCHROW','make',data,prefix,drawing,('STGINFER','chi',(ts,df,alpha,p,cv)))
