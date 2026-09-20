# Author: Gregory King
# Finite-population model check, separate from binomial arithmetic.
import STCORE as c


def finite_check():
    total=c.read_int('POPULATION N: ')
    n=c.read_int('SAMPLE n: ')
    replaced=c.yesno('REPLACE EACH SELECTION?')
    if total<1 or n<1 or (not replaced and n>total):
        raise ValueError('CHECK POPULATION AND SAMPLE')
    small=20*n<=total
    c.results('FINITE SAMPLE / BINOMIAL',[
        ('SAMPLE FRACTION',c.ratio(n,total)),
        ('WITHIN COURSE 5% RULE','YES' if small else 'NO'),
        ('INDEPENDENT DRAWS','YES IF RANDOM EACH DRAW' if replaced else 'NO: WITHOUT REPLACEMENT'),
        ('BINOMIAL MODEL','CHECK FIXED n / TWO OUTCOMES / SAME p' if replaced else 'APPROXIMATION MAY BE USED' if small else 'NOT JUSTIFIED BY 5% RULE')],
        ['5% CHECK: n/N <= .05',
         'WITHOUT REPLACEMENT IS DEPENDENT EVEN WHEN THE APPROXIMATION IS ACCEPTABLE.',
         'EXACT FINITE MODEL: HYPERGEOMETRIC, USING N, EXACT TARGET COUNT K, AND n.',
         'A ROUNDED PERCENT MAY NOT GIVE EXACT K. DO NOT ROUND N*p AND CALL IT EXACT.',
         'OTHER BINOMIAL REQUIREMENTS MUST ALSO HOLD.'])
