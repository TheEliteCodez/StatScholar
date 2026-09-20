# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Cards, roulette, spinner and die/coin, loaded separately.
import STCORE

def experiment_session(kind):
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
    while True:
        print('EVENT: 4S, ODD, <3, S OR D')
        print('DIE/COIN: 3 OR H; 6 AND T')
        print('LIST=SPACE; BACK=NEW QUESTION')
        query = input('EVENT: ').strip().upper()
        if query == 'BACK':
            return
        if query == 'LIST':
            STCORE.view('C05 SAMPLE SPACE', ['TOTAL=' + str(len(outcomes))] + [x[0] for x in outcomes])
            continue
        chosen = experiment_indices(outcomes, kind, query)
        total = STCORE.rsum(weights)
        good = STCORE.rsum([weights[i] for i in chosen])
        STCORE.results('P01 / C05', [('P(EVENT)', STCORE.rdiv(good, total))], ['EVENT=' + query, 'MATCHES=' + str(len(chosen)), 'TOTAL=' + str(len(outcomes)), 'P=EVENT WEIGHT/TOTAL WEIGHT', 'MATCHING OUTCOMES:'] + [outcomes[i][0] for i in chosen])

def experiment_indices(outcomes, kind, query):
    query = query.strip().upper()
    for word, short in [('SPADES', 'S'), ('SPADE', 'S'), ('DIAMONDS', 'D'), ('DIAMOND', 'D'), ('CLUBS', 'C'), ('CLUB', 'C'), ('HEARTS', 'H'), ('HEART', 'H'), ('HEADS', 'H'), ('HEAD', 'H'), ('TAILS', 'T'), ('TAIL', 'T'), ('ACE', '1'), ('JACK', '11'), ('QUEEN', '12'), ('KING', '13')]:
        query = query.replace(word, short)
    query = query.replace(' OF ', '')
    if ' OR ' in query:
        parts = query.split(' OR ')
        sets = [experiment_indices(outcomes, kind, q) for q in parts]
        return [i for i in range(len(outcomes)) if any((i in group for group in sets))]
    if ' AND ' in query:
        parts = query.split(' AND ')
        sets = [experiment_indices(outcomes, kind, q) for q in parts]
        return [i for i in range(len(outcomes)) if all((i in group for group in sets))]
    if query.startswith('NOT '):
        group = experiment_indices(outcomes, kind, query[4:])
        return [i for i in range(len(outcomes)) if i not in group]
    if query in ('ODD', 'EVEN'):
        return [i for i, x in enumerate(outcomes) if x[1] % 2 == (1 if query == 'ODD' else 0) and (kind != 'roulette' or x[1] != 0)]
    if query in ('S', 'D', 'C', 'H', 'T', 'RED', 'BLACK'):
        suits = {'BLACK': 'SC', 'RED': 'DH'}.get(query, query)
        return [i for i, x in enumerate(outcomes) if x[0][-1] in suits]
    if kind == 'roulette':
        for op in ('!=', '='):
            if query.startswith(op) and query[len(op):].strip() in ('0', '00'):
                label = query[len(op):].strip()
                return [i for i, x in enumerate(outcomes) if (x[0] == label) == (op == '=')]
    for op in ('<=', '>=', '!=', '<', '>', '='):
        if query.startswith(op):
            a = STCORE.as_ratio(query[len(op):])
            return [i for i, x in enumerate(outcomes) if STCORE.event_match(x[1], op, a)]
    if query == '00' or (kind == 'roulette' and query == '0'):
        return [i for i, x in enumerate(outcomes) if x[0] == query]
    try:
        a = STCORE.as_ratio(query)
        return [i for i, x in enumerate(outcomes) if STCORE.compare_exact(x[1], a) == 0]
    except ValueError:
        return [i for i, x in enumerate(outcomes) if x[0] == query]
