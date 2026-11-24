# Runtime memory review

Revision **261124-R14**, November 24, 2026. This review covers the current root
program. Desktop evidence does not establish the TI-84 Evo's available heap,
compiler workspace, fragmentation, or peak allocation during native plotting.
Physical acceptance remains pending. The user performs all device transfers
and testing manually.

## Confirmed failures and causes

The first regression traceback reached the `STWORK` import after constructing
the formatted results. The second reached `STCORE.read_choice` importing
`STVIN` from inside an already allocated menu. The reported failed allocation
sizes (80 and 768 bytes) describe the allocations that failed, not the total
memory needed to finish those workflows.

The screenshot's `STCORE.py` line 78 still dispatches to `STVIN` in the older
source. The current reader is implemented in `STCORE`; the main screen displays
**STAT1 261124-R11**, so a manual installation can be identified without relying
on file dates or traceback line numbers. No runtime MemoryError handler, input
cap, or feature suppression was added.

## Changes that reduce simultaneous allocations

| Area | Current behavior |
| --- | --- |
| Shared menu input | Choice reading runs in `STCORE`; no `STVIN` import while waiting for a key. Numeric scan decoding and key normalization no longer create dictionaries for each key. |
| Shared menu rendering | Reuses list/tuple entries, derives numeric aliases during iteration, and does not build a second display list and alias dictionary. Extra shortcut rows are added to a copy only when needed. Caller entries remain unchanged. |
| Home | An immutable route table replaces the live route dictionary. Probability/data callback context is constructed only for those routes. |
| Regression coordinator | `STREGIO.py` is 1,979 source bytes, reduced from 7,902. Input, fitting, work, predictions, definitions and graphs run in separate lazy calls. Only observations, labels, alpha and the numeric fit persist between choices. |
| Input | `STREGIN` returns observations and labels; its code is released before `STREG` loads. Pair order is retained for both manual and TI-list input. |
| Inference | Critical t and the two-sided p-value are calculated in one `STTCRIT` call. Critical t is cached in the numeric result and reused for the graph. Constant y does not load t inference. |
| Work/results | `STREGWK` produces one line at a time. The report, table, classes and their globals are released when the viewer returns. No shared `STWORK` import. |
| Prediction | `STREGPR` computes from cached centered coefficients, formats only its current result, and is released before the next menu. No fitting-module reimport for prediction or residuals. |
| Definitions | `STREGDEF` contains the 15 regression terms. Regression does not import `STSTUDY` or the general `STDEFS` bank. Study and definition search share the same terms. |
| Scatter/residual graphs | `STGSCAT` draws with native plot primitives and row text; numbered ticks align with both axes and variable/unit labels sit beside the axes. Uses the small `STGKEY` reader. No `STGPEN` font bank. QQ plots share this smaller renderer. |
| Correlation t graph | `STGRT` uses native labels, both critical marks, signed TS and two-tailed shading. Does not load the general curve renderer, font bank, t CDF or quantile code while drawing. |
| Text scatter fallback | `STREGTXT` uses nine short row strings rather than a 9-by-25 list of character references. It does not reimport the fitting module. |

Source sizes explain the decomposition; they are not heap measurements.
No calculator memory limit was inferred from a desktop allocation count.

## Verification

Run from this directory:

```text
python -B -m unittest discover -s tests
python -B tests/regression_walk.py
python -B tests/menu_walk.py
python -B tests/distribution_walk.py
python -B tests/hypothesis_walk.py
python -B tests/advanced_walk.py
```

Full-program baseline from R13; R14 focused wording checks are recorded below:

| Check | Result |
| --- | --- |
| Full unit suite | 323 tests passed |
| Whole-program menu walk | 164 menu variants; 1,106 paths; zero failures, unchecked choices or unclassified menu sites |
| Regression stage walk | 117 runs; zero failures |
| Maximum-data walk | 86 paths; zero failures or unchecked choices |
| Hypothesis walk | 32 scoped menus; 192 paths; zero failures or unchecked choices |
| Distribution walk | 54 menus; 314 paths; zero failures or unchecked choices |
| Audit provenance | The five JSON manifests identify the R13 baseline before R14 wording edits |
| Physical Evo memory/display | Pending manual validation |

The regression walk runs 117 cases through Home 16 and the existing Data,
Graphs and Hypothesis links. It covers all result choices and all 15 definitions,
nine textbook pairs, 100 manual pairs, 100 imported pairs, negative slopes,
constant y, perfect fits and calendar-year inputs, twice with and twice without
plotting. It checks numerical examples, graph counts, and weak references to
modules, module-defined functions and classes at each stage boundary. Imports
of `STVIN`, `STWORK`, `STDEFS`, `STSTUDY`, `STGPEN` and `STGCURV` are rejected
during those regression cases. See `artifacts/regression_memory.json`.

Shared-menu tests open and cancel each of the 16 Home options in text, Evo scan
and CE key modes (48 paths), with `STVIN` blocked and code-retention checks.
Nine injected import failures verify loader cleanup and subsequent access to
another Home route. These failures exercise cleanup; they do not simulate the
calculator's allocator or prove that a given amount of free RAM is sufficient.
Native-graph tests verify both shaded tails, the signed statistic, critical
markers and observed-minus-predicted residuals.

The full menu walk checks displayed menu edges and cleanup of modules,
module-defined functions and classes after each completed path. This catches
retention that merely checking `sys.modules` would miss. The maximum-data walk
also includes 60 categories, 10-by-10 tables and 100 pairs. Hash manifests identify
the exact runtime inspected; do not reuse old counts with changed source.

## Other areas and remaining limits

The shared reader/menu changes apply to every menu using `STCORE.menu`, not just
regression. Existing sample-size, CI, mean-test and chi-square stage-separation
checks remain in the full suite. Other graph types still intentionally use
`STGPEN`; general definition search still loads `STDEFS`. They are exercised
by desktop route tests and menu replay, but are not established to fit every
physical calculator heap state. Repeated exact arithmetic, extreme precision,
large integers, fractions and native graph buffers remain input-dependent.

All ordinary and maximum-size menu paths have finite fixtures. Passing them
cannot promise that every possible input, old installed module combination or
interpreter state will avoid MemoryError. A clean Python restart and the
physical acceptance sequence below are required before calling this device
verified.

## Manual transfer and physical acceptance

There is no package or build folder. Select all current root `ST*.py` files,
including the new regression helpers, using the user's usual transfer workflow.
Preserve other calculator programs. Restart calculator Python and run `STAT1`.
Check the heading **STAT1 261124-R11**; a heading without that revision is not
this source set.

1. Open Home 16 definitions before entering observations, read all terms and
   return. Open the input menu and cancel.
2. Enter the nine textbook pairs, label x as pages and y as dollars, alpha .05.
   Check the initial equation, page forward/back, and leave the work viewer.
3. Choose 9; enter 4 significant digits, 2 decimal places, x=451. Expect
   `yhat=0.06896*x + 3.029` and `PREDICTED y=34.13`.
4. Exercise result options 1 through 10, both choices under 8, and several
   predictions/residuals without entering the data again. Return to Home,
   reopen Home 16 and repeat without restarting Python.
5. Check 100 paired values from lists, constant y, perfect fits, and the existing
   regression links from Home 4 > 8, Home 5 > 1 and Home 15 > 7.
6. Between regression sessions, revisit the working normal, binomial, raw-data,
   CI and hypothesis workflows. Record any traceback with the revision shown.

Use `TI_GRAPH_TEST_CHECKLIST.md` for per-screen physical results. No device
operation is part of these desktop audit scripts.

Scatter-axis update: `STGSCAT.py` now draws numeric ticks with 70 bytes of glyph data and its own small renderer, without importing `STGPEN`. The y label is above the vertical axis and the x label is below the horizontal axis. Constant and fractional/negative data have scale checks.


## Supplied statistics and first answer pages

Home 16 > 3 uses `STREGSUM` for supplied slope/intercept, r, n, mean y and
observed range. It computes correlation inference once, releases `STTCRIT`
before display and reuses the numeric result for subsequent x values. The
20-row answer/work object generates text lazily. Textbook prediction selection
is explicit: unknown/outside range -> DNE; inside + significant r -> line;
inside + nonsignificant r -> mean y, or DNE when the mean is absent.

The first eight rows show answer/units, method, x/range, r/critical r, n/alpha,
p-versus-alpha, mean y and equation. A fresh-process test checks those values
on the first screen, repeated predictions, one inference import, absence of
heavy regression helpers and release of module-defined functions/classes.

The shared answer renderer packs short result cells into 30-character rows.
Dedicated CI, hypothesis, raw/paired statistics, regression, sample-size,
normal/uniform/t, binomial and CLT screens prioritize key values before
substitutions. Regression work remains streamed. New first-eight-row tests
verify that common inputs, estimates, SE, critical values, p-values, interval
ends and final answers are visible; existing numerical work tests remain.
No new display module is imported to produce these summaries. Physical Evo
heap/display verification remains pending manual testing.


Equation-copy update: Home 16 > 3 first asks whether the given equation is
y=ax+b or y=a+bx, then prompts for a and b directly. Slope/intercept are mapped
from that selection, and the first answer page retains the supplied equation
form. r^2 is explicitly identified as unnecessary here; the solver uses r.
Fresh-process tests cover both forms, the CO2 example with negative slope,
copying a/b without swapping them, and cancelling before coefficient entry.

Coefficient prompts include both meaning and reported letter: SLOPE (a=) / INTERCEPT (b=) for y=ax+b, and INTERCEPT (a=) / SLOPE (b=) for y=a+bx. The prompt-order tests assert the labels and resulting predictions for both forms.


## Home 15 worked-page import failure (R8)

The R7 physical traceback reaches STHYSH.display and fails while importing a
worked-page module (136-byte allocation). R7 split the formatters but still
kept STHOME, STHYP and STHYSH active during page imports. Its desktop passes
did not establish sufficient calculator heap for those imports.

STAT1 now owns the top-level loop. STHOME.choose returns route data and
unloads before a solver starts. Probability/data callbacks use small CORE
callbacks rather than holding Home's function globals throughout a solver.
This reduces the Home controller baseline for every top-level solver.

For Home 15, STHYFLOW.advance returns one operation and plain state data.
STAT1 performs that operation after the flow module has been released.
Input, inference, summary formatting, individual worked-page formatting,
viewer, review menu and graph imports therefore run without the Home,
STHYP, STHYSH or flow controller code resident. The setup and numeric results
are retained intentionally; previous problem data is cleared before the
next input menu. Existing public STHYP/STHYSH/STHYRES APIs remain available,
but Home 15 does not use those nested controllers for mean/proportion tests.
Paired, regression and chi-square keep their own result workflows.

`tests/hypothesis_memory_walk.py` runs five problem types twice with text
fallback and twice with TI plot/key stubs: one/two proportions, one/two means,
and 100 raw observations. Twenty problems complete in four continuous runs.
Each problem traverses all nine steps, each review selection 1-12 and all-nine
review; native-mode fixtures draw 80 graph frames in total. Guards reject
STHYP/STHYSH/STHYRES/STVIN imports on this path and require Home and flow
module/function objects to be dead before result/graph imports. Math, page
formatters and old result objects have separate lifetime checks. Eight
injected import failures exercise loader unwind and recovery into a fresh
Home route. The full 311-test suite passes. See the JSON audit manifests for
source hashes and individual paths. Source totals are not heap measurements;
physical allocation peaks and TI compilation behavior remain unmeasured.

An additional replay executes those same 20 problems on official MicroPython
v1.29.0-6.gc763859f35 (WebAssembly), with real imports, calculations and text
viewers, plus plot/key stubs. All four batches pass and 80 graph frames are
exercised. Reproduce from the project root with
`node tests/micropython_hypothesis.mjs <path-to-official-micropython.mjs>`.
The interpreter's accompanying micropython.wasm is required. The interpreter
is a development dependency outside the project and is not an upload file.
Its expandable heap makes this a runtime compatibility check, not a bounded
heap test or confirmation of TI firmware behavior. See the
[official WebAssembly port](https://github.com/micropython/micropython/tree/master/ports/webassembly).

## R8 physical failure and fixed-heap investigation (R9)

The new supplied traceback reaches STAT1.hypothesis line 10, then the import
at STCORE.call line 211, and fails allocating 136 bytes. That proves R8 did
not resolve the calculator failure. The traceback does not identify the
requested module; the last displayed screen and calculator gc readings have
been requested to identify and size the physical case.

A native 32-bit MicroPython v1.29.0 interpreter was built locally from upstream
commit 0fd6c573ea815774668bbb16b8e197c8822368b2, with MSVC v143, Release/Win32,
double floats and the normal mark/sweep collector. Only the optional frozen
SSL manifest was emptied; no collector or compiler implementation changed.
The development executable stays outside the calculator project. Its SHA-256
is in artifacts/native_heap.json. This corrects an important limitation of
the earlier WebAssembly check: that port defers collections until returning
to JavaScript and can grow its heap, so its passes cannot establish this
program's fixed-heap behavior.

The same R8 runtime and R9 are replayed with identical
fixtures at -X heapsize=40000,42000,48000,64000. Each completed batch asserts
that gc.mem_free()+gc.mem_alloc() did not increase. Twenty continuous problems
cover all four z/t input routes plus 100 raw observations, all nine worked
steps, every review choice, and text/plot/key fixtures. A separate ten-problem
case imports STAT1 with ON_TI already true so its module body automatically
starts main, matching the entry path visible in the screenshot.

R8 fails at 40,000 and 42,000 in both cases, and passes at 48,000 and 64,000.
R9 passes at 42,000, 48,000 and 64,000 in both cases; 40,000 still
fails. These are requested native GC heap sizes, not device RAM measurements;
actual usable GC capacities and failure tails are recorded in the artifact.
A traced R8 40,000 run fails compiling STHTPLOT, including a 136-byte failure
when import tracing is enabled. That reproduces the failure class and call
path; it does not establish which import failed in the user's screenshot.

Changes address measured compilation peaks rather than merely shrinking
source inventory: STHTPLOT draws curves and axes, then STHTLAB adds positioned
labels, and the smaller STGINK owns the shared packed bitmap font and text
renderer. Twelve normal/t, left/right/two-tail, p/rejection graph traces match R8
command-for-command, including glyph line coordinates (see
artifacts/hypothesis_graph_equivalence.json). The glyph pixels, labels, graph
tails, colors and key behavior are preserved. Shared STGPEN consumers load the smaller helpers too. Mean and
proportion input sessions return their numeric result before the flow loads
STHYINF, so input code no longer overlaps the t-distribution import. The t
critical-value function reuses the existing quantile calculation, removing
a duplicate bisection implementation.

Reproduce the native comparison from the project root with
`python -B tests/native_heap_walk.py <micropython.exe> --baseline <R8-source-directory>`.
Without --baseline, it replays only the current source. The supplied
interpreter must be native 32-bit MicroPython, not CPython or WebAssembly.
The native source build used the upstream mpy-cross.vcxproj followed by
ports/windows/micropython.vcxproj, Configuration=Release, Platform=Win32,
PlatformToolset=v143. Do not transfer interpreters or test files to the Evo.

Physical acceptance is still unresolved. Obtain the last displayed page and
`import gc` followed by `print(gc.mem_free(), gc.mem_alloc())` after the crash.
Compare that evidence with the native replay before treating another upload
as sufficient. No calculator connection or transfer has been performed.

## R9 graph label import failure and source reduction (R10)

The latest physical traceback names STHTPLOT.screens line 61 and show line 41,
then STCORE.call line 211, allocating 136 bytes. In R9, that line imports
STHTLAB while the curve renderer, its closures and shared font helpers are
still live. This confirms that R9's nested graph stages did not fit the
calculator at that point; it is not a stale generic page-import traceback.

R10's operational graph entry is STCORE.ht_plot, called directly by the root
hypothesis driver. It calls the curve, label, heading and key-wait stages one
at a time. Each call returns and releases its stage code before the next
import. STHTPLOT.curve uses small local geometry functions and does not load
the shared font bank. STHTLAB loads only STGINK for glyphs and leader lines;
STHTHEAD uses native row text; STGKEY handles the final key/release. The canvas
is preserved between stages. Compatibility show/screens functions remain,
while Home 15 uses the flat entry. Lifetime guards verify module and function
objects are dead at every operational graph boundary.

The same fixed-heap tests also exposed inference compilation peaks. The
unchanged beta/gamma routines now reside in STTBETA, and floating-point
standard-error work is in STSEWORK. STTCRIT and STWORK retain their public
functions and dispatch/alias the extracted implementations. Hypothesis input
calls the small SE helper directly instead of importing the full work module.

A retained-data native probe reproduces R9's exact screens/show/nested-import
call path when roughly 15-16 KB are free before graph loading. R10 completes
both graph frames at roughly 14.7 KB free. It still fails around 12.5 KB free.
This uses a fixed 64,000-byte native heap and retained 1,024-byte bytearrays;
it is not a TI source-cache emulator. Complete fixture and outputs are in
artifacts/graph_heap_probe.json. The full continuous and automatic-start
native fixtures now pass at a requested 40,000-byte heap; R9 fails there.
Lower 36,000/38,000 settings still fail elsewhere. Current baseline and source
hashes are in artifacts/native_heap.json; those supersede the R8/R9 comparison
above. No physical pass is claimed.

Ninety full PlotLib traces match R9 command-for-command: five parameter axes,
negative/zero/positive statistics, all three tails, and both graph regions.
This covers numeric glyph coordinates, dual axes, labels, shading and headings.
Reproduce with tests/compare_graph_traces.py and a prior R9 source tree.

The root inventory is now 154 files / 358,615 bytes, down from R9's 151 files /
383,644 bytes: 25,029 fewer source bytes. Two-space indentation and LF endings
provide the saving. The compaction pass asserted identical Python ASTs for
every file, including string constants; it kept comments and license notices.
artifacts/source_compaction.json records that whitespace-only pass. Subsequent
intentional stage/helper edits are covered by the runtime hash manifests and
separate tests, rather than being represented as whitespace-only edits.
The available headroom under the repository's 384,000-byte inventory budget
rose from 356 to 25,385 bytes. These are source bytes, not measured free heap.

TI's product page specifies 3.5 MB of user-available memory but does not state
a Python GC heap size. The Evo Python guide page links an older CE reference
PDF, whose CE limits do not establish the Evo's heap. The 384,000-byte figure
is this repository's inventory budget, not a verified TI runtime heap size.
Whether source caches share this Evo firmware's GC heap remains unconfirmed.
Sources: https://education.ti.com/en/products/calculators/graphing-calculators/ti-84-evo
and https://education.ti.com/en/product-resources/eguides/eguide-84-evo/python .

For manual installation select all 154 current root ST*.py files, including
STHTHEAD, STSEWORK and STTBETA. Because source compaction touches the whole
program, transferring only the graph files does not realize the stated total
source reduction. Restart Python and confirm STAT1 261124-R11. Keep device
acceptance pending until the failed graph and repeat-problem sequence passes.

## R11 Type I / Type II identifier

Current inventory: 155 root ST*.py files / 363,566 bytes, November 24, 2026.
The five-file update from R10 is STHERR (new), STHYMNU, STCORE, STDEFS and
STSTUDY. Existing R10 compaction and staged graphics are retained.

Home 15 > 9 directly invokes the lightweight STHERR module. It constructs
hypotheses from all six claim signs or accepts supplied null/alternative
information. The initial output shows both errors, H0, H1 and claim location;
detailed contextual statements follow. A separate decision/truth classifier
covers both errors, both correct outcomes and unknown truth. Definitions
cover alpha, beta and power. It loads no numerical, plotting or definition-bank
module. Study/search still contains the new terms; an experimental direct
Study shortcut was removed after a fixed-heap test exposed retained parent
code at import. It is not present in the final runtime.

Five focused tests exercise the full decision/truth table, all claim signs,
null directions, differences/zero/negative boundaries, initial result rows,
percentage input, real Home routes, cancellation and cleanup. Native replay
runs 24 problems at each of 40,000 and 48,000 bytes with a fixed GC capacity,
automatic first startup, heavy imports blocked, real menus/results and module
cleanup. See artifacts/errors_memory.json and tests/native_error_walk.py.
The general native hypothesis replay still passes its 40,000-byte setting.
Physical calculator heap and display acceptance remain pending.

## R12 chi-square final conclusion

Current inventory: 156 root ST*.py files / 364,761 bytes. The change from R11
adds STCHEND and updates STCHISH plus the STCORE revision. No test inputs,
mathematics or graphs changed. STCHISH now shows a separate final conclusion
after the worked table. It respects Back/Clear on previous pages. The final
page includes the decision, actual p-versus-alpha comparison, entered context,
full significance-level conclusion, both hypotheses and the distinction
between failing to reject and proving a null hypothesis.

The result formatter is small and independent of table generation. The
fresh-process test proves STCHI, STCHIM, STCHRES, STCHROW, STCHITI, STVDISP and
STGCHI modules/functions are released before STCHEND imports. GOF and
independence each exercise reject/fail outcomes twice through actual Home
inputs and real viewers. Separate tests include p=alpha and page navigation.
The complete unit suite has 319 passing tests.

Native MicroPython runs twelve chi-square problems at each fixed requested
heap of 40,000, 48,000 and 64,000 bytes, with both decisions, 60-category GOF,
10x10 independence, real text viewers and plot/key stubs. Every final page is
checked, and each completed problem verifies constant GC heap capacity and
empty topic modules. See artifacts/chi_memory.json and tests/native_chi_walk.py.
These checks do not establish native TI PlotLib memory use or physical Evo
completion. Manually add STCHEND, replace STCHISH/STCORE, restart Python, and
confirm 261124-R12 before recording physical acceptance.

## R13 regression line graphs

Current inventory: 156 root ST*.py files / 366,170 bytes. The R12 update set is
STREGIO, STGSCAT, STREGTXT, STREG and STCORE. Menu 2 now plots the fitted line
with data points, 6 plots only the line, 11 preserves scatter only, and 7
preserves residuals. The first two display the fitted equation in a reserved
native-text row and retain axis names/ticks. Coefficients shown on the graph
use six significant digits; line endpoints use the full-precision fit.
Line-only scaling uses predicted endpoint y values; scatter+line scaling
continues to include the observed points. The line is clipped to the plotting
rectangle. QQ and scatter-only layouts retain the earlier axis geometry.
No general font-bank import was introduced.

The text fallback now supplies the equation and two points on the fitted
line, and uses residual values for a residual request. The public STREG.fit
API defaults to complete inference as before. The operational session requests
only the fit first, then imports t inference after fit-module functions are
released. The regression stage audit explicitly rejects a retained fitting
module at that inference import.

Four focused tests validate red-line endpoints by converting graph coordinates
back through numeric tick values and checking the fitted equation. Cases cover
positive/negative/zero slopes, calendar years, line-only versus points,
equation labels, residual/scatter preservation, menu dispatch, and two-point
text instructions. All 323 unit tests and 117 regression replays pass.
Desktop plot previews were inspected for equation/axis overlap and saved as
artifacts/regression_scatter.png and artifacts/regression_line.png.

Native 32-bit replay checks all four graph modes for five datasets including
100 pairs. Simulated input is consumed as entered to avoid retaining a second
raw input copy. At a requested 40,000-byte heap, four smaller datasets complete;
the 100-pair case fails importing t inference before reaching graphing.
At 48,000 and 64,000 all five datasets / twenty graph frames pass. Each frame
checks line/point counts and presence of the equation; completed problems
check fixed GC capacity and topic cleanup. Scope and hashes are recorded in
artifacts/regression_native_memory.json. These limits are not physical Evo
heap measurements or a device pass. No package or device transfer is made.

## R14 r-squared wording

Current inventory: 156 root ST*.py files / 366,485 bytes. STREGWK puts a plain
English sentence with the percent and entered x/y labels directly after the
numeric r-squared line. It explains variation as differences from the average
and distinguishes it from prediction accuracy. STREGDEF uses the same idea
with an 80% example and the causation distinction. STCORE carries the R14
revision. No numerical algorithm, graph, input or dependency changed.
The interpretation row is moved rather than adding a logical report row.

Nine existing chi/regression tests and three answer-summary tests pass.
Additional direct checks verify the percentage, contextual labels, negative
correlation, constant-y behavior and report row counts. Full-program audit
manifests/native records remain historical R13 evidence; they have not been
retagged as new R14 runs for this text-only change. The manual update from a
complete R13 set is STREGWK, STREGDEF and STCORE; confirm 261124-R14.

Pre-push verification: all 323 unit tests passed on the R14 implementation.
Two extra end-of-file blank lines were removed before committing; their ASTs
were verified unchanged. Current source inventory is 366,485 bytes.
