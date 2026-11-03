import STCORE as c
from STCLTM import normal_cdf, normal_sf, normal_interval, mean_standard_error, proportion_standard_error

def clt_menu():
    actions = {
        '1':lambda:c.call('STCLT1','_sample_mean',False),
        '2':lambda:c.call('STCLT1','_sample_mean',True),
        '3':lambda:c.call('STCLT2','_sample_proportion',False),
        '4':lambda:c.call('STCLT2','_sample_proportion',True)}
    while True:
        key = c.menu('CLT / SAMPLING DISTRIBUTIONS',[
            ('1','MEAN x-bar: DISTRIBUTION'),
            ('2','MEAN x-bar: PROBABILITY'),
            ('3','PROPORTION p-hat: DISTRIBUTION'),
            ('4','PROPORTION p-hat: PROBABILITY')])
        if key == '0':
            return
        actions[key]()
