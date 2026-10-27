import STCORE as c
from STCIIO import _read_number, _read_confidence, _show_result
from STCINUM import one_proportion, one_proportion_estimate, two_proportions
def _one_proportion():
    x = c.read_int('NUMBER WITH EVENT (successes x): ')
    n = c.read_int('TOTAL NUMBER SAMPLED (n): ')
    confidence = _read_confidence()
    estimate,se,critical,interval = one_proportion(x,n,confidence)
    warning = 'CHECK NORMAL APPROXIMATION: n*p-hat AND n*(1-p-hat) >= 10.' if min(estimate*n,(1-estimate)*n) < 10 else None
    _show_result('ONE-PROPORTION z INTERVAL',estimate,se,critical,interval,confidence,
                 warning=warning,estimate_label='p-hat',
                 parameter='POPULATION PROPORTION p',critical_label='z*',
                 input_summary=['INPUT CHECK: x=%d WITH EVENT; n=%d TOTAL' % (x,n)],
                 work=['p-hat=x/n=%d/%d=%.10g' % (x,n,estimate)]+c.call('STWORK','prop_se',estimate,n,se))
def _one_proportion_estimate():
    context=input('EVENT / GROUP LABEL (ENTER=SKIP): ').strip()
    estimate=_read_number('SAMPLE PROPORTION p-hat (DECIMAL OR PERCENT): ')
    n=c.read_int('TOTAL NUMBER SAMPLED (n): ')
    confidence=_read_confidence()
    estimate,se,critical,interval=one_proportion_estimate(estimate,n,confidence)
    success=estimate*n
    failure=(1-estimate)*n
    warning=('CHECK NORMAL APPROXIMATION: n*p-hat AND n*(1-p-hat) >= 10.'
             if min(success,failure)<10 else None)
    _show_result('ONE-PROPORTION z INTERVAL FROM p-hat',estimate,se,critical,
                 interval,confidence,warning=warning,estimate_label='p-hat',
                 parameter='POPULATION PROPORTION p',critical_label='z*',
                 input_summary=[
                     'INPUT CHECK: p-hat=%.4f; n=%d TOTAL' % (estimate,n),
                     'CONTEXT: '+(context or 'population proportion')],
                 work=c.call('STWORK','prop_se',estimate,n,se))
def _two_proportions():
    x1 = c.read_int('GROUP 1 NUMBER WITH EVENT (x1): ')
    n1 = c.read_int('GROUP 1 TOTAL SAMPLED (n1): ')
    x2 = c.read_int('GROUP 2 NUMBER WITH EVENT (x2): ')
    n2 = c.read_int('GROUP 2 TOTAL SAMPLED (n2): ')
    confidence = _read_confidence()
    estimate,se,critical,interval = two_proportions(x1,n1,x2,n2,confidence)
    warning = 'CHECK SUCCESS/FAILURE COUNTS >= 10 IN BOTH GROUPS.' if min(x1,n1-x1,x2,n2-x2) < 10 else None
    _show_result('TWO-PROPORTION z INTERVAL',estimate,se,critical,interval,confidence,
                 warning=warning,estimate_label='p1-hat - p2-hat',
                 parameter='GROUP 1 - GROUP 2 PROPORTION DIFFERENCE',critical_label='z*',
                 input_summary=['INPUT CHECK: GROUP 1 %d/%d; GROUP 2 %d/%d' %
                                (x1,n1,x2,n2),'INTERVAL DIRECTION: p1 - p2'],
                 work=['PE=x1/n1-x2/n2=%d/%d-%d/%d=%.10g' % (x1,n1,x2,n2,estimate)]+
                      c.call('STWORK','prop_two',x1/n1,n1,x2/n2,n2,se))
