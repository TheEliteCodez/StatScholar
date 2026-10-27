import STCORE as c

def menu():
    routes=(('STHYPR','session',False),('STHYPR','session',True),
            ('STHYME','session',False),('STHYME','session',True),
            ('STCHI','session',False),('STCHI','session',True))
    while True:
        key=c.menu('HYPOTHESIS TESTING',[
            ('1','ONE PROPORTION z TEST'),('2','TWO PROPORTIONS z TEST'),
            ('3','ONE MEAN t TEST'),('4','TWO INDEPENDENT MEANS t TEST'),
            ('5','CHI-SQUARE GOODNESS OF FIT'),('6','CHI-SQUARE INDEPENDENCE'),
            ('7','CORRELATION / REGRESSION')])
        if key=='0': return
        if key=='7':
            c.call('STREGIO','session');continue
        c.call(*routes[int(key)-1])
