import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
if __name__=='__main__':
    exe=Path(sys.argv[1]).resolve();code=(ROOT/'tests/micropython_regression.py').read_text()
    rows=[]
    for heap in (40000,48000,64000):
        run=subprocess.run([str(exe),'-X','heapsize='+str(heap),'-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        passed=run.returncode==0 and 'REGRESSION_NATIVE_PASS 20 ' in run.stdout
        rows.append(dict(heap_requested_bytes=heap,passed=passed,completed_pair_counts=[int(line.split()[1]) for line in run.stdout.splitlines() if line.startswith('REGRESSION_NATIVE_CASE_PASS ')],
                         result=run.stdout.splitlines()[-1:] if passed else (run.stdout+run.stderr)[-1800:]))
        print(heap,'PASS' if passed else 'FAIL',flush=True)
    evidence={'scope':'Five real regression datasets and all four graph modes, 20 frames per fixed native 32-bit heap. Includes 100 pairs, negative and zero slopes, calendar years; real imports/math/viewer, plot/key stubs. Not Evo firmware or display proof.',
              'runs':rows,'interpreter_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),
              'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('ST*.py')}}
    (ROOT/'artifacts/regression_native_memory.json').write_text(json.dumps(evidence,indent=2)+'\n')
    assert all(r['passed'] for r in rows if r['heap_requested_bytes']>=48000),rows
