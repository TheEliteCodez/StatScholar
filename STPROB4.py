import STCORE as c
def category_session():
    labels = []
    counts = []
    c.heading('F02 CATEGORY COUNTS')
    for i in range(c.read_size('NUMBER OF CATEGORIES: ', c.MAX_OUTCOMES)):
        labels.append(input('CATEGORY NAME: '))
        counts.append(c.read_int('COUNT: '))
    total = sum(counts)
    selected = None
    while True:
        key = c.menu('SELECT CATEGORY', [(str(i + 1), x) for i, x in enumerate(labels)] + [('E', 'COMPARE EXPECTED P'),('C','EDIT CATEGORY COUNT'),('T','SHOW ALL PROPORTIONS')])
        if key == '0':
            return
        if key=='T':
            work=c.call('STWORK','Lines',len(labels),lambda i:'P(%s)=%d/%d=%.10g; PERCENT=(%d/%d)*100=%.10g%%' % (labels[i],counts[i],total,counts[i]/total,counts[i],total,100*counts[i]/total))
            c.paged_results('CATEGORY PROPORTIONS',len(labels),lambda i:(labels[i],c.ratio(counts[i],total)),work,graph=('STGDATA','show',(list(zip(labels,counts)),'category','CATEGORY COUNTS',selected)));continue
        if key=='C':
            i=c.read_size('CATEGORY NUMBER: ',len(labels))-1
            labels[i]=input('CATEGORY NAME: ');counts[i]=c.read_int('COUNT: ');total=sum(counts);continue
        if key == 'E':
            if selected is None:
                c.view('SELECT CATEGORY FIRST', ['CHOOSE THE CATEGORY TO COMPARE'])
                continue
            target = c.read_exact('EXPECTED PROBABILITY: ')
            estimate = c.ratio(counts[selected], total)
            delta = c.radd(estimate, (-target[0], target[1]))
            c.results('F02 COMPARE', [('ESTIMATED P', estimate), ('EXPECTED P', target), ('DIFFERENCE (PERCENT POINTS)', c.rmul(delta, (100, 1)))],
                      c.call('STWORK','ratio_work','ESTIMATED P',counts[selected],total)+[
                      'DIFFERENCE=(%s-%s)*100=%s PERCENT POINTS' % (c.exact_text(estimate),c.exact_text(target),c.exact_text(c.rmul(delta,(100,1))))])
            continue
        i = int(key) - 1
        selected = i
        c.results('F02 / P01 / P02', [('P(' + labels[i] + ')', c.ratio(counts[i], total)), ('P(NOT)', c.ratio(total - counts[i], total))],
                  c.call('STWORK','ratio_work','P('+labels[i]+')',counts[i],total)+
                  c.call('STWORK','ratio_work','P(NOT)',total-counts[i],total),graph=('STGDATA','show',(list(zip(labels,counts)),'category','CATEGORY COUNTS',selected)))
