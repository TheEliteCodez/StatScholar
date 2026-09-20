# Author: Gregory King
# Multiple-dice arithmetic and menus, loaded on demand.
import STCORE
from STCOMB import ncr

def solver_dice_space():
    n = STCORE.read_int('# DICE: ')
    STCORE.results('C02 DICE OUTCOMES', [('TOTAL', (6 ** n, 1))], ['6^' + str(n)])

def dice_sum_at_most(n, value):
    # Inclusion-exclusion for bounded dice faces; no frequency array.
    if value < n: return 0
    if value >= 6*n: return 6**n
    count = 0
    for j in range(min(n, (value-n)//6)+1):
        term = ncr(n,j) * ncr(value-6*j,n)
        count += -term if j % 2 else term
    return count


def dice_event_count(n, event, value=0):
    total = 6 ** n
    if event == '1':
        return total
    if event == '2':
        return dice_sum_at_most(n,value)-dice_sum_at_most(n,value-1)
    if event == '3':
        return dice_sum_at_most(n,value)
    if event == '4':
        return total-dice_sum_at_most(n,value-1)
    if event == '5':
        return total - 5 ** n
    if event == '6':
        if value < 0 or value > n:
            return 0
        return ncr(n, value) * 5 ** (n - value)
    if event == '7':
        return 5 ** n
    if event in ('8', '9'):
        return 3 ** n
    if event == 'A':
        return total - 3 ** n
    if event == 'B':
        return 6
    if event == 'C':
        return 1

def solver_multi_dice(n=None):
    STCORE.heading('C07 MULTIPLE DICE')
    if n is None: n = STCORE.read_int('HOW MANY FAIR 6-SIDED DICE: ')
    if n < 1:
        raise ValueError('USE AT LEAST ONE DIE')
    while True:
        event = STCORE.menu('C07 EVENT', [('1', 'TOTAL OUTCOMES'), ('2', 'SUM ='), ('3', 'SUM <='), ('4', 'SUM >='), ('5', 'AT LEAST ONE FACE'), ('6', 'EXACTLY r OF A FACE'), ('7', 'NO DICE OF A FACE'), ('8', 'ALL EVEN'), ('9', 'ALL ODD'), ('A', 'AT LEAST ONE EVEN'), ('B', 'ALL SAME'), ('C', 'ALL = ONE FACE')])
        if event == '0':
            return
        value = 0
        steps = ['FAIR INDEPENDENT DICE', 'n=' + str(n), 'TOTAL=6^n=' + str(6 ** n)]
        if event in ('2', '3', '4'):
            value = STCORE.read_int('SUM: ')
            steps += ['COUNT ORDERED SUM RESULTS', 'SUM ' + {'2': '=', '3': '<=', '4': '>='}[event] + str(value)]
        if event in ('5', '6', '7', 'C'):
            face = STCORE.read_int('TARGET FACE (1-6): ')
            if face < 1 or face > 6:
                raise ValueError('FACE MUST BE 1-6')
            steps.append('FACE=' + str(face))
        if event == '6':
            value = STCORE.read_int('EXACTLY HOW MANY r: ')
        formulas = {'5': 'P=1-(5/6)^n', '6': 'P=nCr*5^(n-r)/6^n', '7': 'P=(5/6)^n', '8': 'P=(1/2)^n', '9': 'P=(1/2)^n', 'A': 'P=1-(1/2)^n', 'B': 'P=6/6^n', 'C': 'P=1/6^n'}
        if event in formulas:
            steps.append(formulas[event])
        if event=='5': steps += ['ONE DIE: P(NOT FACE)=5/6', 'NO TARGET IN n DICE: (5/6)^n', 'AT LEAST ONE=1-P(NONE)']
        good = dice_event_count(n, event, value)
        answers = [('TOTAL OUTCOMES', str(6 ** n))] if event == '1' else [('P', STCORE.ratio(good, 6 ** n)), ('SUCCESSFUL', str(good))]
        STCORE.results('C07', answers, steps)
