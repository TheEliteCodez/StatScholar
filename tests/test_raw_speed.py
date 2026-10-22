import subprocess
import sys
import unittest


class RawCalculationSpeed(unittest.TestCase):
    def test_collection_count_does_not_grow_per_observation(self):
        code='''
import gc
from fractions import Fraction
import STCORE as c
original=gc.collect
collections=[0]
def collect():
    collections[0]+=1
    return original()
gc.collect=collect
counts=[]
for size in (30,100):
    values=[(i,10) for i in range(size)]
    collections[0]=0
    stats=c.call('STDMATH','descriptive',values)
    counts.append(collections[0])
    reference=[Fraction(*v) for v in values]
    mean=sum(reference)/size
    squared=sum((x-mean)**2 for x in reference)
    assert Fraction(*stats['MEAN'])==mean
    assert Fraction(*stats['POPULATION VARIANCE'])==squared/size
    assert Fraction(*stats['SAMPLE VARIANCE s^2'])==squared/(size-1)
    assert not c.topic_modules(),c.topic_modules()
assert max(counts)<=12,counts
assert counts[1]<=counts[0]+2,counts
print(counts)
'''
        run=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
