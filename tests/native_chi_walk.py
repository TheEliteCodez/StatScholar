import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
if __name__=='__main__':
    exe=Path(sys.argv[1]).resolve();code=(ROOT/'tests/micropython_chi.py').read_text()
    rows=[]
    for heap in (40000,48000,64000):
        run=subprocess.run([str(exe),'-X','heapsize='+str(heap),'-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        passed=run.returncode==0 and 'CHI_NATIVE_PASS 12 ' in run.stdout
        rows.append(dict(heap_requested_bytes=heap,passed=passed,
                         result=run.stdout.splitlines()[-1:] if passed else (run.stdout+run.stderr)[-1800:]))
        print(heap,'PASS' if passed else 'FAIL',flush=True)
    evidence={'scope':'12 real chi-square problems per native 32-bit fixed heap: GOF/independence, reject/fail, 60 categories and 10x10 table, real viewers and final conclusions, PlotLib/key stubs. Not physical Evo proof.',
              'interpreter_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'runs':rows,
              'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('ST*.py')}}
    (ROOT/'artifacts/chi_memory.json').write_text(json.dumps(evidence,indent=2)+'\n')
    assert all(r['passed'] for r in rows if r['heap_requested_bytes']>=48000),rows
