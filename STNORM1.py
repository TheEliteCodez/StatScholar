import STCORE as c
def axis_lines(mean,sd,start,observations=()):
    def labels(values):
        line=''
        for value in values:
            gap=10-len(value)
            line+=' '*(gap//2)+value+' '*(gap-gap//2)
        return line.rstrip()
    ticks=range(start,start+3)
    values=[c.fixed(c.call('STNORM','x_value',(z,1),mean,sd),4).rstrip('0').rstrip('.') for z in ticks]
    keys=[]
    for i,value in enumerate(values):
        if len(value)>9:
            name=chr(65+i)
            keys.append(name+'='+value)
            values[i]=name
    marks=[' ']*30
    for x in observations:
        z=c.call('STNORM','z_value',x,mean,sd)
        offset=c.rdiv(c.call('STNORM','sub',z,(start,1)),(2,1))
        if c.compare_exact(offset,0)>=0 and c.compare_exact(offset,1)<=0:
            marks[4+int(round(20*offset[0]/offset[1]))]='*'
    axis='    |---------|---------|'
    lines=['z: '+str(start)+' TO '+str(start+2),labels([str(z) for z in ticks]),axis,axis,labels(values),'x: SAME TICKS AS z']
    if observations: lines.insert(0,''.join(marks).rstrip() or 'NO OBSERVATION IN THIS PANEL')
    return lines+keys
def show_axes(title,mean,sd,observations=()):
    if not sd[0]:
        c.view(title,['SD=0: z AXIS UNDEFINED','ALL MODEL VALUES EQUAL MEAN']);return
    lines=[]
    for start in (-3,-1,1):
        panel=axis_lines(mean,sd,start,observations)
        lines+=panel+['']*((-len(panel))%c.VIEW_LINES)
    c.view(title,lines)
def observation_report(x,mean,sd,variance=None,inclusive=False):
    variance=c.rmul(sd,sd) if variance is None else variance
    position=c.call('STNORM','usual_classification',x,mean,variance,inclusive)
    c.results('VALUE / Z / USUAL', [('x',x),('z',c.call('STNORM','z_value',x,mean,sd)),
        ('MIN USUAL',c.call('STNORM','x_value',(-2,1),mean,sd)),('MAX USUAL',c.call('STNORM','x_value',(2,1),mean,sd)),
        ('UNUSUAL','NO' if position=='NOT UNUSUAL' else 'YES'),('CLASSIFICATION',position)],
        ['z=(x-MEAN)/SD','BOUNDARIES UNUSUAL' if inclusive else 'BOUNDARIES USUAL','NORMAL MENU 7 CHANGES < / <='],drawing=c.call('STSKETCH','position',mean,sd,x))
