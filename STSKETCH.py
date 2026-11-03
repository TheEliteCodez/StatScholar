import STCORE as c

def curve(kind,center,spread,event=None,bounds=(),label=None):
    lines=['HOW TO DRAW: '+kind]
    if kind=='UNIFORM':
        lines+=['RECTANGLE FROM %.4f TO %.4f' % (center,spread),
                'HEIGHT=%.4f' % (1/(spread-center)),
                'ZERO HEIGHT OUTSIDE ENDPOINTS.']
    elif kind=='t':
        lines+=['SYMMETRIC t BELL; CENTER=0.',
                'LABEL HORIZONTAL AXIS t.',
                'df=%.4f; HEAVIER TAILS THAN z.' % spread]
    else:
        lines+=['DRAW A SYMMETRIC NORMAL BELL.',
                'CENTER=%.4f; SD=%.4f' % (center,spread),
                'LABEL x AXIS; z=0 AT CENTER.']
        lines+=['z=%+d: x=%.4f' % (i,center+i*spread) for i in range(-3,4)]
    lines+=['MARK CUTOFF: '+str(x) for x in bounds]
    if event:
        lines.append({'1':'SHADE LEFT OF CUTOFF.',
                      '2':'SHADE RIGHT OF CUTOFF.',
                      '3':'SHADE BETWEEN CUTOFFS.',
                      'outside':'SHADE BOTH OUTSIDE TAILS.'}[event])
    return c.call('STGATT','attach',lines,'STGCURV','show',(kind,center,spread,event,bounds,label))

def confidence(estimate,low,high,level,critical,kind,label='ESTIMATE'):
    lines=['HOW TO DRAW: CONFIDENCE INTERVAL',
            'DRAW A HORIZONTAL NUMBER LINE.',
            'LEFT END=%.4f' % low,'CENTER ESTIMATE=%.4f' % estimate,
            'RIGHT END=%.4f' % high,'CONNECT ENDPOINTS; MARK CENTER.',
            'LABEL INTERVAL %.2f%% CONFIDENCE.' % (100*level),
            'CRITICAL-VALUE CURVE: '+kind,
            'BELL CENTER=0; MARK +/-%.4f' % critical,
            'SHADE MIDDLE AREA=%.4f' % level,
            'EACH OUTSIDE TAIL=%.4f' % ((1-level)/2)]
    return c.call('STGATT','attach',lines,'STGINTR','show',(estimate,low,high,level,label))

def bars(low,high,event=None):
    lines=['HOW TO DRAW: PROBABILITY BARS',
           'X AXIS: '+str(low)+' TO '+str(high),
           'VERTICAL AXIS: P(X).',
           'EQUAL-WIDTH BARS AT EACH X.',
           'HEIGHT=CORRESPONDING TABLE P.',
           'KEEP NUMERIC SPACING; NO BELL.']
    if event:
        op,a,b=event
        lines+=['SHADE ONLY BARS MATCHING:',
                (op[0]+c.exact_text(a)+', '+c.exact_text(b)+op[1] if op in ('[]','()','[)','(]') else 'X '+op+' '+c.exact_text(a)),
                'BRACKETS INCLUDE ENDPOINTS.',
                'PARENTHESES EXCLUDE ENDPOINTS.',
                'SHADED BAR HEIGHTS ADD TO P.']
    return lines

def position(mean,sd,x):
    lines=['HOW TO DRAW: x / z AXES',
            'DRAW ALIGNED NUMBER LINES.',
            'x CENTER='+c.exact_text(mean)+'; z CENTER=0',
            'x TICK SPACING='+c.exact_text(sd)+'; z SPACING=1',
            'MARK x='+c.exact_text(x)+' ON x AXIS.',
            'MARK ITS z DIRECTLY BELOW.',
            'BELL CURVE ONLY IF NORMAL.',
            'A z-SCORE ALONE IS NOT AN AREA.']
    return c.call('STGATT','attach',lines,'STGCURV','show',('POSITION',c.number(mean),c.number(sd),None,(c.number(x),)))

def venn(total,a,b,both):
    lines=['HOW TO DRAW: VENN',
            'RECTANGLE TOTAL='+str(total),
            'DRAW OVERLAPPING CIRCLES A, B.',
            'OVERLAP='+str(both),'A ONLY='+str(a-both),
            'B ONLY='+str(b-both),'OUTSIDE BOTH='+str(total-a-b+both),
            'OR: SHADE BOTH CIRCLES.',
            'AND: SHADE ONLY OVERLAP.',
            'GIVEN A: USE A AS TOTAL.',
            'GIVEN B: USE B AS TOTAL.']
    return c.call('STGATT','attach',lines,'STGDIAG','venn',(total,a,b,both))
