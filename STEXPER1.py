# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.
# Experiment session UI; event helper loads back through the dispatcher.
import STCORE


def experiment_inputs(kind):
    STCORE.heading('P01 / C05 EXPERIMENT')
    if kind == 'roulette':
        zeros = STCORE.read_size('ZERO SPACES (0,00 -> 2): ', STCORE.MAX_OUTCOMES-1, 0)
        last = STCORE.read_size('LAST NUMBER (USUALLY 36): ', STCORE.MAX_OUTCOMES-zeros)
        outcomes = [(str(k), k) for k in range(1, last + 1)] + [('0' * (i + 1), 0) for i in range(zeros)]
    elif kind == 'cards':
        outcomes = [(str(k) + s, k) for s in ('S', 'D', 'C', 'H') for k in range(1, 14)]
        print('52 CARDS; ACE=1 J=11 Q=12 K=13')
        print('S SPADES; D DIAMONDS')
        print('C CLUBS; H HEARTS')
        print('ALSO RED OR BLACK')
    elif kind == 'coin':
        sides = STCORE.read_size('DIE SIDES (USUALLY 6): ', STCORE.MAX_OUTCOMES//2)
        outcomes = [(str(k) + c, k) for k in range(1, sides + 1) for c in ('H', 'T')]
        print('FAIR COIN, INDEPENDENT DIE')
    else:
        size = STCORE.read_size('NUMBER OF SPINNER SECTORS: ', STCORE.MAX_OUTCOMES)
        outcomes = []
        weights = []
        for i in range(size):
            x = STCORE.read_int('SECTOR NUMBER: ')
            outcomes.append((str(x), x))
            weights.append(STCORE.read_exact('SECTOR WEIGHT (EQUAL: 1): '))
    if kind != 'spinner':
        weights = [(1, 1)] * len(outcomes)
    return outcomes, weights


def experiment_session(kind, word=None):
    outcomes, weights = experiment_inputs(kind)
    while True:
        key = STCORE.menu('EXPERIMENT > NEXT', [('1','CHOOSE EVENT'),('2','A AND B'),('3','A OR B'),('4','NOT / COMPLEMENT'),('5','SAMPLE SPACE'),('6','TYPE EVENT EXPRESSION'),('7','CHANGE EXPERIMENT DATA'),('8','COUNT IN REPEATED DRAWS')]) if not word else '8' if word == 'one' else '1'
        if key == '0': return
        if key == '7':
            outcomes, weights = experiment_inputs(kind); continue
        if key == '5':
            STCORE.view('SAMPLE SPACE', ['TOTAL='+str(len(outcomes))]+[x[0] for x in outcomes]); continue
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
        STCORE.results('P01 / C05', [('P(EVENT)', STCORE.rdiv(good, total))], ['EVENT=' + query, 'MATCHES=' + str(len(chosen)), 'TOTAL=' + str(len(outcomes)), 'P=EVENT WEIGHT/TOTAL WEIGHT', 'MATCHING OUTCOMES:'] + [outcomes[i][0] for i in chosen])


def guided_event(kind, word=None):
    return STCORE.call('STEXPER3', 'guided_event', kind, word)
