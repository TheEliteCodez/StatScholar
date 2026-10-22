import math
import STCORE as c
from STZCRIT import _validate_confidence, z_critical
def proportion_margin_error(successes,n,confidence):
    _validate_counts(successes,n)
    estimate = successes/n
    critical = z_critical(confidence)
    se = math.sqrt(estimate*(1-estimate)/n)
    return estimate,se,critical,critical*se
def mean_margin_error(sigma,n,confidence):
    if sigma < 0 or n < 1:
        raise ValueError('POPULATION SD MUST BE NONNEGATIVE AND n MUST BE POSITIVE')
    critical = z_critical(confidence)
    se = sigma/math.sqrt(n)
    return se,critical,critical*se
def one_proportion(successes, n, confidence):
    _validate_counts(successes,n)
    p_hat = successes/n
    critical = z_critical(confidence)
    se = math.sqrt(p_hat*(1-p_hat)/n)
    return p_hat, se, critical, (p_hat-critical*se,p_hat+critical*se)
def one_proportion_estimate(p_hat,n,confidence):
    _validate_confidence(confidence)
    if not 0 <= p_hat <= 1 or n < 1:
        raise ValueError('USE 0 <= p-hat <= 1 AND POSITIVE SAMPLE SIZE')
    critical=z_critical(confidence)
    se=math.sqrt(p_hat*(1-p_hat)/n)
    return p_hat,se,critical,(p_hat-critical*se,p_hat+critical*se)
def proportion_margin_error_estimate(p_hat,n,confidence):
    estimate,se,critical,interval=one_proportion_estimate(p_hat,n,confidence)
    return estimate,se,critical,critical*se
def panic_proportion(successes, n, confidence, population_size=1000000, reference=None):
    _validate_counts(successes,n)
    _validate_confidence(confidence)
    if population_size < 1:
        raise ValueError('POPULATION SIZE N MUST BE POSITIVE')
    if reference is not None and not 0 <= reference <= 1:
        raise ValueError('CLAIMED PROPORTION MUST BE BETWEEN 0 AND 1')
    estimate,se,critical,interval = one_proportion(successes,n,confidence)
    return {
        'estimate':estimate,
        'se':se,
        'critical':critical,
        'interval':interval,
        'successes':successes,
        'failures':n-successes,
        'sample_size':n,
        'population_size':population_size,
        'success_ok':successes >= 10,
        'failure_ok':n-successes >= 10,
        'independence_ok':n <= 0.05*population_size,
        'reference':reference,
        'reference_in_interval':reference is not None and
            interval[0] <= reference <= interval[1]
    }
def two_proportions(x1,n1,x2,n2,confidence):
    _validate_counts(x1,n1)
    _validate_counts(x2,n2)
    p1, p2 = x1/n1, x2/n2
    se = math.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2)
    critical = z_critical(confidence)
    difference = p1-p2
    return difference, se, critical, (difference-critical*se,difference+critical*se)
def one_mean(mean, sd, n, confidence):
    _validate_mean_data(sd,n)
    critical = c.call('STTCRIT','t_critical',confidence,n-1)
    se = sd/math.sqrt(n)
    return mean, se, critical, (mean-critical*se,mean+critical*se)
def two_means(mean1,sd1,n1,mean2,sd2,n2,confidence):
    _validate_mean_data(sd1,n1)
    _validate_mean_data(sd2,n2)
    se1, se2 = sd1*sd1/n1, sd2*sd2/n2
    se = math.sqrt(se1+se2)
    degrees = (se1+se2)*(se1+se2)/(se1*se1/(n1-1)+se2*se2/(n2-1))
    critical = c.call('STTCRIT','t_critical',confidence,degrees)
    difference = mean1-mean2
    return difference, se, critical, degrees, (difference-critical*se,difference+critical*se)
def _validate_counts(successes,n):
    if n < 1 or successes < 0 or successes > n:
        raise ValueError('USE 0 <= SUCCESS COUNT <= SAMPLE SIZE')
def _validate_mean_data(sd,n):
    if sd < 0 or n < 2:
        raise ValueError('SD MUST BE NONNEGATIVE AND n MUST BE AT LEAST 2')
