import STCORE as c
def missing_probability():
    c.heading('R05 MISSING PROBABILITY')
    print('EACH P MUST BE 0 TO 1')
    known = []
    count = c.read_size('HOW MANY KNOWN P? ', c.MAX_ROWS)
    for i in range(count):
        while True:
            p = c.read_exact('KNOWN P ' + str(i + 1) + '/' + str(count) + ': ')
            if c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0:
                break
            c.view('R05', ['PROBABILITIES ARE 0..1', 'TRY AGAIN'])
        known.append(p)
    total = c.rsum(known)
    if c.compare_exact(total, 1) > 0:
        c.view('R05', ['KNOWN SUM=' + c.exact_text(total), 'SUM CANNOT EXCEED 1', 'CHECK YOUR P VALUES'])
        return
    missing = c.radd((1, 1), (-total[0], total[1]))
    c.results('R05', [('MISSING P', missing)], ['P=1-SUM(KNOWN P)', 'KNOWN SUM=' + c.exact_text(total), 'ONE UNKNOWN CAN BE FOUND', 'X LABELS NOT NEEDED'])
def read_sample_distribution():
    total=c.read_int('TOTAL OBJECTS N: ')
    targets=c.read_int('TARGET OBJECTS K: ')
    draws=c.read_int('NUMBER SELECTED n: ')
    return c.call('STCOUNT', 'hyper_distribution', total, targets, draws)
def rounded_distribution_session():
    rows,approximate=c.call('STCOUNT', 'read_distribution', True)
    c.call('STCOUNT', 'distribution_session', rows, approximate)
def heights_page(rows, approximate):
    c.paged_results('APPROXIMATE HEIGHTS' if approximate else 'PROBABILITY HISTOGRAM',len(rows),lambda i:('x='+c.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=P(X)', 'INCLUDE EVERY X, INCLUDING ZERO', 'NUMERIC x AXIS; PROBABILITY y AXIS', 'APPROXIMATE HEIGHTS: ROUNDED TABLE' if approximate else 'USE EQUAL-WIDTH BARS'])
def check_table(rows, note, approximate):
    valid = all((c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0 for x, p in rows)) and c.rsum([p for x, p in rows]) == (1, 1)
    lines = note + ['VALID=' + ('UNKNOWN (ROUNDED)' if approximate else str(valid))]
    lines += [c.exact_text(x) + ': ' + c.answer_text(p, 'F') for x, p in rows]
    c.view('R01 TABLE', lines)

def discrete_tools(count,row_at,title,approximate=False):
    from STEFMT import rsum
    order=[]
    for i in range(count):
        x,p=row_at(i)
        if c.compare_exact(p,0)<0 or c.compare_exact(p,1)>0:
            raise ValueError('TABLE PROBABILITIES MUST BE 0..1')
        at=len(order)
        while at and c.compare_exact(row_at(order[at-1])[0],x)>0: at-=1
        order.insert(at,i)
    starts=[i for i in range(count) if i==0 or c.compare_exact(row_at(order[i])[0],row_at(order[i-1])[0])!=0]
    def row(i):
        low=starts[i];high=starts[i+1] if i+1<len(starts) else len(order)
        return row_at(order[low])[0],rsum(row_at(order[j])[1] for j in range(low,high))
    count=len(starts)
    def cumulative(x):
        return c.rsum(row(i)[1] for i in range(count) if c.compare_exact(row(i)[0],x)<=0)
    total=c.rsum(row(i)[1] for i in range(count))
    note=['X=VALUE; P=P(X=x); CDF=P(X<=x).',
          'SUM P='+c.exact_text(total),
          'ROUNDED INPUT: APPROXIMATE OUTPUT.' if approximate else 'EXACT ENTERED MODEL.']
    drawing=c.call('STSKETCH','bars',c.exact_text(row(0)[0]),c.exact_text(row(count-1)[0]))
    while True:
        key=c.menu(title+' > TABLE TOOLS',[
            ('1','PROBABILITY TABLE / BAR HEIGHTS'),('2','CUMULATIVE PROBABILITY TABLE'),
            ('3','WORK TABLE: P, xP, x^2P'),('4','PERCENTILE / DISCRETE CUTOFF'),
            ('5','EXPECTED FREQUENCIES'),('6','MEAN / VAR / SD / SUMS')])
        if key=='0': return
        if key=='1':
            c.paged_results(title+' > P(x)',count,lambda i:('x='+c.exact_text(row(i)[0]),row(i)[1]),note,drawing=drawing)
        elif key=='2':
            c.paged_results(title+' > CDF',count,lambda i:('P(X<='+c.exact_text(row(i)[0])+')',cumulative(row(i)[0])),note,drawing=drawing)
        elif key=='3':
            def cell(i):
                x,p=row(i//3)
                values=(p,c.rmul(x,p),c.rmul(c.rmul(x,x),p))
                return ('x='+c.exact_text(x)+' '+('P','xP','x^2P')[i%3],values[i%3])
            mean=c.rsum(c.rmul(*row(i)) for i in range(count))
            second=c.rsum(c.rmul(c.rmul(row(i)[0],row(i)[0]),row(i)[1]) for i in range(count))
            if not approximate and total==(1,1):
                square=c.rmul(mean,mean)
                variance=c.radd(second,(-square[0],square[1]))
                import math
                work=c.call('STDWK','moments',count,row,mean,variance,math.sqrt(c.number(variance)))
            else:
                work=c.call('STWORK','Chain',
                    c.call('STWORK','sum_work','SUM xP',count,lambda i:'('+c.exact_text(row(i)[0])+'*'+c.exact_text(row(i)[1])+')',mean),
                    c.call('STWORK','sum_work','SUM x^2P',count,lambda i:'('+c.exact_text(row(i)[0])+'^2*'+c.exact_text(row(i)[1])+')',second),
                    ['ROUNDED / UNNORMALIZED: THESE ARE WEIGHTED SUMS, NOT EXACT MOMENTS.'])
            c.paged_results(title+' > WORK TABLE',3*count,cell,c.call('STWORK','Chain',note,work))
        elif key=='5':
            repeats=c.read_int('NUMBER OF REPEATED EXPERIMENTS: ')
            if repeats<0: raise ValueError('REPETITIONS MUST BE NONNEGATIVE')
            c.paged_results(title+' > EXPECTED COUNTS',count,lambda i:('x='+c.exact_text(row(i)[0]),c.rmul((repeats,1),row(i)[1])),note+['EXPECTED COUNT=m*P(x); m='+str(repeats), 'EXPECTED, NOT OBSERVED COUNTS.'])
        else:
            if approximate or total!=(1,1):
                c.view('EXACT MODEL NEEDED',note+['EXACT MOMENTS / CUTOFF NEED P SUMMING TO 1.']);continue
            if key=='4':
                area=c.read_exact('PERCENTILE / LEFT AREA: ')
                if c.compare_exact(area,0)<0 or c.compare_exact(area,1)>0: raise ValueError('USE AREA 0..1')
                running=(0,1)
                for i in range(count):
                    x,p=row(i);running=c.radd(running,p)
                    if c.compare_exact(running,area)>=0: break
                left=cumulative(x)
                point=c.rsum(row(j)[1] for j in range(count) if c.compare_exact(row(j)[0],x)==0)
                below=c.radd(left,(-point[0],point[1]))
                c.results(title+' > CUTOFF',[('x CUTOFF',x),('P(X<x)',below),('P(X<=x)',left)],note+['SMALLEST LISTED x WITH CDF>=GIVEN AREA.', 'CDF MAY JUMP PAST THE REQUESTED AREA.', 'AREA 0 USES MINIMUM LISTED x.'])
            else:
                mean=c.rsum(c.rmul(*row(i)) for i in range(count))
                second=c.rsum(c.rmul(c.rmul(row(i)[0],row(i)[0]),row(i)[1]) for i in range(count))
                variance=c.radd(second,(-c.rmul(mean,mean)[0],c.rmul(mean,mean)[1]))
                import math
                sd=math.sqrt(c.number(variance))
                c.results(title+' > SUMMARY',[('SUM P',total),('SUM xP / MEAN',mean),('SUM x^2P',second),('VAR',variance),('SD',sd)],
                          c.call('STWORK','Chain',note,c.call('STDWK','moments',count,row,mean,variance,sd)))
