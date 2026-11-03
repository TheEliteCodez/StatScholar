import math
import STCORE as c
from STGPEN import frame,line,ink,tag,scale,wait,BLACK,BLUE,RED

def cdf(kind,x,center,spread):
    if abs(x)==float('inf'):return float(x>0)
    if kind=='UNIFORM': return max(0,min(1,(x-center)/(spread-center)))
    if kind=='t': return c.call('STTCRIT','t_cdf',x,spread)
    if kind=='CHI': return 1-c.call('STCHIM','survival',max(0,x),spread)
    if spread==0: return float(x>=center)
    return c.call('STCLTM','normal_cdf',(x-center)/spread)

def area(kind,center,spread,event,bounds):
    if not event or not bounds: return None
    if spread==0 and kind=='NORMAL':
        return float(center<bounds[0]) if event=='1' else float(center>bounds[0]) if event=='2' else float(bounds[0]<=center<=bounds[-1]) if event=='3' else float(center<=bounds[0] or center>=bounds[-1])
    a=cdf(kind,bounds[0],center,spread)
    if event=='1': return a
    if event=='2':
        if kind=='NORMAL' and spread: return c.call('STCLTM','normal_sf',(bounds[0]-center)/spread)
        if kind=='t': return c.call('STTCRIT','t_sf',bounds[0],spread)
        if kind=='CHI': return c.call('STCHIM','survival',max(0,bounds[0]),spread)
        return 1-a
    b=cdf(kind,bounds[-1],center,spread)
    return b-a if event=='3' else a+1-b

def selected(x,event,bounds):
    if not event or not bounds:return False
    if event=='1':return x<=bounds[0]
    if event=='2':return x>=bounds[0]
    if event=='3':return bounds[0]<=x<=bounds[-1]
    return x<=bounds[0] or x>=bounds[-1]

def show(kind,center,spread,event=None,bounds=(),label=None,probability=None,area_label='AREA'):
    label=label or ('t' if kind=='t' else 'chi-square' if kind=='CHI' else 'x')
    center=float(center);spread=float(spread)
    bounds=tuple(float('-inf') if x=='-INFINITY' else float('inf') if x=='INFINITY' else float(x) for x in bounds)
    finite=tuple(x for x in bounds if abs(x)!=float('inf'))
    if probability is None: probability=area(kind,center,spread,event,bounds)
    standard=kind not in ('t','CHI','UNIFORM','POSITION') and spread>0
    if kind=='UNIFORM': low,high=min(center-.1*(spread-center),min(finite or (center,))),max(spread+.1*(spread-center),max(finite or (spread,)))
    elif kind=='CHI': low,high=0,max(spread+6*math.sqrt(2*spread),max(finite or (0,))*1.15)
    else:
        width=spread if kind not in ('t','POSITION') else (1 if kind=='t' else spread)
        low=min(center-4*width,min(finite or (center,))-width*.5)
        high=max(center+4*width,max(finite or (center,))+width*.5)
    if low==high: low-=1;high+=1
    def density(x):
        if kind=='UNIFORM':return 1 if center<=x<=spread else 0
        if kind=='CHI':
            x=max(x,1e-8);mode=max(spread-2,1e-8)
            return math.exp((spread/2-1)*math.log(x/mode)-(x-mode)/2)
        if kind=='t':return (1+x*x/spread)**(-(spread+1)/2)
        return math.exp(-.5*((x-center)/spread)**2) if spread else 0
    peak=max(density(low+(high-low)*i/240) for i in range(1 if kind=='CHI' and spread<2 else 0,241)) if kind!='POSITION' else 1
    title=('chi-square' if kind=='CHI' else kind)+(' df=%.5g'%spread if kind in ('t','CHI') else ' DISTRIBUTION')
    plt=frame(title,label+' AXIS',(area_label+'=%.7g')%probability if probability is not None else ('SD / SE=%.5g'%spread))
    if plt is None:return False
    at=lambda x:scale(x,low,high)
    line(plt,26,142,306,142)
    if kind!='POSITION' and spread:
        previous=None
        for i in range(241):
            x=low+(high-low)*i/240;y=142-94*min(1,density(x)/peak)
            if selected(x,event,bounds):
                plt.color(*BLUE);line(plt,at(x),142,at(x),y)
            plt.color(*BLACK)
            if previous:line(plt,previous[0],previous[1],at(x),y)
            previous=(at(x),y)
    else:line(plt,at(center),142,at(center),55)
    marks=sorted(set((center,)+finite)) if kind!='UNIFORM' else sorted(set((center,spread)+finite))
    if standard and not finite:marks=[center+i*spread for i in range(-3,4)]
    occupied=[];above=[]
    def mark_label(text,x,y,color,target):
        left=max(1,min(318-(6*len(text)-1),x-3*len(text)));right=left+6*len(text)-1
        if any(not(right+2<a or left>b+2 or y+9<top or y>bottom+2) for a,b,top,bottom in occupied):
            tag(plt,text,x,target,color,above)
        else:
            ink(plt,text,left,y,color);occupied.append((left,right,y,y+7))
    for i,x in enumerate(marks):
        plt.color(*(RED if x in bounds else BLACK));line(plt,at(x),142,at(x),60 if x in bounds else 135)
        mark_label('%.5g'%x,at(x),146+(i%2)*9,RED if x in bounds else BLACK,142)
    if standard or kind=='POSITION':
        plt.color(*BLACK)
        line(plt,26,173,306,173)
        for x in (center,)+tuple(x for x in marks if x!=center):
            if spread:mark_label('z=%.4g'%((x-center)/spread),at(x),165,RED if x in bounds else BLACK,173)
    plt.color(*BLACK)
    if kind=='UNIFORM':plt.text_at(2,'HEIGHT=%.6g'%(1/(spread-center)),'center')
    elif standard:plt.text_at(2,label+' / z ALIGNED; SE=%.5g'%spread,'center')
    elif kind=='POSITION':plt.text_at(2,'POSITION ONLY; NO NORMAL MODEL','center')
    if len(finite)!=len(bounds):plt.text_at(2,'CUTOFF AT '+('-INFINITY' if bounds[0]<0 else 'INFINITY'),'center')
    return wait(plt)
