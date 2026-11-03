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
            ('7','CORRELATION / REGRESSION'),('8','PAIRED DATA: TEST + INTERVAL')])
        if key=='0': return
        if key=='8':
            c.call('STPAIRED','session');continue
        if key=='7':
            c.call('STREGIO','session');continue
        route=routes[int(key)-1]
        if key in ('1','2','3','4'):
            payload=c.call(route[0],route[1],route[2],False)
            if payload is not None: show(*payload)
        else: c.call(*route)

def inference(ts,alpha,alternative,degrees=None):
    return c.call('STHYINF','inference',ts,alpha,alternative,degrees)

def page_module(index):
    if index==6: return 'STHYDRAW'
    if index==7: return 'STHYPVAL'
    return 'STHYRES' if index<6 else 'STHYEND'

def show(setup,result,inference_result=None):
    if inference_result is None:
        inference_result=inference(result['ts'],setup['alpha'],setup['alternative'],result['df'])
    probability,critical,reject=inference_result
    labels=('REQUIREMENTS','H0 AND H1','POINT ESTIMATE','CRITICAL VALUES','TEST STATISTIC',
            'DRAW SAMPLING DISTRIBUTION','p-VALUE','INITIAL CONCLUSION','FINAL CONCLUSION')
    def display(index):
        if index==6 and c.ON_TI:
            action=c.call('STHTPLOT','screens',setup,result,probability,critical)
            if action: return 'back' if action=='back' else None
        return c.view('HT '+str(index)+': '+labels[index-1],c.call(page_module(index),'step',index,setup,result,probability,critical,reject))
    for index in range(1,10):
        if display(index) in ('back','exit'): break
    while True:
        key=c.menu('HYPOTHESIS > REVIEW STEPS',[(str(i+1),label) for i,label in enumerate(labels)]+[('10','ALL NINE STEPS'),('11','FULL-SCREEN p-VALUE GRAPH'),('12','FULL-SCREEN REJECTION GRAPH')])
        if key=='0': return
        if key in ('11','12'):
            if not c.call('STHTPLOT','show',setup,result,probability,critical,'p' if key=='11' else 'alpha'):
                c.view('GRAPHICS UNAVAILABLE',['THIS GRAPH USES ti_plotlib.']+c.call('STHYDRAW','drawing',setup,result,critical))
        elif key=='10':
            for index in range(1,10):
                if display(index) in ('back','exit'): break
        else: display(int(key))
