import STCORE as c

def menu():
    routes=(('STHYPR','session',False),('STHYPR','session',True),
            ('STHYME','session',False),('STHYME','session',True))
    while True:
        key=c.menu('HYPOTHESIS TESTING',[
            ('1','ONE PROPORTION z TEST'),('2','TWO PROPORTIONS z TEST'),
            ('3','ONE MEAN t TEST'),('4','TWO INDEPENDENT MEANS t TEST')])
        if key=='0': return
        c.call(*routes[int(key)-1])
