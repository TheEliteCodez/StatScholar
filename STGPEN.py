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
        glyph=FONT.get(char,FONT.get(char.lower(),b'\x00'*5))
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


def number(x):
    return x[0]/x[1] if isinstance(x,tuple) else x

def frame(title,xlabel='',ylabel=''):
    try: import ti_plotlib as plt
    except ImportError: return None
    plt.cls();plt.window(0,319,0,209);plt.pen('thin','solid');plt.color(*BLACK)
    plt.text_at(1,title[:40],'center')
    plt.text_at(2,xlabel[:40],'center');plt.text_at(11,ylabel[:40],'center')
    plt.text_at(12,'LEFT = BACK  RIGHT = NEXT','center')
    return plt

def scale(value,low,high,a=26,b=306):
    return (a+b)/2 if high==low else a+(b-a)*(value-low)/(high-low)

def dot(plt,x,y,color=BLUE):
    plt.color(*color);plt.pen('medium','solid')
    line(plt,x-1,y,x+1,y);line(plt,x,y-1,x,y+1)
    plt.pen('thin','solid')

def axes(plt,low,high,ymax=1):
    plt.color(*BLACK);line(plt,26,164,306,164);line(plt,26,36,26,164)
    ink(plt,'%.4g'%low,26,170,BLACK);ink(plt,'%.4g'%high,278,170,BLACK)
    ink(plt,'%.4g'%ymax,2,38,BLACK);ink(plt,'0',14,157,BLACK)
