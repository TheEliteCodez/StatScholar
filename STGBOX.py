from STGPEN import frame,line,ink,scale,dot,number,wait,BLACK,BLUE,RED

def summary(values):
    import STCORE as c
    q1,med,q3,iqr,lo,hi,wl,wh,out=c.call('STGRAPH','boxplot_values',values)
    return tuple(number(x) for x in (values[0],q1,med,q3,values[-1],wl,wh)),tuple(number(x) for x in out)

def compare(a,b):return show((summary(a),summary(b)))

def show(boxes):
    low=min(b[0][0] for b in boxes);high=max(b[0][4] for b in boxes);pad=(high-low)*.1 or 1
    plt=frame('BOXPLOT'+(' COMPARISON' if len(boxes)>1 else ''),'SAME NUMERIC SCALE','RED DOTS = OUTLIERS')
    if plt is None:return False
    at=lambda x:scale(x,low-pad,high+pad)
    line(plt,26,165,306,165);ink(plt,'%.5g'%low,at(low)-10,166,BLACK);ink(plt,'%.5g'%high,at(high)-10,166,BLACK)
    for i,(box,out) in enumerate(boxes):
        mn,q1,med,q3,mx,wl,wh=box;y=65+i*60
        plt.color(*BLUE);line(plt,at(wl),y,at(wh),y)
        for x in (wl,wh):line(plt,at(x),y-8,at(x),y+8)
        for x in (q1,med,q3):line(plt,at(x),y-17,at(x),y+17)
        line(plt,at(q1),y-17,at(q3),y-17);line(plt,at(q1),y+17,at(q3),y+17)
        for x in out:dot(plt,at(x),y,RED)
        for j,x in enumerate((wl,q1,med,q3,wh)):ink(plt,'%.4g'%x,at(x)-10,y+20+(j%2)*9,BLACK)
    return wait(plt)
