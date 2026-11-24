import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
if __name__=='__main__':
    exe=Path(sys.argv[1]).resolve()
    code=(ROOT/'tests/micropython_errors.py').read_text()
    rows=[]
    for heap in (40000,48000):
        run=subprocess.run([str(exe),'-X','heapsize='+str(heap),'-c',code],cwd=ROOT,capture_output=True,text=True,timeout=30)
        passed=run.returncode==0 and 'ERROR_NATIVE_PASS 24 ' in run.stdout
        rows.append(dict(heap_requested_bytes=heap,passed=passed,
                         result=run.stdout.splitlines()[-1:] if passed else (run.stdout+run.stderr)[-1800:]))
        print(heap,'PASS' if passed else 'FAIL')
    evidence={'scope':'24 repeated identifier problems at each native 32-bit fixed heap. First run starts STAT1 automatically. Heavy numerical/definition/graph imports blocked; real menus, formatter/viewer, math entry and cleanup. Not device heap proof.',
              'interpreter_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'runs':rows,
              'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('ST*.py')}}
    (ROOT/'artifacts/errors_memory.json').write_text(json.dumps(evidence,indent=2)+'\n')
    assert all(r['passed'] for r in rows),rows
