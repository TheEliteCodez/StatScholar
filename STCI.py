from STTCRIT import _log_gamma, _beta_fraction, _regularized_beta, _t_cdf, t_critical, t_cdf, t_sf, t_interval, t_quantile
from STCINUM import *
from STCINUM import _validate_counts, _validate_mean_data
from STCIIO import _read_number, _read_confidence, _show_result, _show_zstar
from STCIPROP import _one_proportion, _one_proportion_estimate, _two_proportions
from STCIMEAN import _one_mean, _two_means
from STCIMOE import _margin_error, _interval_from_estimate_and_margin
from STZCRIT import _validate_confidence, _normal_quantile, z_critical, standard_normal_quantile
from STSIZE import proportion_sample_size, mean_sample_size, mean_sample_size_estimate
import math
import STCORE as c
def confidence_from_z(critical):
    if critical <= 0:
        raise ValueError('z* MUST BE POSITIVE')
    return 2*c.call('STCLTM','normal_cdf',critical)-1
def t_probability_session(degrees,event):
    return c.call('STTPROB','t_probability_session',degrees,event)
def _read_zstar():
    critical = _read_number('z* (POSITIVE): ')
    if critical <= 0:
        raise ValueError('z* MUST BE POSITIVE')
    return critical
def _check_assumption(title):
    key = c.menu('CHECK: '+title,[
        ('1','YES / GIVEN'),
        ('2','NO'),
        ('3','NOT GIVEN / UNSURE')])
    return {'1':'PASS','2':'FAIL','3':'VERIFY'}[key]
def _read_population_size(title):
    raw = input(title+' N (ENTER=1000000): ').strip()
    size = int(raw) if raw else 1000000
    if size < 1:
        raise ValueError('POPULATION SIZE N MUST BE POSITIVE')
    return size
def panic_one_proportion():
    context = input('SHORT EVENT / POPULATION LABEL (ENTER=SKIP): ').strip()
    successes = c.read_int('NUMBER WITH EVENT (successes x): ')
    n = c.read_int('TOTAL NUMBER SAMPLED (n): ')
    confidence = _read_confidence()
    population_size = _read_population_size('POPULATION SIZE')
    random_check = _check_assumption('RANDOM SAMPLE')
    raw_reference = input('CLAIMED PROPORTION TO CHECK (ENTER=SKIP): ').strip()
    reference = c.number(c.as_ratio(raw_reference)) if raw_reference else None
    result = panic_proportion(successes,n,confidence,population_size,reference)
    estimate_fraction = c.exact_text(c.ratio(successes,n))
    estimate = result['estimate']
    low,high = result['interval']
    margin = result['critical']*result['se']
    context = context or 'the population of interest'
    lines = [
        'INPUT CHECK: x=%d WITH EVENT; n=%d TOTAL' % (successes,n),
        'CONFIDENCE=%.1f%%; POPULATION N=%d' %
        (100*confidence,population_size),
        'P: PARAMETER',
        'p = TRUE PROPORTION OF '+context,
        'SAMPLE: '+str(n)+' OBSERVATIONS; POPULATION: '+context,
        'A: ASSUMPTIONS',
        'RANDOM SAMPLE: '+random_check,
        'SUCCESS: '+str(successes)+' >= 10: '+('PASS' if result['success_ok'] else 'FAIL'),
        'FAILURE: '+str(n-successes)+' >= 10: '+('PASS' if result['failure_ok'] else 'FAIL'),
        'INDEPENDENCE: n/N <= 0.05: '+('PASS' if result['independence_ok'] else 'FAIL'),
        'N: NAME',
        'ONE-PROPORTION z INTERVAL',
        'I: INTERVAL AND POINT ESTIMATE',
        'p-hat = '+estimate_fraction+' = '+('%.4f' % estimate),
        'alpha=%.4f; z*=%.4f' % (1-confidence,result['critical']),
        'MOE=%.4f*sqrt(%.4f*%.4f/%d)=%.4f' %
        (result['critical'],estimate,1-estimate,n,margin),
        '%.1f%% CI = (%.3f, %.3f)' % (confidence*100,low,high),
        'C: CONCLUSION',
        '%.1f%% CONFIDENT p FOR %s IS BETWEEN %.3f AND %.3f.' %
        (confidence*100,context,low,high)]
    if reference is not None:
        lines.extend(['CLAIM '+('%.3f' % reference)+' IS '+
                      ('INSIDE' if result['reference_in_interval'] else 'OUTSIDE')+
                      ' THE INTERVAL.',
                      'CLAIM IS '+('REASONABLE' if result['reference_in_interval'] else 'NOT REASONABLE')+
                      ' AT THIS CONFIDENCE LEVEL.'])
    c.view('PANIC: ONE PROPORTION',lines)
def panic_two_proportions():
    context = input('SHORT GROUP COMPARISON LABEL (ENTER=SKIP): ').strip()
    x1 = c.read_int('GROUP 1 NUMBER WITH EVENT (x1): ')
    n1 = c.read_int('GROUP 1 TOTAL NUMBER SAMPLED (n1): ')
    N1 = _read_population_size('GROUP 1 POPULATION SIZE')
    x2 = c.read_int('GROUP 2 NUMBER WITH EVENT (x2): ')
    n2 = c.read_int('GROUP 2 TOTAL NUMBER SAMPLED (n2): ')
    N2 = _read_population_size('GROUP 2 POPULATION SIZE')
    confidence = _read_confidence()
    random_check = _check_assumption('INDEPENDENT RANDOM SAMPLES')
    estimate,se,critical,interval = two_proportions(x1,n1,x2,n2,confidence)
    p1,p2 = x1/n1,x2/n2
    successes_ok = min(x1,n1-x1,x2,n2-x2) >= 10
    independent_ok = n1 <= .05*N1 and n2 <= .05*N2
    r1,r2 = c.ratio(x1,n1),c.ratio(x2,n2)
    difference = c.radd(r1,(-r2[0],r2[1]))
    low,high = interval
    context = context or 'the group proportions'
    lines = [
        'INPUT CHECK: GROUP 1 %d/%d; GROUP 2 %d/%d' % (x1,n1,x2,n2),
        'CONFIDENCE=%.1f%%; INTERVAL DIRECTION: p1 - p2' %
        (100*confidence),
        'P: p1-p2 = TRUE DIFFERENCE IN PROPORTIONS',
        'GROUP 1 p-hat='+c.exact_text(r1)+'; GROUP 2 p-hat='+c.exact_text(r2),
        'A: INDEPENDENT RANDOM SAMPLES: '+random_check,
        'SUCCESS/FAILURE COUNTS EACH >= 10: '+('PASS' if successes_ok else 'FAIL'),
        'GROUP 1 SUCCESS/FAILURE: %d/%d' % (x1,n1-x1),
        'GROUP 2 SUCCESS/FAILURE: %d/%d' % (x2,n2-x2),
        '5% CONDITION BOTH GROUPS: '+('PASS' if independent_ok else 'FAIL'),
        'N: TWO-PROPORTION z INTERVAL',
        'I: p1-hat-p2-hat='+c.exact_text(difference)+' = %.4f' % estimate,
        'CONFIDENCE=%.1f%%; alpha=%.4f; z*=%.4f' %
        (100*confidence,1-confidence,critical),
        'SE=sqrt(p1hat(1-p1hat)/n1+p2hat(1-p2hat)/n2)=%.4f' % se,
        'MOE=z*SE=%.4f' % (critical*se),
        'CI=(%.3f, %.3f)' % interval,
        'C: %.1f%% CONFIDENT p1-p2 FOR %s IS BETWEEN %.3f AND %.3f.' %
        (100*confidence,context,low,high)]
    if low <= 0 <= high:
        lines.append('ZERO IS IN THE CI: NO CLEAR DIFFERENCE.')
    else:
        lines.append('ZERO IS NOT IN THE CI: EVIDENCE OF A DIFFERENCE.')
    c.view('PANIC: TWO PROPORTIONS',lines)
def _read_mean_group(label):
    source = c.menu(label+' DATA',[
        ('1','SUMMARY (x-bar,s,n)'),
        ('2','RAW MEASUREMENTS')])
    if source == '0':
        return None
    if source == '2':
        values = c.call('STDMATH','read_raw',label+' MEASUREMENTS (SAME UNITS)')
        stats = c.call('STDMATH','descriptive',values)
        if stats['n'] < 2:
            raise ValueError('A t INTERVAL NEEDS AT LEAST TWO VALUES')
        return c.number(stats['MEAN']),stats['SAMPLE SD Sx'],stats['n']
    mean = _read_number(label+' SAMPLE AVERAGE (x-bar): ')
    sd = _read_number(label+' SAMPLE STANDARD DEVIATION (s): ')
    n = c.read_int(label+' TOTAL NUMBER SAMPLED (n): ')
    _validate_mean_data(sd,n)
    return mean,sd,n
def panic_two_means():
    context = input('SHORT GROUP COMPARISON LABEL (ENTER=SKIP): ').strip()
    group1 = _read_mean_group('GROUP 1')
    if group1 is None:
        return
    group2 = _read_mean_group('GROUP 2')
    if group2 is None:
        return
    mean1,sd1,n1 = group1
    mean2,sd2,n2 = group2
    confidence = _read_confidence()
    random_check = _check_assumption('RANDOM SAMPLES')
    independent = _check_assumption('GROUPS ARE INDEPENDENT')
    shape1 = 'PASS' if n1 >= 30 else _check_assumption('GROUP 1 APPROXIMATELY NORMAL / NO STRONG OUTLIERS')
    shape2 = 'PASS' if n2 >= 30 else _check_assumption('GROUP 2 APPROXIMATELY NORMAL / NO STRONG OUTLIERS')
    estimate,se,critical,degrees,interval = two_means(
        mean1,sd1,n1,mean2,sd2,n2,confidence)
    low,high = interval
    context = context or 'the population means'
    lines = [
        'INPUT CHECK: GROUP 1 x-bar=%.4f, s=%.4f, n=%d' %
        (mean1,sd1,n1),
        'GROUP 2 x-bar=%.4f, s=%.4f, n=%d' % (mean2,sd2,n2),
        'CONFIDENCE=%.1f%%; INTERVAL DIRECTION: GROUP 1 - GROUP 2' %
        (100*confidence),
        'P: mu1-mu2 = TRUE DIFFERENCE IN POPULATION MEANS',
        'A: RANDOM SAMPLES: '+random_check+'; INDEPENDENT GROUPS: '+independent,
        'GROUP 1 n=%d; x-bar=%.4f; s=%.4f; SHAPE: %s' %
        (n1,mean1,sd1,shape1),
        'GROUP 2 n=%d; x-bar=%.4f; s=%.4f; SHAPE: %s' %
        (n2,mean2,sd2,shape2),
        'N: TWO-INDEPENDENT-SAMPLE t INTERVAL (WELCH)',
        'I: x-bar1-x-bar2=%.4f; SE=%.4f' % (estimate,se),
        'CONFIDENCE=%.1f%%; alpha=%.4f; df=%.2f; t*=%.4f' %
        (100*confidence,1-confidence,degrees,critical),
        'MOE=t*SE=%.4f' % (critical*se),
        'CI=(%.3f, %.3f)' % interval,
        'C: %.1f%% CONFIDENT mu1-mu2 FOR %s IS BETWEEN %.3f AND %.3f.' %
        (100*confidence,context,low,high)]
    if low <= 0 <= high:
        lines.append('ZERO IS IN THE CI: NO CLEAR DIFFERENCE.')
    else:
        lines.append('ZERO IS NOT IN THE CI: EVIDENCE OF A DIFFERENCE.')
    c.view('PANIC: TWO MEANS',lines)
def panic_one_mean():
    context = input('SHORT MEASURE / UNIT LABEL (ENTER=SKIP): ').strip()
    values = c.call('STDMATH','read_raw','MEASUREMENTS (SAME UNITS)')
    stats = c.call('STDMATH','descriptive',values)
    n = stats['n']
    if n < 2:
        raise ValueError('A ONE-MEAN t INTERVAL NEEDS AT LEAST TWO VALUES')
    mean = c.number(stats['MEAN'])
    sd = stats['SAMPLE SD Sx']
    confidence = _read_confidence()
    estimate,se,critical,interval = one_mean(mean,sd,n,confidence)
    raw_reference = input('REFERENCE MEAN TO CHECK (ENTER=SKIP): ').strip()
    reference = c.number(c.as_ratio(raw_reference)) if raw_reference else None
    raw_margin = input('TARGET MARGIN FOR APPROX SAMPLE SIZE (ENTER=SKIP): ').strip()
    margin = c.number(c.as_ratio(raw_margin)) if raw_margin else None
    random_check = _check_assumption('RANDOM SAMPLE')
    if n < 30:
        shape_check = _check_assumption('POPULATION APPROXIMATELY NORMAL / NO STRONG OUTLIERS')
    else:
        shape_check = 'LARGE SAMPLE n >= 30; CHECK EXTREME OUTLIERS'
    context = context or 'the population of interest'
    q1,median,q3 = stats['Q1'],stats['MEDIAN'],stats['Q3']
    lines = [
        'INPUT CHECK: n=%d; x-bar=%.4f; s=%.4f' % (n,mean,sd),
        'CONFIDENCE=%.1f%%' % (100*confidence),
        'P: mu = TRUE MEAN '+context,
        'A: SAMPLE SIZE n='+str(n)+'; S SAMPLE SD='+('%.4f' % sd),
        'RANDOM SAMPLE: '+random_check+'; OBSERVATIONS INDEPENDENT',
        'SHAPE / OUTLIER CONDITION: '+shape_check,
        'N: ONE-SAMPLE STUDENT t INTERVAL; df='+str(n-1),
        'CONFIDENCE=%.1f%%; alpha=%.4f' % (100*confidence,1-confidence),
        'I: x-bar='+('%.4f' % mean)+'; SE='+('%.4f' % se),
        't*='+('%.4f' % critical)+'; MOE=t*s/sqrt(n)=%.4f' % (critical*se),
        'MOE=%.4f*%.4f/sqrt(%d)=%.4f' % (critical,sd,n,critical*se),
        'TAIL AREAS=%.3f EACH; t=+/-%.4f' % ((1-confidence)/2,critical),
        'CI=(%.3f, %.3f)' % interval,
        'INEQUALITY: %.3f < mu < %.3f' % interval,
        'C: %.1f%% CONFIDENT THE MEAN %s IS IN THIS INTERVAL.' %
        (100*confidence,context),
        'FIVE-NUMBER SUMMARY: '+','.join('%.2f' % c.number(v)
                                          for v in (stats['MIN'],q1,median,q3,stats['MAX'])),
        'SORTED DATA: '+','.join(c.exact_text(v) for v in values),
        'OUTLIERS: '+str(stats['OUTLIERS']),
        'ASSESS WHETHER THE DATA ARE APPROXIMATELY NORMAL.']
    if reference is not None:
        inside = interval[0] <= reference <= interval[1]
        lines.extend(['REFERENCE MEAN '+('%.3f' % reference)+' IS '+
                      ('INSIDE' if inside else 'OUTSIDE')+' THE CI.',
                      ('NO EVIDENCE OF A DIFFERENCE FROM ' if inside else 'EVIDENCE OF A DIFFERENCE FROM ')+
                      'THE REFERENCE MEAN AT '+('%.1f' % (100*confidence))+'%.'])
    if margin is not None:
        raw_n = mean_sample_size_estimate(sd,margin,confidence)
        z_planning = z_critical(confidence)
        achieved = z_planning*sd/math.sqrt(int(math.ceil(raw_n)))
        lines.extend(['APPROX n USING s AS sigma: (z* s/E)^2',
                      'z*=%.4f; SUBSTITUTE: (z* %.4f / %.4f)^2' %
                      (z_planning,sd,margin),
                      'RAW n='+('%.3f' % raw_n)+'; ROUND UP TO '+str(int(math.ceil(raw_n))),
                      'AT n='+str(int(math.ceil(raw_n)))+', APPROX E=%.3f (< %.3f)' %
                      (achieved,margin)])
    c.view('PANIC: ONE MEAN',lines)
def compare_mean_ci_with_without_value():
    context=input('MEASURE / UNIT LABEL: ').strip() or 'the population mean'
    values=c.call('STDMATH','read_raw','SAMPLE MEASUREMENTS (SAME UNITS)')
    if len(values)<3:
        raise ValueError('COMPARISON NEEDS AT LEAST THREE MEASUREMENTS')
    confidence=_read_confidence()
    omitted=c.read_exact('VERIFIED OUTLIER VALUE TO OMIT: ')
    index=None
    for i,value in enumerate(values):
        if c.compare_exact(value,omitted)==0:
            index=i
            break
    if index is None:
        raise ValueError('VALUE TO OMIT MUST MATCH A RECORDED MEASUREMENT')
    reduced=values[:index]+values[index+1:]
    if len(reduced)<2:
        raise ValueError('AT LEAST TWO MEASUREMENTS MUST REMAIN')
    original_stats=c.call('STDMATH','descriptive',values)
    reduced_stats=c.call('STDMATH','descriptive',reduced)
    mean1=c.number(original_stats['MEAN'])
    mean2=c.number(reduced_stats['MEAN'])
    sd1=original_stats['SAMPLE SD Sx']
    sd2=reduced_stats['SAMPLE SD Sx']
    _,se1,t1,interval1=one_mean(mean1,sd1,len(values),confidence)
    _,se2,t2,interval2=one_mean(mean2,sd2,len(reduced),confidence)
    c.view('MEAN CI > WITH / WITHOUT VALUE',[
        'CONTEXT: '+context,
        'CONFIDENCE=%.1f%%' % (100*confidence),
        'WITH ALL DATA: n=%d; x-bar=%.4f; s=%.4f' %
        (len(values),mean1,sd1),
        't*=%.4f; SE=%.4f; MOE=%.4f' % (t1,se1,t1*se1),
        'CI=(%.4f, %.4f)' % interval1,
        'OMITTED ONE RECORDED VALUE: '+c.exact_text(omitted),
        'WITHOUT THAT VALUE: n=%d; x-bar=%.4f; s=%.4f' %
        (len(reduced),mean2,sd2),
        't*=%.4f; SE=%.4f; MOE=%.4f' % (t2,se2,t2*se2),
        'CI=(%.4f, %.4f)' % interval2,
        'VERIFY THE VALUE IS A REAL OUTLIER; DO NOT REMOVE DATA ONLY TO CHANGE THE RESULT.'])
def choose_confidence_method():
    task = c.menu('WHAT DOES THE PROBLEM ASK?',[
        ('1','FIND A CONFIDENCE INTERVAL'),
        ('2','INTERPRET A GIVEN INTERVAL'),
        ('3','FIND MARGIN OF ERROR'),
        ('4','FIND REQUIRED SAMPLE SIZE')])
    if task == '0':
        return
    if task == '2':
        _interpret_given_interval()
        return
    if task == '3':
        _margin_error()
        return
    if task == '4':
        _required_sample_size()
        return
    data_type = c.menu('WHAT TYPE OF RESPONSE?',[
        ('1','YES/NO OR CATEGORY: PROPORTION'),
        ('2','NUMERICAL MEASUREMENT: MEAN')])
    if data_type == '0':
        return
    samples = c.menu('HOW MANY SAMPLES / GROUPS?',[
        ('1','ONE SAMPLE / GROUP'),
        ('2','TWO INDEPENDENT GROUPS (NOT PAIRED)')])
    if samples == '0':
        return
    if data_type == '1':
        if samples == '1':
            panic_one_proportion()
        else:
            panic_two_proportions()
    elif samples == '1':
        panic_one_mean()
    else:
        panic_two_means()
def _interpret_given_interval():
    parameter_type = c.menu('WHAT PARAMETER IS THE INTERVAL ABOUT?',[
        ('1','ONE PROPORTION p'),
        ('2','ONE MEAN mu'),
        ('3','DIFFERENCE BETWEEN TWO GROUPS')])
    if parameter_type == '0':
        return
    context = input('POPULATION / PARAMETER IN CONTEXT: ').strip()
    low = _read_number('LOWER ENDPOINT: ')
    high = _read_number('UPPER ENDPOINT: ')
    if low >= high:
        raise ValueError('LOWER ENDPOINT MUST BE LESS THAN UPPER ENDPOINT')
    confidence = _read_confidence()
    labels = {'1':'p','2':'mu','3':'GROUP 1 - GROUP 2 PARAMETER'}
    parameter = labels[parameter_type]
    middle = (low+high)/2
    margin = (high-low)/2
    context = context or 'the population parameter'
    c.view('INTERPRET GIVEN INTERVAL',[
        'PARAMETER: '+parameter+' = '+context,
        'GIVEN CI=(%.4f, %.4f)' % (low,high),
        'POINT ESTIMATE / CENTER=%.4f' % middle,
        'MARGIN OF ERROR=%.4f' % margin,
        'CONFIDENCE=%.1f%%' % (100*confidence),
        'INTERPRETATION: %.1f%% CONFIDENT THE %s IS BETWEEN %.4f AND %.4f.' %
        (100*confidence,context,low,high)])
def _zstar_from_confidence():
    confidence = _read_confidence()
    critical = z_critical(confidence)
    _show_zstar('z* FROM CONFIDENCE',confidence,critical,[])
def _confidence_from_zstar():
    critical = _read_zstar()
    confidence = confidence_from_z(critical)
    c.view('CONFIDENCE FROM z*',[
        'z*='+('%.4f' % critical),
        'CONFIDENCE='+('%.2f' % (100*confidence))+'%'])
def _required_sample_size():
    return c.call('STSIZE','_required_sample_size')
def zstar_menu():
    actions = {'1':_zstar_from_confidence,
               '2':_confidence_from_zstar,
               '3':_margin_error,
               '4':_required_sample_size}
    while True:
        key = c.menu('z* / MARGIN OF ERROR',[
            ('1','FIND z* FROM CONFIDENCE'),
            ('2','FIND CONFIDENCE FROM z*'),
            ('3','CALCULATE MARGIN OF ERROR'),
            ('4','FIND REQUIRED SAMPLE SIZE'),
            ('5','FIND z* FROM UPPER-TAIL AREA')])
        if key == '0':
            return
        if key in actions:
            actions[key]()
        elif key == '5':
            tail=_read_number('UPPER-TAIL AREA alpha (E.G. 0.005): ')
            if not 0 < tail < 1:
                raise ValueError('UPPER-TAIL AREA alpha MUST BE BETWEEN 0 AND 1')
            critical=standard_normal_quantile(1-tail)
            c.view('z* FROM UPPER-TAIL AREA',[
                'UPPER-TAIL AREA alpha=%.6f' % tail,
                'z*=%.6f' % critical])
def confidence_menu():
    procedures = {'1':_one_proportion,'2':_two_proportions,'3':_one_mean,'4':_two_means}
    while True:
        key = c.menu('CH 7/8 CONFIDENCE INTERVALS',[
            ('1','ONE PROPORTION (x,n)'),
            ('2','TWO PROPORTIONS (x,n EACH)'),
            ('3','ONE MEAN (x-bar,s,n)'),
            ('4','TWO MEANS (x-bar,s,n EACH)'),
            ('5','z* / MOE / SAMPLE SIZE'),
            ('6','ONE-PROP CI: FULL WORKSHEET'),
            ('7','ONE-MEAN CI: RAW + FULL WORK'),
            ('8','GUIDED: WHAT IS ASKED?'),
            ('9','STUDENT t PROBABILITY / PERCENTILE'),
            ('10','ONE-PROPORTION CI (GIVEN p-hat)'),
            ('11','INTERVAL FROM ESTIMATE +/- E'),
            ('12','INTERPRET GIVEN INTERVAL'),
            ('13','MEAN CI WITH / WITHOUT OUTLIER')])
        if key == '0':
            return
        if key == '5':
            zstar_menu()
        elif key == '6':
            panic_one_proportion()
        elif key == '7':
            panic_one_mean()
        elif key == '8':
            choose_confidence_method()
        elif key == '9':
            c.call('STDIST','t_menu')
        elif key == '10':
            _one_proportion_estimate()
        elif key == '11':
            _interval_from_estimate_and_margin()
        elif key == '12':
            _interpret_given_interval()
        elif key == '13':
            compare_mean_ci_with_without_value()
        else:
            procedures[key]()
