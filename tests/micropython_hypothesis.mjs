// Usage: node tests/micropython_hypothesis.mjs /path/to/official/micropython.mjs
// The WASM build can grow its heap. This checks language/runtime execution,
// not fixed-heap capacity, a TI firmware build, or physical graphics.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const {loadMicroPython}=await import(pathToFileURL(path.resolve(process.argv[2])));
const lines=[];
const mp=await loadMicroPython({pystack:8192,stdout:line=>{
    if(line.startsWith('MPY_'))lines.push(line);
}});
for(const name of fs.readdirSync('.').filter(n=>/^ST.*[.]py$/.test(n)))
    mp.FS.writeFile(name,fs.readFileSync(name));
mp.runPython(fs.readFileSync('tests/micropython_hypothesis.py','utf8'));
if(lines.filter(line=>line.startsWith('MPY_BATCH_PASS')).length!==4 ||
   !lines.some(line=>line.startsWith('MPY_PASS ')))throw Error('Incomplete replay');
console.log(lines.join('\n'));
