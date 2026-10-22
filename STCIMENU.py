import STCORE as c

def menu():
    routes=(('STCIPROP','_one_proportion'),('STCIPROP','_one_proportion_estimate'),('STCIMEAN','_one_mean'),('STCIPROP','_two_proportions'),('STCIMEAN','_two_means'),('STCIMOE','_margin_error'),('STCIMOE','_interval_from_estimate_and_margin'))
    while True:
        key=c.menu('CONFIDENCE INTERVAL / MOE',[(str(i+1),label) for i,label in enumerate(('ONE PROPORTION: x,n','ONE PROPORTION: p-hat,n','ONE MEAN: x-bar,s,n','TWO PROPORTIONS','TWO MEANS','MARGIN OF ERROR','GIVEN CENTER + MARGIN'))])
        if key=='0': return
        c.call(*routes[int(key)-1])
