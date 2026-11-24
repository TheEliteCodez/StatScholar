import STCORE as c
from STEXACT import read_exact, compare_exact, to_ratio
from STEFMT import exact_sorted
RAW_LIMIT = 100
def sub(a, b):
  return c.radd(a, (-b[0], b[1]))
def read_raw(title='DATA > RAW'):
  c.heading(title)
  while True:
    raw=input('NUMBER OF VALUES (1..100) OR L1: ').strip().upper()
    if raw in ('L1','L2','L3','L4','L5','L6'):
      return read_os_list(raw[1])
    try: n=int(raw)
    except ValueError:
      print('ENTER A COUNT OR L1-L6'); continue
    if 1<=n<=RAW_LIMIT: break
    print('USE 1..100 VALUES')
  values = [read_exact('VALUE '+str(i+1)+': ') for i in range(n)]
  for i in range(1, n):
    x, j = values[i], i
    while j and compare_exact(values[j-1], x) > 0:
      values[j] = values[j-1]
      j -= 1
    values[j] = x
  return values

def read_os_list(number='1'):
  try:
    from ti_system import recall_list
  except ImportError:
    raise ValueError('TI LIST IMPORT REQUIRES ti_system.recall_list')
  values=recall_list(number)
  if values is None or not 1<=len(values)<=RAW_LIMIT:
    raise ValueError('L'+number+' MUST CONTAIN 1..100 VALUES')
  return exact_sorted(to_ratio(x) for x in values)
def median_span(values, start, end):
  length = end-start
  if not length: return None
  mid = start+length//2
  return values[mid] if length%2 else c.rdiv(c.radd(values[mid-1], values[mid]), (2,1))
def quartiles(values):
  n = len(values)
  return (median_span(values, 0, n//2), median_span(values, 0, n),
      median_span(values, (n+1)//2, n))
def descriptive(values):
  return c.call('STDMATH2', 'weighted_stats', ((x,1) for x in values))
def value_counts(values):
  counts={}
  for x in values: counts[x]=counts.get(x,0)+1
  return [(x,counts[x]) for x in exact_sorted(counts)]
def min_exact(a,b): return a if compare_exact(a,b)<=0 else b
def max_exact(a,b): return a if compare_exact(a,b)>=0 else b
def edit_raw(values):
  c.paged_results('SORTED VALUES / EDIT INDEX',len(values),lambda i:(str(i+1),values[i]))
  index=c.read_size('SORTED INDEX TO CHANGE: ',len(values))-1
  values[index]=read_exact('NEW VALUE: ')
  return exact_sorted(values)
def edit_frequency(rows):
  c.paged_results('FREQUENCY ROWS',len(rows),lambda i:(str(i+1),c.exact_text(rows[i][0])+' COUNT='+str(rows[i][1])))
  index=c.read_size('ROW TO CHANGE: ',len(rows))-1
  x=read_exact('VALUE: ');f=c.read_int('FREQUENCY: ')
  if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
  rows[index]=(x,f)
  return rows
def read_frequency_rows():
  print('EXACT VALUES, NOT CLASS LIMITS')
  rows=[]
  for i in range(c.read_size('NUMBER OF ROWS: ',c.MAX_ROWS)):
    x=read_exact('VALUE: '); f=c.read_int('FREQUENCY: ')
    if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
    rows.append((x,f))
  return rows
def probe_summary(size):
  values=[(i,1) for i in range(size)]
  stats=c.call('STDMATH1','descriptive',values)
  print('RAW '+str(size)+' MEAN='+c.exact_text(stats['MEAN']))
  return stats['MEAN']
