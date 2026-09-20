# Author: Gregory King
# STREF - on-demand reference module.
import STCORE

STARTERS = [('Roll 3, 4, 5, 6 or more fair dice...', 'C07'), ('You roll two fair dice...', 'C02'), ('An experiment is rolling a fair die and then flipping a coin...', 'C01'), ('Find the probability that the sum is...', 'P01'), ('Find the probability that A OR B...', 'P04'), ('E and F are mutually exclusive events...', 'P03'), ('Find P(E|F)...', 'P07'), ('Find the probability that at least one...', 'P09'), ("Using your whole group's sample, determine what proportion...", 'F04'), ('Under what distance do the shortest 25%...', 'S06'), ('Half of students travel under what distance...', 'S02'), ('Calculate the maximum usual value...', 'S10'), ('Are any values statistically high? Find z-scores...', 'S12'), ('Does the data appear to come from a Normally distributed population? Why?', 'G02'), ('For the data shown above, find the mean...', 'S01'), ('Find the five-number summary...', 'S05'), ('Find the interquartile range...', 'S08'), ('Find the expected value of X...', 'R02'), ('Is this a valid probability distribution?', 'R01'), ('Choose r objects from n...', 'C03'), ('Arrange or rank r objects from n...', 'C04'), ('What is the probability of exactly x successes...', 'B02'), ('What is the probability of at most x successes...', 'B03'), ('What is the probability of less than x successes...', 'B04'), ('What is the probability of at least x successes...', 'B05'), ('What is the probability of more than x successes...', 'B06'), ('VALUES + FREQUENCY; MEAN', 'F05'), ('FREQUENCY TABLE; MEDIAN', 'F06'), ('FREQUENCY TABLE; MODE', 'F07'), ('DIE THEN COIN; LIST OUTCOMES', 'C05'), ('CAN THESE OCCUR TOGETHER?', 'P10'), ('ARE EVENTS INDEPENDENT?', 'P11'), ('AND / BOTH FROM COUNTS', 'P12'), ('CAN THIS BE A PROBABILITY?', 'P13'), ('ROW/COLUMN TABLE; ONE EVENT', 'P14'), ('TABLE ALREADY GIVES P(X)', 'R04'), ('ONE BLANK IN P(X) COLUMN', 'R05'), ('IS AN EVENT UNUSUAL?', 'R06'), ('BOX; TARGET COUNT; SELECT n', 'R07'), ('PRIZES, COSTS, PROFIT, LOSS', 'R08'), ('LIST X AND P(X) FOR TRIALS', 'B11'), ('MATCH GRAPH TO p; SYMMETRY', 'B12'), ('RANGE RULE; FIRST UNUSUAL', 'B13')]

def question_starters():
    page = 0
    per_page = 6
    while True:
        STCORE.heading('QUESTION STARTERS')
        start = page * per_page
        end = min(start + per_page, len(STARTERS))
        i = start
        n = 1
        while i < end:
            phrase = STARTERS[i][0]
            print(str(n) + ' ' + phrase[:25])
            i += 1
            n += 1
        if end < len(STARTERS):
            print('N NEXT')
        if page > 0:
            print('P PREV')
        print('0 BACK')
        c = input('> ').upper()
        if c == '0':
            return
        elif c == 'N' and end < len(STARTERS):
            page += 1
        elif c == 'P' and page > 0:
            page -= 1
        else:
            try:
                idx = int(c)
                real = start + idx - 1
                if idx >= 1 and idx <= per_page and (real < len(STARTERS)):
                    phrase, qid = STARTERS[real]
                    STCORE.view('QUESTION WORDING', [phrase, '', 'MATRIX TYPE:', qid, GUIDES[qid][0]])
                    show_identified(qid)
            except:
                pass

def wizard_chart_table():
    table_tasks()

def wizard_raw_data():
    STCORE.call('STDATA','raw_session')

def wizard_dice_random():
    experiment_tasks()

def wizard_probability_words():
    probability_tasks()

def wizard_binomial():
    trial_tasks()

def wizard_counting():
    STCORE.heading('COUNTING WIZARD')
    if STCORE.yesno('DOES IT SAY CHOOSE / SELECT / GROUP / PAIR?'):
        if STCORE.yesno('DOES ORDER MATTER?'):
            show_identified('C04')
        else:
            show_identified('C03')
        return
    if STCORE.yesno('DOES IT SAY ARRANGE / RANK / ORDER / POSITIONS?'):
        show_identified('C04')
        return
    if STCORE.yesno('DOES IT ASK TOTAL POSSIBLE OUTCOMES FROM STAGES?'):
        show_identified('C01')
        return
    STCORE.view('NOT IDENTIFIED', ['TRY QUESTION STARTERS.', 'ASK YOURSELF WHETHER', 'ORDER MATTERS.'])

def wizard_formula():
    while True:
        STCORE.heading('FORMULA WIZARD')
        print('WHICH LOOKS CLOSE?')
        print('1 (x-mean)/SD')
        print('2 mean+2(SD)')
        print('3 Q3-Q1')
        print('4 f/n')
        print('5 P(A and B)/P(B)')
        print('6 A+B-BOTH')
        print('7 nCr*p^x*(1-p)^(n-x)')
        print('8 SUM[x*P(x)]')
        print('9 n*p')
        print('A sqrt(n*p*(1-p))')
        print('0 BACK')
        c = input('> ').upper()
        if c == '1':
            show_identified('S12')
        elif c == '2':
            show_identified('S10')
        elif c == '3':
            show_identified('S08')
        elif c == '4':
            show_identified('F02')
        elif c == '5':
            show_identified('P07')
        elif c == '6':
            show_identified('P04')
        elif c == '7':
            show_identified('B07')
        elif c == '8':
            show_identified('R02')
        elif c == '9':
            show_identified('B08')
        elif c == 'A':
            show_identified('B09')
        elif c == '0':
            return

def browse_matrix():
    groups = [('D', 'DATA'), ('F', 'FREQUENCY'), ('S', 'DESCRIPTIVE'), ('G', 'GRAPHS'), ('P', 'PROBABILITY'), ('C', 'COUNTING'), ('R', 'RANDOM VARIABLE'), ('B', 'BINOMIAL')]
    while True:
        key = STCORE.menu('GUIDE GROUP', [(a, b) for a, b in groups])
        if key == '0':
            return
        browse_ids(key, sorted([gid for gid in GUIDES if gid.startswith(key)]))

def browse_ids(title, ids):
    page = 0
    per_page = 7
    while True:
        STCORE.heading(title)
        start = page * per_page
        end = min(start + per_page, len(ids))
        i = start
        n = 1
        while i < end:
            qid = ids[i]
            print(str(n) + ' ' + qid + ' ' + GUIDES[qid][0][:16])
            i += 1
            n += 1
        if end < len(ids):
            print('N NEXT')
        if page > 0:
            print('P PREV')
        print('0 BACK')
        c = input('> ').upper()
        if c == '0':
            return
        elif c == 'N' and end < len(ids):
            page += 1
        elif c == 'P' and page > 0:
            page -= 1
        else:
            try:
                idx = int(c)
                real = start + idx - 1
                if idx >= 1 and idx <= per_page and (real < len(ids)):
                    show_identified(ids[real])
            except:
                pass

def ti84_methods():
    while True:
        STCORE.heading('TI-84 EVO METHODS')
        print('1 1-VAR STATS')
        print('2 BOXPLOT')
        print('3 HISTOGRAM')
        print('4 nCr / nPr')
        print('5 BINOM PDF/CDF')
        print('6 EXPECTED VALUE')
        print('0 BACK')
        c = input('> ')
        if c == '1':
            STCORE.view('1-VAR STATS', ['STAT > EDIT.', 'ENTER DATA IN L1.', '', 'STAT > CALC.', '1-VAR STATS.', 'LIST=L1.', '', 'READ:', 'xbar MEAN', 'Sx SAMPLE SD', 'n SAMPLE SIZE', 'minX,Q1,Med,Q3,maxX.'])
        elif c == '2':
            STCORE.view('BOXPLOT', ['ENTER DATA IN L1.', 'STAT PLOT / PLOT1 ON.', 'CHOOSE BOX PLOT.', 'Xlist=L1.', 'Freq=1.', 'ZOOM > ZoomStat.'])
        elif c == '3':
            STCORE.view('HISTOGRAM', ['ENTER DATA IN L1.', 'STAT PLOT / PLOT1 ON.', 'CHOOSE HISTOGRAM.', 'Xlist=L1.', 'Freq=1.', 'ZOOM > ZoomStat.'])
        elif c == '4':
            STCORE.view('nCr / nPr', ['TYPE n.', 'MATH > PRB.', '', 'nCr IF ORDER', 'DOES NOT MATTER.', '', 'nPr IF ORDER MATTERS.', '', 'TYPE r, ENTER.'])
        elif c == '5':
            STCORE.view('BINOMIAL', ['EXACTLY x:', 'binompdf(n,p,x)', '', 'AT MOST x:', 'binomcdf(n,p,x)', '', 'LESS THAN x:', 'binomcdf(n,p,x-1)', '', 'AT LEAST x:', '1-binomcdf(n,p,x-1)', '', 'MORE THAN x:', '1-binomcdf(n,p,x)'])
        elif c == '6':
            STCORE.view('EXPECTED VALUE', ['L1=x VALUES.', 'L2=P(x).', '', '1-VAR STATS.', 'LIST=L1.', 'FREQ=L2.', '', 'xbar = E(X).'])
        elif c == '0':
            return

def open_reference(name, context, *args):
    for key,value in context.items():
        if key not in globals(): globals()[key]=value
    return globals()[name](*args)
