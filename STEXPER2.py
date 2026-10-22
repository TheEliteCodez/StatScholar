import STCORE
def _val(x, kind):
    return x % 13 + 1 if kind == 'cards' and isinstance(x, int) else x[1]
def _lab(x, kind):
    return str(x % 13 + 1) + 'SDCH'[x // 13] if kind == 'cards' and isinstance(x, int) else x[0]
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
        return [i for i, x in enumerate(outcomes) if _val(x, kind) % 2 == (1 if query == 'ODD' else 0) and (kind != 'roulette' or _val(x, kind) != 0)]
    if query in ('S', 'D', 'C', 'H', 'T', 'RED', 'BLACK'):
        suits = {'BLACK': 'SC', 'RED': 'DH'}.get(query, query)
        return [i for i, x in enumerate(outcomes) if _lab(x, kind)[-1] in suits]
    if kind == 'roulette':
        for op in ('!=', '='):
            if query.startswith(op) and query[len(op):].strip() in ('0', '00'):
                lab = query[len(op):].strip()
                return [i for i, x in enumerate(outcomes) if (_lab(x, kind) == lab) == (op == '=')]
    for op in ('<=', '>=', '!=', '<', '>', '='):
        if query.startswith(op):
            a = STCORE.as_ratio(query[len(op):])
            return [i for i, x in enumerate(outcomes) if STCORE.event_match(_val(x, kind), op, a)]
    if query == '00' or (kind == 'roulette' and query == '0'):
        return [i for i, x in enumerate(outcomes) if _lab(x, kind) == query]
    try:
        a = STCORE.as_ratio(query)
        return [i for i, x in enumerate(outcomes) if STCORE.compare_exact(_val(x, kind), a) == 0]
    except ValueError:
        return [i for i, x in enumerate(outcomes) if _lab(x, kind) == query]
