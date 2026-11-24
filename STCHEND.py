def conclusion(data):
  table,label,random,alpha,nc,observed,expected,ts,df,p,cv,fitted,rt,ct=data
  reject=p<=alpha
  evidence='SUFFICIENT' if reject else 'NOT SUFFICIENT'
  subject='THE ROW AND COLUMN VARIABLES ARE ASSOCIATED' if table else 'THE POPULATION DISTRIBUTION DIFFERS FROM THE SPECIFIED MODEL'
  rows=['REJECT H0' if reject else 'FAIL TO REJECT H0',
    'BECAUSE p=%.10g %s alpha=%.8g.' % (p,'<=' if reject else '>',alpha),
    evidence+' EVIDENCE OF '+('AN ASSOCIATION.' if table else 'A DIFFERENCE FROM THE MODEL.')]
  if label:rows.append('CONTEXT: '+label)
  rows+=['FINAL CONCLUSION:',
    'AT THE %.8g%% SIGNIFICANCE LEVEL, THERE IS %s EVIDENCE TO CONCLUDE THAT %s.' % (100*alpha,evidence,subject),
    'H0: '+('THE VARIABLES ARE INDEPENDENT.' if table else 'THE POPULATION DISTRIBUTION MATCHES THE SPECIFIED MODEL.'),
    'H1: '+('THE VARIABLES ARE ASSOCIATED.' if table else 'THE POPULATION DISTRIBUTION DIFFERS FROM THE SPECIFIED MODEL.'),
    'FAILURE TO REJECT DOES NOT PROVE '+('INDEPENDENCE.' if table else 'THAT THE MODEL IS TRUE.')]
  return rows
