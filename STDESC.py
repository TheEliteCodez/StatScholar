import STCORE
def solver_rel_freq():
    return STCORE.call('STDESC1', 'solver_rel_freq')
def solver_range_iqr():
    return STCORE.call('STDESC1', 'solver_range_iqr')
def solver_usual():
    return STCORE.call('STDESC1', 'solver_usual')
def solver_zscore():
    return STCORE.call('STDESC1', 'solver_zscore')
def solver_outlier():
    return STCORE.call('STDESC1', 'solver_outlier')
def frequency_stats(rows):
    return STCORE.call('STDESC2', 'frequency_stats', rows)
def frequency_session(rows=None):
    return STCORE.call('STDESC2', 'frequency_session', rows)
