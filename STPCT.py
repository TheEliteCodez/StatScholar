import STCORE as c
def percent_session():
    total=c.read_exact('TOTAL: ')
    rate=c.read_exact('PERCENT (45% OR .45): ')
    answer=c.rmul(total,rate)
    c.results('PERCENT OF TOTAL',[('ANSWER',answer)],['TOTAL * PERCENT/100',
        'ANSWER=%s*(%s)=%s' % (c.exact_text(total),c.exact_text(rate),c.exact_text(answer)),
        'ENTERED RATE AS PERCENT=(%s)*100=%s%%' % (c.exact_text(rate),c.fixed(c.rmul(rate,(100,1)),4)),
        'ENTER 45% OR .45, NOT 45','FOR WHOLE ITEMS, ROUND ONLY IF THE QUESTION ALLOWS AN APPROXIMATION.','NEAREST WHOLE: '+c.fixed(answer,0)])
def frequency_lines(rows):
    total=sum(f for x,f in rows)
    if total<=0: raise ValueError('NEED POSITIVE TOTAL FREQUENCY')
    cumulative=0
    for x in c.exact_sorted(set(x for x,f in rows)):
        f=sum(f for value,f in rows if c.compare_exact(value,x)==0)
        cumulative+=f
        yield 'VALUE='+c.exact_text(x)+' COUNT='+str(f)
        yield 'RELATIVE='+str(f)+'/'+str(total)+'='+c.fixed(c.ratio(f,total),4)
        yield 'CUM COUNT='+str(cumulative)
        yield 'CUM REL='+str(cumulative)+'/'+str(total)+'='+c.fixed(c.ratio(cumulative,total),4)
def frequency_event(rows,op,cutoff):
    total=sum(f for x,f in rows)
    selected=0
    for x,f in rows:
        comparison=c.compare_exact(x,cutoff)
        if {'=':comparison==0,'<=':comparison<=0,'>=':comparison>=0,'<':comparison<0,'>':comparison>0}[op]: selected+=f
    return c.ratio(selected,total)
def frequency_tools(rows=None):
    if rows is None: rows=c.call('STDMATH','read_frequency_rows')
    while True:
        key=c.menu('FREQUENCY TABLE',[('1','RELATIVE / CUMULATIVE'),('2','EXACTLY'),('3','AT MOST'),('4','AT LEAST'),('5','LESS THAN'),('6','MORE THAN'),('7','BETWEEN')])
        if key=='0': return
        if key=='1': c.call('STSTUDY','definition_pages','TABLE / IN VALUE ORDER','; '.join(frequency_lines(rows)))
        elif key=='7':
            event=c.call('STBWE','read_event','[]')
            if event:
                total=sum(f for x,f in rows)
                matching=sum(f for x,f in rows if c.event_match(x,*event))
                c.results('FREQUENCY BETWEEN',[('PROPORTION',c.ratio(matching,total))],c.call('STWORK','ratio_work','PROPORTION',matching,total),graph=('STGBARS','show',(('rows',[(x,c.ratio(f,total)) for x,f in rows]),event,'FREQUENCY EVENT')))
        else:
            op={'2':'=','3':'<=','4':'>=','5':'<','6':'>'}[key]
            cutoff=c.read_exact('CATEGORY / VALUE CUTOFF: ')
            probability=frequency_event(rows,op,cutoff)
            total=sum(f for x,f in rows)
            matching=probability[0]*total//probability[1]
            c.results('FREQUENCY > X'+op+c.exact_text(cutoff),[('PROPORTION',probability)],
                      c.call('STWORK','ratio_work','PROPORTION',matching,total),graph=('STGBARS','show',(('rows',[(x,c.ratio(f,total)) for x,f in rows]),(op,cutoff,0),'FREQUENCY EVENT')))
