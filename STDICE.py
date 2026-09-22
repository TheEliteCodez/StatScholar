# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Two-dice events only; other experiments load separately.
import STCORE

def solver_dice_space(): return STCORE.call('STMDICE','solver_dice_space')
def solver_multi_dice(n=None): return STCORE.call('STMDICE','solver_multi_dice',n)
def dice_event_count(n,event,value=0): return STCORE.call('STMDICE','dice_event_count',n,event,value)
def dice_sum_at_most(n,value): return STCORE.call('STMDICE','dice_sum_at_most',n,value)
def experiment_session(kind): return STCORE.call('STEXPER','experiment_session',kind)
def experiment_indices(outcomes,kind,query): return STCORE.call('STEXPER','experiment_indices',outcomes,kind,query)

def pair_matches(pair,event):
    kind,op,value=event[:3]
    upper=event[3] if len(event)>3 else 0
    a,b=pair
    if kind=='sumodd': return (a+b)%2==1
    if kind=='sumeven': return (a+b)%2==0
    if kind=='anyeven': return a%2==0 or b%2==0
    if kind=='sum': return STCORE.event_match(a+b,op,value,upper)
    if kind=='first': return STCORE.event_match(a,op,value,upper)
    if kind=='second': return STCORE.event_match(b,op,value,upper)
    if kind=='doubles': return a==b
    if kind=='even': return a%2==0 and b%2==0
    if kind=='odd': return a%2==1 and b%2==1
    if kind=='face': return a==value or b==value
    raise ValueError('UNKNOWN DICE EVENT')


def pair_probability(first,second=None,join='AND'):
    return STCORE.ratio(sum(1 for pair in pair_outcomes(first,second,join)),36)


def pair_outcomes(first,second=None,join='AND'):
    for a in range(1,7):
        for b in range(1,7):
            x=pair_matches((a,b),first)
            y=pair_matches((a,b),second) if second else x
            if (x and y) if join=='AND' else (x or y): yield a,b



def read_pair_event():
    key=STCORE.menu('DICE > DESCRIBE EVENT',[('1','SUM'),('2','FIRST DIE'),('3','SECOND DIE'),('4','DOUBLES / SAME'),('5','BOTH EVEN'),('6','BOTH ODD'),('7','AT LEAST ONE FACE'),('8','SUM IS ODD'),('9','SUM IS EVEN'),('10','AT LEAST ONE EVEN')])
    if key=='0': return None
    kind={'1':'sum','2':'first','3':'second','4':'doubles','5':'even','6':'odd','7':'face','8':'sumodd','9':'sumeven','10':'anyeven'}[key]
    op='='
    value=0
    if key in ('1','2','3'):
        op=STCORE.choice_pages('DICE > WORDS',((('EXACTLY','='),('AT MOST','<='),('AT LEAST','>='),('LESS THAN','<'),('MORE THAN','>'),('BETWEEN','[]')),))
        if op is None: return None
        if op=='[]':
            event=STCORE.call('STBWE','read_event',op)
            return (kind,)+event if event else None
        value=STCORE.read_int('VALUE: ')
    elif key=='7': value=STCORE.read_size('FACE (1..6): ',6)
    return kind,op,value


def dice_session(word=None):
    n=STCORE.read_int('HOW MANY FAIR 6-SIDED DICE: ')
    pending={'and':'2','or':'3'}.get(word) if n==2 else None
    if word and word not in ('and','or'): STCORE.call('STMDICE','word_event',n,word)
    if n!=2:
        solver_multi_dice(n)
        return
    while True:
        key=pending or STCORE.menu('TWO DICE > QUESTION',[('1','ONE EVENT / SUM / FIRST'),('2','A AND B / BOTH'),('3','A OR B'),('4','SAMPLE SPACE'),('5','FACE COUNTS / MORE EVENTS'),('6','CHANGE DICE COUNT')])
        pending=None
        if key=='0': return
        if key=='6':
            n=STCORE.read_int('NUMBER OF DICE: ')
            if n!=2: solver_multi_dice(n)
            n=2
            continue
        if key=='4':
            STCORE.call('STPAGE','text_pages','TWO DICE > 36 OUTCOMES','FIRST,SECOND: '+', '.join('('+str(a)+','+str(b)+')' for a in range(1,7) for b in range(1,7)))
            continue
        if key=='5':
            solver_multi_dice(n);continue
        first=read_pair_event()
        if first is None: continue
        second=read_pair_event() if key in ('2','3') else None
        if key in ('2','3') and second is None: continue
        join='OR' if key=='3' else 'AND'
        p=pair_probability(first,second,join)
        STCORE.results('DICE > '+join if second else 'DICE > EVENT',[('P',p),('FRACTION',STCORE.answer_text(p,'F')),('SUCCESSFUL',STCORE.number(STCORE.rmul(p,(36,1)))),('TOTAL',36)],['ORDERED PAIRS: FIRST,SECOND','AND: BOTH CONDITIONS HOLD','OR: EITHER; COUNT OVERLAP ONCE','FIRST/SECOND DISTINGUISHED'])
        show=STCORE.menu('DICE > NEXT',[('1','ANOTHER EVENT'),('2','LIST MATCHING OUTCOMES')])
        if show=='0': return
        if show=='2':
            lines=['('+str(a)+','+str(b)+')' for a,b in pair_outcomes(first,second,join)]
            STCORE.call('STPAGE','text_pages','SUCCESSFUL ORDERED PAIRS',', '.join(lines) or 'NONE')
