class Instructions:
  def __init__(self,start,end,observed,expected,nc,table):
    self.start,self.end=start,end
    self.observed,self.expected=observed,expected
    self.nc,self.table=nc,table
  def __len__(self): return len(self.start)+len(self.observed)+len(self.end)
  def __iter__(self):
    for line in self.start: yield line
    for i in range(len(self.observed)):
      if self.table:
        yield '[A](%d,%d)=%g' % (i//self.nc+1,i%self.nc+1,self.observed[i])
      else:
        yield 'ROW %d: L1=%g; L2=%.10g' % (i+1,self.observed[i],self.expected[i])
    for line in self.end: yield line

def steps(observed,expected,nc,df,alpha,ts,p,cv,table=False):
  if table:
    start=['TI-84: INDEPENDENCE STEPS',
      '1. MATRIX > EDIT > [A].',
      'SET SIZE: %d ROWS, %d COLS.' % (len(observed)//nc,nc),
      'ENTER OBSERVED COUNTS BELOW; DO NOT INCLUDE TOTALS.',
      '2. STAT > TESTS > chi2-Test.',
      'Observed: [A]; Expected: [B].',
      '3. SELECT Calculate FOR TS,p,df; Draw FOR THE p-VALUE GRAPH.',
      'THE TEST COMPUTES EXPECTED COUNTS IN [B].',
      'YOUR MATRIX [A] ENTRIES:']
  else:
    start=['TI-84: GOF BUTTON STEPS',
      '1. EVO: OPEN LIST EDITOR.',
      'PLUS/CE: STAT > EDIT.',
      'ENTER OBSERVED COUNTS IN L1 AND EXPECTED COUNTS IN L2.',
      'L1 AND L2 NEED %d ENTRIES EACH; REPLACE OLD DATA.' % nc,
      'L2 NEEDS COUNTS n*pi, NOT PROBABILITIES.',
      '2. STAT > TESTS > chi2GOF-Test.',
      'Observed: L1; Expected: L2.',
      'df=%d (INCLUDING ANY FITTED-PARAMETER ADJUSTMENT).' % df,
      '3. SELECT Calculate FOR TS,p,df; Draw FOR THE p-VALUE GRAPH.',
      'YOUR LIST ENTRIES:']
  end=['chi2 IS THE chi-SQUARE SYMBOL ON THE TI MENU; SELECT THE MENU TOKEN.',
    'CHECK: TS=%.8g; df=%d' % (ts,df),
    'CHECK: p=%.8g' % p,
    'TI-84: p-VALUE BY CDF',
    'EVO: ALPHA+STAT (DISTR) > Chi-Square > chi2cdf.',
    'PLUS/CE: 2nd > VARS (DISTR) > chi2cdf.',
    'LOWER=%.10g; UPPER=1E99; df=%d' % (ts,df),
    'chi2cdf(%.10g,1E99,%d)' % (ts,df),
    'ENTER GIVES p=%.8g' % p,
    '1E99 MEANS 10^99; USE THE EE EXPONENT TOKEN.',
    'TI-84: RIGHT-TAIL CV',
    'EVO: OPEN NUMERIC SOLVER.',
    'PLUS/CE: MATH > Solver.',
    'E1: chi2cdf(X,1E99,%d)' % df,
    'E2: %.10g' % alpha,
    'IF THE EDITOR SHOWS 0=, ENTER chi2cdf(X,1E99,%d)-%.10g' % (df,alpha),
    'PRESS ENTER; SET X GUESS=%d.' % df,
    'SET bound={0,%.10g}.' % max(100,cv*2),
    'HIGHLIGHT X; SELECT SOLVE. PLUS/CE: ALPHA+ENTER.',
    'X=CV=%.8g' % cv,
    'RIGHT-TAIL AREA AT CV IS alpha=%.8g.' % alpha]
  return Instructions(start,end,observed,expected,nc,table)
