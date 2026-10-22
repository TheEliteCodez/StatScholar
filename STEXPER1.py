import STCORE
def experiment_inputs(kind):
    return STCORE.call('STEXPER4', 'experiment_inputs', kind)

def label(x):
    return str(x % 13 + 1) + 'SDCH'[x // 13] if isinstance(x, int) else x[0]
def experiment_session(kind, word=None):
    outcomes, weights = experiment_inputs(kind)
    while True:
        key = STCORE.menu('EXPERIMENT > NEXT', [('1','CHOOSE EVENT'),('2','A AND B'),('3','A OR B'),('4','NOT / COMPLEMENT'),('5','SAMPLE SPACE'),('6','TYPE EVENT EXPRESSION'),('7','CHANGE EXPERIMENT DATA'),('8','COUNT IN REPEATED DRAWS')]) if not word else '8' if word == 'one' else '1'
        if key == '0': return
        if key == '7':
            outcomes, weights = experiment_inputs(kind); continue
        if key == '5':
            STCORE.view('SAMPLE SPACE', ['TOTAL='+str(len(outcomes))]+[label(x) for x in outcomes]); continue
        if key == '6':
            query = input('EVENT (BACK=RETURN): ').strip().upper()
            if query == 'BACK': continue
        else:
            query = STCORE.call('STEXPER1','guided_event',kind, None if key == '8' else word)
            if query is None: word = None; continue
            if key in ('2', '3'):
                second = STCORE.call('STEXPER1','guided_event',kind)
                if second is None: continue
                query += ' AND ' if key == '2' else ' OR '
                query += second
            if key == '4': query = 'NOT ' + query
        if key == '8':
            chosen = STCORE.call('STEXPER2', 'experiment_indices', outcomes, kind, query)
            n = STCORE.read_int('NUMBER OF DRAWS / TRIALS: ')
            replacement = '1' if kind != 'cards' else STCORE.menu('CARD DRAWS', [('1','WITH REPLACEMENT'),('2','WITHOUT REPLACEMENT')])
            if replacement == '1':
                chance = STCORE.rdiv(STCORE.rsum(weights[i] for i in chosen), STCORE.rsum(weights))
                STCORE.call('STBWORD','wording_session',word,n,chance)
            elif replacement == '2': STCORE.call('STSAMPLE','sample_tasks',52,len(chosen),n,word)
            word = None; continue
        word = None
        chosen = STCORE.call('STEXPER2', 'experiment_indices', outcomes, kind, query)
        total = STCORE.rsum(weights)
        good = STCORE.rsum([weights[i] for i in chosen])
        STCORE.results('P01 / C05', [('P(EVENT)', STCORE.rdiv(good, total))], ['EVENT=' + query, 'MATCHES=' + str(len(chosen)), 'TOTAL=' + str(len(outcomes)), 'P=EVENT WEIGHT/TOTAL WEIGHT', 'MATCHING OUTCOMES:'] + [label(outcomes[i]) for i in chosen])
def guided_event(kind, word=None):
    return STCORE.call('STEXPER', 'guided_event', kind, word)
