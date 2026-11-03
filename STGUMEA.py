import math
import STCORE as c
from STGPEN import frame,line,ink,scale,wait,BLACK,BLUE,RED

def density(x,a,b,n):
    if not a<=x<=b:return 0
    if n==1:return 1/(b-a)
    t=n*(x-a)/(b-a);total=0;choose=1;factorial=1
    for j in range(1,n):factorial*=j
    for k in range(min(n,int(t))+1):
        total+=(-1)**k*choose*max(0,t-k)**(n-1)
        choose=choose*(n-k)//(k+1)
    return max(0,n*total/((b-a)*factorial))

def show(a,b,n,event,probability):
    plt=frame('EXACT UNIFORM SAMPLE MEAN','x-bar','P=%.7g'%probability)
    if plt is None:return False
    peak=density((a+b)/2,a,b,n) or 1;previous=None
    op=event[0];low=c.number(event[1]);high=c.number(event[2])
    line(plt,26,160,306,160)
    for i in range(241):
        x=a+(b-a)*i/240;y=160-110*density(x,a,b,n)/peak;at=scale(x,a,b)
        included=(x<low) if op=='<' else (x>low) if op=='>' else (low<=x<=high)
        if included:plt.color(*BLUE);line(plt,at,160,at,y)
        plt.color(*BLACK)
        if previous:line(plt,previous[0],previous[1],at,y)
        previous=(at,y)
    for x in (a,(a+b)/2,b):ink(plt,'%.5g'%x,scale(x,a,b)-10,166,BLACK)
    for exact in (event[1],event[2]) if event[0]=='[]' else (event[1],):
        x=c.number(exact)
        if a<=x<=b:plt.color(*RED);line(plt,scale(x,a,b),160,scale(x,a,b),45);ink(plt,'%.5g'%x,scale(x,a,b)-10,148,RED)
    return wait(plt)
