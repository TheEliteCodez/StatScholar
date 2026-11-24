import STCORE as c
from STCIIO import _read_number, _read_confidence, _show_result
from STCINUM import one_mean, two_means
def _one_mean(stats=None):
  source = '2' if stats is not None else c.menu('ONE-MEAN INPUT',[('1','SUMMARY (x-bar,s,n)'),('2','RAW MEASUREMENTS')])
  if source == '0':
    return
  if source == '2':
    if stats is None:
      mean,sd,n=c.call('STMEAN','read_raw','MEASUREMENTS (SAME UNITS)')
    else:
      if stats['n']<2: raise ValueError('NEED TWO VALUES FOR A SAMPLE MEAN INTERVAL')
      mean = c.number(stats['MEAN'])
      sd = stats['SAMPLE SD Sx']
      n = stats['n']
  else:
    mean = _read_number('SAMPLE AVERAGE (x-bar): ')
    sd = _read_number('SAMPLE STANDARD DEVIATION (s): ')
    n = c.read_int('TOTAL NUMBER SAMPLED (n): ')
  confidence = _read_confidence()
  estimate,se,critical,interval = one_mean(mean,sd,n,confidence)
  warning = 'CHECK RANDOM SAMPLE, OUTLIERS, AND NORMAL/NEAR-NORMAL SHAPE.'
  _show_result('ONE-MEAN t INTERVAL',estimate,se,critical,interval,confidence,df=n-1,
        warning=warning,estimate_label='x-bar',
        parameter='POPULATION MEAN mu',critical_label='t*',
        input_summary=['INPUT CHECK: x-bar=%.4f; s=%.4f; n=%d' %
                (mean,sd,n)],work=c.call('STWORK','mean_se',sd,n,se))
  raw_reference=input('REFERENCE POPULATION MEAN (ENTER=SKIP): ').strip()
  if raw_reference:
    reference=c.number(c.as_ratio(raw_reference))
    inside=interval[0] <= reference <= interval[1]
    c.view('ONE-MEAN CLAIM CHECK',[
      'REFERENCE MEAN=%.4f' % reference,
      'REFERENCE IS '+('INSIDE' if inside else 'OUTSIDE')+' THE CI.',
      'CLAIM IS '+('REASONABLE' if inside else 'NOT REASONABLE')+
      ' AT THIS CONFIDENCE LEVEL.',
      'INTERVAL INCLUSION DOES NOT PROVE THE CLAIM TRUE.'])
def _two_means():
  first=c.call('STHYIO','mean_data','GROUP 1')
  if first is None: return
  second=c.call('STHYIO','mean_data','GROUP 2')
  if second is None: return
  mean1,sd1,n1=first
  mean2,sd2,n2=second
  confidence = _read_confidence()
  estimate,se,critical,degrees,interval = two_means(mean1,sd1,n1,mean2,sd2,n2,confidence)
  _show_result('TWO-MEAN t INTERVAL',estimate,se,critical,interval,confidence,df=degrees,
        summary_inputs=['xbar1=%.6g' % mean1,'s1=%.6g' % sd1,'n1=%d' % n1,
                'xbar2=%.6g' % mean2,'s2=%.6g' % sd2,'n2=%d' % n2],
        warning='CHECK INDEPENDENT GROUPS, RANDOMNESS, AND EACH GROUP SHAPE.',
        estimate_label='x-bar1 - x-bar2',
        parameter='GROUP 1 - GROUP 2 MEAN DIFFERENCE',critical_label='t*',
        input_summary=['INPUT CHECK: GROUP 1 x-bar=%.4f, s=%.4f, n=%d' %
                (mean1,sd1,n1),
                'GROUP 2 x-bar=%.4f, s=%.4f, n=%d' %
                (mean2,sd2,n2),
                'INTERVAL DIRECTION: GROUP 1 - GROUP 2'],
        work=['PE=x-bar1-x-bar2=%.10g-%.10g=%.10g' % (mean1,mean2,estimate)]+
           c.call('STWORK','mean_two',sd1,n1,sd2,n2,se,degrees))
