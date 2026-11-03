import math

def _validate_confidence(confidence):
    if not 0 < confidence < 1:
        raise ValueError('CONFIDENCE LEVEL MUST BE BETWEEN 0 AND 1')

def _normal_quantile(p):
    if not 0 < p < 1:
        raise ValueError('PROBABILITY MUST BE BETWEEN 0 AND 1')
    a = (-39.6968302866538, 220.946098424521, -275.928510446969,
         138.357751867269, -30.6647980661472, 2.50662827745924)
    b = (-54.4760987982241, 161.585836858041, -155.698979859887,
         66.8013118877197, -13.2806815528857)
    cc = (-0.00778489400243029, -0.322396458041136, -2.40075827716184,
          -2.54973253934373, 4.37466414146497, 2.93816398269878)
    d = (0.00778469570904146, 0.32246712907004, 2.445134137143,
         3.75440866190742)
    if p < 0.02425:
        q = math.sqrt(-2 * math.log(p))
        return (((((cc[0]*q+cc[1])*q+cc[2])*q+cc[3])*q+cc[4])*q+cc[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > 1 - 0.02425:
        q = math.sqrt(-2 * math.log(1-p))
        return -(((((cc[0]*q+cc[1])*q+cc[2])*q+cc[3])*q+cc[4])*q+cc[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

def z_critical(confidence):
    _validate_confidence(confidence)
    return _normal_quantile((1 + confidence) / 2)

def standard_normal_quantile(probability):
    return _normal_quantile(probability)
