import STCORE

def experiment_inputs(kind):
    STCORE.heading('P01 / C05 EXPERIMENT')
    if kind == 'roulette':
        zeros = STCORE.read_size('ZERO SPACES (0,00 -> 2): ', STCORE.MAX_OUTCOMES-1, 0)
        last = STCORE.read_size('LAST NUMBER (USUALLY 36): ', STCORE.MAX_OUTCOMES-zeros)
        outcomes = [(str(k), k) for k in range(1, last + 1)] + [('0' * (i + 1), 0) for i in range(zeros)]
    elif kind == 'cards':
        outcomes = list(range(52))
        print('52 CARDS; ACE=1 J=11 Q=12 K=13')
        print('S SPADES; D DIAMONDS')
        print('C CLUBS; H HEARTS')
        print('ALSO RED OR BLACK')
        if STCORE.HAS_KEYS:
            STCORE.wait_key()
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
