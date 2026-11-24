import STCORE as c

def choose():
  key=c.menu('HYPOTHESIS TESTING',[
    ('1','ONE PROPORTION z TEST'),('2','TWO PROPORTIONS z TEST'),
    ('3','ONE MEAN t TEST'),('4','TWO INDEPENDENT MEANS t TEST'),
    ('5','CHI-SQUARE GOODNESS OF FIT'),('6','CHI-SQUARE INDEPENDENCE'),
    ('7','CORRELATION / REGRESSION'),('8','PAIRED DATA: TEST + INTERVAL'),('9','TYPE I / TYPE II ERRORS')])
  if key=='0':return
  if key=='9':return 'call','STHERR','menu',()
  if key=='7':return 'call','STREGIO','session',()
  if key=='8':return 'call','STPAIRED','session',()
  number=int(key)
  module='STHYPR' if number<=2 else 'STHYME' if number<=4 else 'STCHI'
  return 'test' if number<=4 else 'chi',module,'session',(number%2==0,False)
