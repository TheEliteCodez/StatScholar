from STEXACT import ratio, compare_exact
from STEFMT import radd, rmul, range_relation, fixed, exact_text
def to_ratio(value):
    return (value,1) if isinstance(value,int) else value
from STCORE import number
