import STCORE
from STWORK import num
def frequency_stats(rows):
    counts = {}
    for x, f in rows:
        counts[x] = counts.get(x, 0) + f
    ordered = STCORE.exact_sorted([x for x in counts if counts[x] > 0])
    total = sum((counts[x] for x in ordered))
    if total == 0:
        raise ValueError('NO OBSERVATIONS')
    weighted = STCORE.rsum([STCORE.rmul(x, (counts[x], 1)) for x in ordered])
    positions = [(total + 1) // 2, total // 2 + 1]
    mid = []
    running = 0
    for x in ordered:
        before = running
        running += counts[x]
        for pos in positions:
            if before < pos <= running:
                mid.append(x)
    median = STCORE.rdiv(STCORE.rsum(mid), (2, 1))
    peak = max(counts.values())
    modes = [x for x in ordered if counts[x] == peak]
    if peak==1 or len(modes) == len(ordered) and len(ordered) > 1 or len(modes) > 2:
        mode = 'DNE'
    else:
        mode = ','.join((STCORE.exact_text(x) for x in modes))
    return (total, weighted, STCORE.rdiv(weighted, (total, 1)), median, mode, positions)
def frequency_session(rows=None):
    STCORE.heading('F05-F07 VALUE/FREQUENCY')
    if rows is None:
        rows = []
        for i in range(STCORE.read_size('NUMBER OF ROWS: ', STCORE.MAX_ROWS)):
            print('ROW ' + str(i + 1))
            rows.append((STCORE.read_exact('DATA VALUE: '), STCORE.read_int('FREQUENCY: ')))
    n, w, mean, median, mode, pos = frequency_stats(rows)
    counts = {}
    for x, f in rows:
        counts[x] = counts.get(x, 0) + f
    ordered=STCORE.exact_sorted(counts)
    def detail(i):
        at,part=divmod(i,3);x=ordered[at];f=counts[x]
        cumulative=sum(counts[ordered[j]] for j in range(at+1))
        if part==0: return 'x='+num(x)+' f='+str(f)
        if part==1: return 'CUMULATIVE f='+str(cumulative)
        return 'RELATIVE f=%d/%d=%.10g' % (f,n,f/n)
    stats=STCORE.call('STDMATH','weighted_stats',rows)
    STCORE.results('F05/F06/F07/F03', [('MEAN', mean), ('MEDIAN', median), ('MODE', mode)],
                   STCORE.call('STWORK','Chain',['n=SUM(f)='+str(n),'MIDDLE POS='+str(pos[0])+','+str(pos[1])],
                               STCORE.call('STDWK','descriptive',stats,None,rows),STCORE.call('STWORK','Lines',3*len(ordered),detail)))
