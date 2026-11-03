import math

def wait(plt):
    import STCORE as c
    try: import ti_system as keys
    except ImportError:
        plt.show_plot()
        return 'next'
    poll=getattr(keys,'get_key',None)
    read=(lambda:poll(0)) if poll else getattr(keys,'wait_key',None)
    if read is None:
        plt.show_plot()
        return 'next'
    # Ignore the key that opened the graph, then consume the closing key's
    # release so it cannot also dismiss the following result or menu.
    if poll:
        while read() not in (0,None,''): pass
    while True:
        raw=read();key=c.normalize_key(raw)
        if key in ('left','esc','clear','back','0') or raw in ((142,62,153) if c.KEY_STYLE=='ce' else (102,)):
            action='back'
        elif key in ('enter','right'): action='next'
        else: continue
        if poll:
            while read() not in (0,None,''): pass
        c._LAST_RAW=None
        plt.cls()
        return action

def height(x,degrees):
    if degrees is None: return math.exp(-x*x/2)
    return (1+x*x/degrees)**(-(degrees+1)/2)

def shaded(x,statistic,alternative):
    if alternative=='<': return x<=statistic
    if alternative=='>': return x>=statistic
    return abs(x)>=abs(statistic)

def original(setup,result,score):
    return setup['null']+score*result['se']

# Compact 5x7 glyphs provide labels at actual graph coordinates. PlotLib's
# text_at positions whole rows, so it cannot attach labels to individual marks.
FONT={
'0':b'\x3e\x51\x49\x45\x3e','1':b'\x00\x42\x7f\x40\x00',
'2':b'\x42\x61\x51\x49\x46','3':b'\x21\x41\x45\x4b\x31',
'4':b'\x18\x14\x12\x7f\x10','5':b'\x27\x45\x45\x45\x39',
'6':b'\x3c\x4a\x49\x49\x30','7':b'\x01\x71\x09\x05\x03',
'8':b'\x36\x49\x49\x49\x36','9':b'\x06\x49\x49\x29\x1e',
'C':b'\x3e\x41\x41\x41\x22','V':b'\x1f\x20\x40\x20\x1f',
'T':b'\x01\x01\x7f\x01\x01','S':b'\x46\x49\x49\x49\x31',
'H':b'\x7f\x08\x08\x08\x7f','P':b'\x7f\x09\x09\x09\x06',
'E':b'\x7f\x49\x49\x49\x41','=':b'\x14\x14\x14\x14\x14',
'-':b'\x08\x08\x08\x08\x08','+':b'\x08\x08\x3e\x08\x08',
'.':b'\x00\x60\x60\x00\x00','/':b'\x20\x10\x08\x04\x02',
'e':b'\x38\x54\x54\x54\x18','t':b'\x04\x3f\x44\x40\x20',
'z':b'\x44\x64\x54\x4c\x44','x':b'\x44\x28\x10\x28\x44',
'b':b'\x7f\x48\x44\x44\x38','a':b'\x20\x54\x54\x54\x78',
'r':b'\x7c\x08\x04\x04\x08','p':b'\x7c\x14\x14\x14\x08',
'h':b'\x7f\x08\x04\x04\x78','d':b'\x38\x44\x44\x48\x7f',
'l':b'\x00\x41\x7f\x40\x00'}
BLACK=(0,0,0);RED=(210,45,45);GREEN=(0,135,55);BLUE=(0,100,210)

def line(plt,x1,y1,x2,y2):
    plt.line(x1,209-y1,x2,209-y2)

def position(score,extent):
    return 8+303*(score+extent)/(2*extent)

def ink(plt,text,x,y,color):
    x=max(1,min(318-(6*len(text)-1),x))
    plt.pen('medium','solid');plt.color(255,255,255)
    for row in range(-1,8): line(plt,x-1,y+row,x+6*len(text),y+row)
    plt.pen('thin','solid');plt.color(*color)
    for char in text:
        glyph=FONT[char]
        for col,bits in enumerate(glyph):
            for row in range(7):
                if bits & (1<<row):
                    line(plt,x+col,y+row,x+col+.3,y+row)
                    if row<6 and bits & (1<<(row+1)):
                        line(plt,x+col,y+row,x+col,y+row+1)
                    if col<4:
                        for r in range(max(0,row-1),min(7,row+2)):
                            if glyph[col+1] & (1<<r): line(plt,x+col,y+row,x+col+1,y+r)
        x+=6

def tag(plt,text,x,y,color,boxes):
    width=6*len(text)-1
    left=max(1,min(318-width,x+6 if x>=159.5 else x-width-6))
    if y<55: left=1 if x<159.5 else 318-width
    wanted=max(36,min(82,y-15))
    for top in (wanted,36,46,56,66,76,86):
        if all(left+width+2<a or left>b+2 or top+9<c or top>d+2 for a,b,c,d in boxes): break
    boxes.append((left,left+width,top,top+7))
    plt.color(*color)
    line(plt,left+width/2,top+8,x,y)
    ink(plt,text,left,top,color)

def show(setup,result,probability,critical,region='p'):
    try: import ti_plotlib as plt
    except ImportError: return False
    ts=result['ts'];df=result['df'];alt=setup['alternative'];alpha=setup['alpha']
    extent=max(3.5,abs(ts)+.7,max(abs(v) for v in critical)+.7)
    at=lambda score:position(score,extent)
    y=lambda score:100-60*height(score,df)
    plt.cls();plt.window(0,319,0,209)
    plt.pen('medium','solid');plt.color(*(BLUE if region=='p' else RED))
    boundary=ts if region=='p' else (critical[0] if alt=='<' else critical[-1])
    for i in range(241):
        score=-extent+2*extent*i/240
        if shaded(score,boundary,alt): line(plt,at(score),100,at(score),y(score))
    for score in ((boundary,) if alt!='!=' else (-abs(boundary),abs(boundary))):
        line(plt,at(score),100,at(score),y(score))
    plt.pen('thin','solid');plt.color(*BLACK)
    previous=(-extent,y(-extent))
    for i in range(1,241):
        score=-extent+2*extent*i/240
        line(plt,at(previous[0]),previous[1],at(score),y(score));previous=(score,y(score))
    line(plt,8,100,311,100);line(plt,8,132,311,132)
    plt.color(140,140,140);line(plt,at(0),100,at(0),y(0))
    for score in (0,ts)+tuple(critical):
        line(plt,at(score),100,at(score),132)
    for score in (0,)+tuple(critical)+(ts,):
        plt.color(*(GREEN if score==ts else RED if score in critical else BLACK))
        line(plt,at(score),100,at(score),104);line(plt,at(score),132,at(score),136)
    boxes=[]
    for score in critical:
        plt.color(*RED);line(plt,at(score),100,at(score),max(36,y(score)-8))
        tag(plt,'CV=%.4g' % score,at(score),max(36,y(score)-8),RED,boxes)
    plt.color(*GREEN);line(plt,at(ts),100,at(ts),max(36,y(ts)-8))
    tag(plt,'TS=%.4g' % ts,at(ts),max(36,y(ts)-8),GREEN,boxes)
    bounds=(boundary,) if alt!='!=' else (-abs(boundary),abs(boundary))
    for i,score in enumerate(bounds):
        middle=(score-extent)/2 if alt=='<' or (alt=='!=' and i==0) else (score+extent)/2
        text=('p' if region=='p' else 'alpha')+('/2' if alt=='!=' else '')+'=%.4g' % ((probability if region=='p' else alpha)/(2 if alt=='!=' else 1))
        tag(plt,text,at(middle),100-(100-y(middle))/2,BLUE if region=='p' else RED,boxes)
    kind='z' if df is None else 't'
    symbol={'mu':'x-bar','p':'p-hat','mu1-mu2':'x1bar-x2bar','p1-p2':'p1hat-p2hat','mu_d':'d-bar'}[setup['parameter']]
    ink(plt,kind,1,91,BLACK);ink(plt,symbol,1,124,BLACK)
    ink(plt,kind+'=0',at(0)-9,107,BLACK)
    ink(plt,'H0=%.5g' % setup['null'],at(0)-3*len('H0=%.5g' % setup['null']),139,BLACK)
    for score in critical:
        text=kind+'=%.4g' % score;ink(plt,text,at(score)-3*len(text),107,RED)
        text='%.5g' % original(setup,result,score);ink(plt,text,at(score)-3*len(text),139,RED)
    text=kind+'=%.4g' % ts;ink(plt,text,at(ts)-3*len(text),117,GREEN)
    text='%.5g' % result['estimate'];ink(plt,text,at(ts)-3*len(text),149,GREEN)
    plt.color(*BLACK)
    plt.text_at(1,'STANDARD NORMAL (z)' if df is None else 't DISTRIBUTION df=%.5g' % df,'center')
    tail={'<':'LEFT','>':'RIGHT','!=':'TWO-TAILED'}[alt]
    plt.text_at(2,tail+(' REJECTION REGION' if region!='p' else ' p-VALUE REGION'),'center')
    if region=='p':
        plt.text_at(10,'SHADE '+('LEFT OF TS' if alt=='<' else 'RIGHT OF TS' if alt=='>' else 'BEYOND +/-abs(TS)'),'center')
        plt.color(*BLUE);plt.text_at(11,'p-VALUE=%.6g' % probability,'center')
    else:
        comparison=('TS' if alt!='!=' else '|TS|')
        a,b=(abs(ts),critical[-1]) if alt=='!=' else (ts,critical[0])
        comparison+=' > CV' if a>b else ' < CV' if a<b else ' = CV'
        plt.text_at(10,comparison+(': REJECT H0' if probability<=alpha else ': FAIL TO REJECT H0'),'center')
        plt.color(*RED);plt.text_at(11,'SHADE '+('LEFT OF CV' if alt=='<' else 'RIGHT OF CV' if alt=='>' else 'BOTH OUTSIDE CVs')+'; alpha=%.4g' % alpha,'center')
    plt.color(*BLACK);plt.text_at(12,'LEFT/CLEAR:BACK ENTER:NEXT','center')
    return wait(plt)

def screens(setup,result,probability,critical):
    for region in ('alpha','p'):
        action=show(setup,result,probability,critical,region)
        if not action or action=='back': return action
    return 'next'
