import STCORE as c
PAGES = (
 (('EXACTLY / P(X=n)','='),('AT MOST / X<=n','<='),('AT LEAST / X>=n','>='),
  ('LESS THAN / X<n','<'),('MORE THAN / X>n','>'),('BETWEEN TWO VALUES','[]'),
  ('AT LEAST ONE','one')),
 (('MEAN / VAR / SD / USUAL','stats'),('USUAL COUNTS / TAILS','usual'),
  ('DISTRIBUTION SHAPE','shape'),('DEFINE X, n, p','model'),
  ('PROBABILITY TABLE / HEIGHTS','full'),('CDF / WORK / CUTOFF / COUNTS','tables')),
 (('IS THIS BINOMIAL?','conditions'),('FINITE SAMPLE / 5% CHECK','finite'),
  ('WITHOUT REPLACE / HYPERGEOM','sample'),('FORMULA / CHEAT SHEET','cheat')))

def pages():
    return PAGES
def read_event(op):
    if op=='none': return ('=',0,0)
    if op=='one': return '>=',(1,1),0
    a=c.read_exact('LOWER: ' if op=='[]' else 'CUTOFF r: ')
    b=0
    if op=='[]':
        b=c.read_exact('UPPER: ')
        key=c.menu('BINOMIAL > ENDPOINTS',[('1','BOTH INCLUDED [a,b]'),('2','NEITHER (a,b)'),('3','LOWER ONLY [a,b)'),('4','UPPER ONLY (a,b]')])
        if key=='0': return None
        op={'1':'[]','2':'()','3':'[)','4':'(]'}[key]
    return op,a,b
