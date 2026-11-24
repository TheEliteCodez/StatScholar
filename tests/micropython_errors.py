"""Native MicroPython fixture for the error identifier; no physical TI proof."""
import builtins
import gc
import STCORE as c

c.wait_key=lambda:'right'
original=builtins.__import__
def guard(name,*args,**kwargs):
  if name in ('STDEFS','STTCRIT','STZCRIT','STHYME','STHYPR','STHTPLOT'):
    raise AssertionError('Unneeded import: '+name)
  return original(name,*args,**kwargs)
builtins.__import__=guard
heap=gc.mem_free()+gc.mem_alloc()
cases=[
 ['15','9','1','1','adults who smoke','2','40%','1','1','1','0','0','0'],
 ['15','9','2','2','battery life','1','150','3','1','0','0','0','0'],
 ['15','9','3','2','2','0','0','0'],
 ['15','9','3','1','2','0','0','0'],
 ['15','9','3','2','1','0','0','0'],
 ['15','9','3','1','3','0','0','0'],
 ['15','9','3','2','3','0','0','0'],
 ['15','9','4','0','0','0']]
for repeat in range(3):
  for answers in cases:
    pending=iter(answers);builtins.input=lambda prompt='':next(pending)
    if 'STAT1' in globals():STAT1.main()
    else:
      c.ON_TI=True
      import STAT1
    assert list(pending)==[]
    assert not c.topic_modules() and not c._call_depth
    gc.collect()
    assert gc.mem_free()+gc.mem_alloc()==heap
print('ERROR_NATIVE_PASS',24,heap)
