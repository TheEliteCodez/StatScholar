# Multiple observations with one mean/SD; loaded only for this report.
import STCORE as c


def z_list(mean,sd,variance,inclusive=False):
    import STNORM as normal
    values=[c.read_exact('OBSERVATION x: ') for i in range(c.read_size('HOW MANY OBSERVATIONS: ',c.MAX_ROWS))]
    while True:
        key=c.menu('SAVED OBSERVATIONS',[('1','Z / LOW-HIGH REPORT'),('2','x AND z AXES / MARK VALUES')])
        if key=='0': return
        if key=='1':
            c.results('USUAL LIMITS',[('MIN USUAL',normal.x_value((-2,1),mean,sd)),('MAX USUAL',normal.x_value((2,1),mean,sd))],['BOUNDARIES UNUSUAL' if inclusive else 'BOUNDARIES USUAL'])
            c.paged_results('OBSERVATION REPORT',len(values),lambda i:('x='+c.exact_text(values[i]),'z='+c.fixed(normal.z_value(values[i],mean,sd),4)+' '+normal.usual_classification(values[i],mean,variance,inclusive)),['CLASSIFY BEFORE ROUNDING z'])
        else:
            normal.show_axes('ALIGNED AXES (* = OBSERVATION)',mean,sd,values)
            c.results('LABEL AXES',[('z='+str(z)+' x',normal.x_value((z,1),mean,sd)) for z in range(-3,4)],['CENTER MODEL BELL AT z=0','MARK OBSERVATIONS BELOW AT THEIR z'])
            c.paged_results('MARK OBSERVATIONS',len(values),lambda i:('x='+c.exact_text(values[i])+' AT z',normal.z_value(values[i],mean,sd)))
