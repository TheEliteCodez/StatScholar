# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Event-expression matcher for experiments, loaded only while matching.
import STCORE


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
