# StatScholar

A general-purpose introductory college statistics calculator for the TI-84 Evo Python environment. Run
**STAT1**. Calculators accept your own numbers and show results, formulas and
worked substitutions where supported, with optional full-screen graphs and
paper-drawing guidance for relevant results.

There is one program: **156 root `ST*.py` files, totaling 366,485 source bytes**
(as checked November 24, 2026). No separate build folder or build step is required.

## Install and run

1. Remove the previous StatScholar modules from the calculator. Overwriting
   matching names leaves obsolete modules taking up space.
2. Transfer all 156 current root `ST*.py` files together, preserving their names.
   Do not transfer tests, helper scripts, documentation or backups.
3. Restart Python and run **STAT1**. Confirm the heading **STAT1 261124-R14**.
   Select files directly from this project; no package or build folder is used.

R10 reduced the source inventory by 25,029 bytes relative to R9 (383,644 to
358,615 bytes) using two-space indentation and LF line endings. Solver features,
displayed strings, graph labels and license comments are preserved. The
hypothesis graph now releases curve code before labels, labels before the
heading, and heading code before waiting for a key. New helpers STHTHEAD,
STSEWORK and STTBETA are included in the root module set.

Python app-start RAM and the interpreter heap available after startup are
separate constraints. Source-byte totals do not establish either capacity.
Physical Evo startup, transfer, display, keys and heap usage remain unverified.
See [MEMORY_REVIEW.md](MEMORY_REVIEW.md) for constraints, remaining risks, and
the device validation procedure. Remove obsolete STCI.py from prior installs.

For a desktop session, run `python -B STAT1.py` from the repository root.

## Home menu

Enter the displayed option number directly, including two-digit numbers.
Existing shortcut numbers are preserved; Home 1, 7 and 8 are distribution menus.

| Home | Menu | Main tasks |
| --- | --- | --- |
| 1 | Normal distribution | Probability; percentile/cutoff; z/find x; empirical rule; usual/unusual; axes; several values; change mean/SD; critical z* |
| 2 | Binomial | Wording-based events; statistics; model checks; distribution/table tools; without-replacement cross-link |
| 3 | Probability | Counts; supplied probabilities; experiments; discrete tables; payoffs; conditional events; defective-item boxes |
| 4 | Data / stats | Raw lists; frequency tables; discrete probability tables; row/column tables; categories; comparisons; percent of total; regression/correlation |
| 5 | Graphs / data shape | Scatterplot/regression; boxplots; dotplots; histograms; shape/normality; outliers; relative position |
| 6 | Study / concepts | Sampling/design; definitions/search; statistical concepts; rules/formulas |
| 7 | Uniform distribution | Probability; percentile/cutoff; mean/variance/SD/height; rectangle drawing; change endpoints |
| 8 | Student t distribution | Critical t* from confidence/df; probability; percentile; other critical-value inputs; drawing/interpretation |
| 9 | CLT / sampling distributions | Sample-mean and sample-proportion distributions and probabilities; model-dependent exact fallbacks |
| 10 | Sample size calculator | Proportion or mean planning |
| 11 | Confidence interval / MOE | One/two groups; paired original data; margin of error; interval from center and margin |
| 12 | Z-score calculator | Individual value or sample mean |
| 13 | Z* critical value | Confidence, alpha or area inputs |
| 14 | T* critical value | Confidence, alpha or area inputs with df |
| 15 | Hypothesis testing | One/two proportions; one/two independent means; paired test plus interval; chi-square goodness of fit/independence; correlation/regression |
| 16 | Linear regression / correlation | Fit a line; predict y; round answers; residuals; scatter/fitted/residual graphs; definitions |

Use 0 to return/exit menus. In paged text menus, empty Enter advances and minus
returns to the previous page. Physical-key navigation uses Right/Left and Clear
where supported. See [MENU_AUDIT.md](MENU_AUDIT.md) for the detailed menu matrix
and the scope of its replay evidence.

Menu choice reading lives in `STCORE` with key normalization and polling. Menus
do not import `STVIN` to read an answer: that import previously exhausted
calculator memory while allocating 768 bytes from `STVMENU.menu`.
`STVIN` forwards to the shared reader for existing callers. After updating
the complete root module set, restart calculator Python before retesting Home
and regression menus. The shared renderer also avoids duplicate item/alias
containers, and key decoding avoids temporary dictionaries. Desktop tests cover
all 16 Home routes with text, Evo and CE keys; physical heap acceptance remains
pending. See [MEMORY_REVIEW.md](MEMORY_REVIEW.md) for the complete audit scope.

Worked quizzes, practice tests, numbered homework banks, guide-page libraries,
guide/search indexes and the question wizard were removed. Definitions search,
rules/formulas and statistical concepts remain available under Study / concepts.

## Distributions and probability

Normal, Uniform and t probability menus offer below, above and between events.
Percentile/cutoff menus ask for the wording: **AT MOST / BELOW / LESS THAN**,
**AT LEAST / ABOVE / MORE THAN**, or **PERCENTILE / AREA TO LEFT**. Enter the
given percentage directly. An at-least area r is converted to left area 1-r.
For Uniform(0,20), 30% at least gives a cutoff of 14; 30% at most gives 6.
Cutoff results show the numerical answer first, then drawing instructions.
Back/Clear on the answer screen returns without opening the drawing pages.

Normal tasks reuse entered mean and SD, including z/find-x, usual/unusual and
several-value tools. The empirical-rule task can also work from percentages
without parameters. Use **CHANGE MEAN / SD** for a different problem. Uniform
tasks reuse endpoints; use **CHANGE ENDPOINTS** to replace them. Normal outputs
include boundary z work and matching normalcdf/invNorm commands where relevant;
Uniform outputs include width/area work and variance. Student t accepts
fractional degrees of freedom, including Welch df.

Discrete X/P(X) tables are at **Home 3 > 5** and **Home 4 > 3**.
Shared table tools for custom discrete, Binomial, Hypergeometric and dice-sum
models offer probability/bar-height tables, cumulative probabilities, P/xP/x^2P
work tables, discrete percentiles, expected frequencies and moment summaries.
Exact moments/cutoffs require probabilities summing exactly to 1; rounded-input
tables are identified as approximate. A discrete cutoff is the smallest listed
x whose cumulative probability reaches the requested area; the CDF can jump
past that area.

Dice remain at **Home 3 > 4 > 1**. Defective-item boxes remain at
**Home 3 > 14**: without replacement uses Hypergeometric, with replacement
uses Binomial with p=K/N, and a supplied X/P table is another option.
Bernoulli is covered by Binomial n=1. There are no dedicated Poisson, geometric,
exponential or F parameter solvers. Chi-square tests are under Home 15.

## Chi-square and regression

Existing Home option numbers are unchanged. Added routes:

```text
Home 15: HYPOTHESIS TESTING
  1 One proportion z
  2 Two proportions z
  3 One mean t
  4 Two independent means t
  5 Chi-square goodness of fit
      Expected: 1 equally likely / 2 counts / 3 probabilities
  6 Chi-square independence
  7 Correlation / regression
  8 Paired original data: test + interval
Home 11: CONFIDENCE INTERVAL / MOE
  8 Paired original measurements
Home 4: DATA / STATS
  8 Correlation / regression
Home 5: GRAPHS / DATA SHAPE
  1 Scatter / regression
Home 16: LINEAR REGRESSION / CORRELATION
  1 Enter data / fit / predict
  2 Regression definitions (no data entry needed)
  3 Given equation / r / n: equation, mean or DNE
```

Chi-square tests first show an answer screen with TS (chi-square), the right-tail
CV, p-value, df, alpha and the decision with its p-versus-alpha comparison.
Continue with Right/Enter to open the rejection-region graph, then the p-value
graph automatically on the calculator. Press 6 on either text result to reopen
either graph. The statistic is chi-square, not a t-score.
The Home 15 routes release chi-square input/calculation code before opening
results. A small `STCHISH` coordinator loads the answer, dedicated `STGCHI`
graphs, TI steps and worked results in separate stages. TI instructions are a
separate text screen, so they are released before graphs can be reopened from
the worked result. The general distribution renderer is not loaded for these
graphs. `python -B tests/render_chi_graph.py` generates desktop previews;
physical calculator RAM and graph acceptance remain pending.
`STGCHI` uses native plot text for CV/TS labels and a small `STGKEY` key reader.
It does not import the shared `STGPEN` font/drawing module: a device traceback
showed that import exhausting memory while allocating 373 bytes. Fresh-process
Home 15 tests block both `STGPEN` and the general renderer during chi-square
graphs; the updated import still requires a physical calculator retest.
The chi-square TI instructions and worked-result rows also avoid `STWORK`:
the calculator reached `STCHITI.steps` but exhausted memory importing that
shared formatting module. They now use their own small iterable objects,
preserve row-by-row generation and retain the graph shortcut on worked results.
Fresh-process tests block `STWORK` throughout these Home 15 routes, including
the blood-type example with probabilities and rounded expected counts.
The worked results show hypotheses, requirements, expected counts, every cell's
substituted contribution, the expanded statistic sum, degrees of freedom,
critical value, right-tail p-value and conclusions. Drawing instructions appear
as a fallback when graphics are unavailable.
Before the worked results, TI-84 steps show the native test menu, your L1/L2
entries (GOF) or matrix [A] entries (independence), adjusted df, Calculate/Draw,
the substituted chi-square CDF command for p, and Numeric Solver inputs for CV.
Evo List Editor/DISTR/Numeric Solver paths and Plus/CE alternatives are labeled.
Native workflow references: TI's [GOF test instructions](https://education.ti.com/en/customer-support/knowledge-base/ti-83-84-plus-family/product-usage/34844),
[independence test instructions](https://education.ti.com/en/customer-support/knowledge-base/ti-83-84-plus-family/troubleshooting-messages-unexpected-results/34872),
and [Evo Numeric Solver guide](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/numeric-solver).
Goodness of fit accepts 2..60 categories and an estimated-parameter df adjustment;
independence accepts 2..10 rows and columns, using uncorrected Pearson chi-square.
Low expected counts leave the asymptotic result conditional.

Regression is directly available at **Home 16 > 1**. It accepts 3..100 manually
entered pairs or paired TI lists L1-L6 without sorting them independently.
Enter variable/unit labels and correlation-test alpha (use .05 if no test level
is specified; alpha does not affect the fitted equation or predictions).
The initial results show the fitted equation, slope and intercept first, then
worked calculations. Press Back/Clear to leave the work pages, or continue to
the end, to reach the regression results menu:
**1 results, 2 scatterplot, 3 prediction, 4 residual, 5 paired work table,
6 fitted-line graph, 7 residual graph, 8 test-distribution graph,
9 round equation / prediction, 10 regression definitions**.
Option 9 asks for equation significant digits, prediction decimal places and x.
It retains full coefficient precision for prediction and rounds only the output.
For example, enter the nine textbook (pages,cost) pairs, labels pages/dollars,
alpha .05, then choose **9**, enter **4**, **2**, **451**: the equation is
`yhat=0.06896*x + 3.029` and predicted cost is **34.13 dollars**.
Option 3 accepts further x values using the same data.

Outputs include centered sums, slope/intercept, r, r^2, a two-sided correlation
t test and critical r, plus units and interpretation. Graph options use
full-screen plots where available, with a text scatterplot fallback whose
overlapping cells are marked #. Predictions use the centered line for precision.
**Home 16 > 2** opens regression definitions without requiring data; the same
definitions are at **Home 6 > 7 > 7** and included in **Search all definitions**.
They explain the equation, least squares, x/y variables, slope, intercept,
prediction, residuals, r, r^2, scatterplots, interpolation/extrapolation,
influential points and correlation versus causation. Modules load on demand;
source totals are not peak-heap estimates.

Regression runs in separate lazy stages: `STREGIN` input, `STREG` fit,
`STREGWK` streamed work, `STREGPR` prediction/rounding and `STREGDEF` definitions.
The small `STREGIO` coordinator retains only numeric data and labels between
choices. Work does not import `STWORK`; regression definitions do not import the
general study/definition bank. Critical t and p are calculated in one inference
call, with critical t cached for graphs. Predictions use the cached centered
coefficients. Text scatter fallback uses nine short strings rather than a grid
of character-reference lists.

Scatter and correlation graphs use native plot labels and the small `STGKEY`
reader. They do not load `STGPEN` or the general curve renderer. The correlation
graph shows both critical marks, signed TS and two-tailed rejection/p shading;
scatter and residual plots place variable/unit labels beside their axes and
show numbered ticks at readable intervals, plus the residual zero reference. QQ plots share the smaller scatter renderer.

`python -B tests/regression_walk.py` exercises 117 repeated/maximum-data cases
through all four regression routes, including all choices and definitions, with
six unnecessary imports blocked. It checks module, function and class release
between stages. `artifacts/regression_memory.json` records exact source hashes
and observations; source-byte observations are not physical heap measurements.
The calculator previously failed on `STWORK` (80-byte allocation) and `STVIN`
(768-byte allocation) imports. Both import paths have been removed from these
workflows. The current source still requires manual physical acceptance after
transfer and a Python restart; see [MEMORY_REVIEW.md](MEMORY_REVIEW.md).

**Home 16 > 3: GIVEN EQUATION / r / n** handles supplied regression output
without reconstructing raw pairs. First choose **1 y=ax+b** or **2 y=a+bx**,
matching the printed equation. Enter **a** and **b** exactly as supplied. The
prompts show both the role and letter, such as `SLOPE (a=) (x COEFFICIENT)`
and `INTERCEPT (b=) (CONSTANT)`. The program maps their roles: in y=ax+b, a is slope and b is intercept; in y=a+bx,
a is intercept and b is slope. Enter r (not r^2), n, alpha (Enter defaults to
.05), mean y if known, observed x
minimum/maximum, and y units. Then enter x and answer decimal places.
For textbook equation/mean/DNE questions, an unknown/outside x range gives DNE;
within the range, significant two-sided correlation uses the equation,
otherwise the mean y is used (DNE if that mean is missing). The screen states
this rule and shows the statistical comparison. Ordinary raw-data prediction
at option 1 retains direct fitted-line prediction.

For the tire-pressure example, choose **1 y=ax+b**, then enter `a=.3858`,
`b=2.02`, `r=.65`, `n=8`, Enter for alpha, `16.7`,
`30`, `45`, `mpg`, `36.5`, `1`. The first page shows **ANSWER=16.7 mpg**,
**USE MEAN y**, x/range, r/critical r, n/alpha, p, mean y and the supplied
line in the supplied form. r^2=.4225 is not needed for this choice; the input
screen explicitly says to skip r^2 and use r=.65. p=.08102035 > .05, so there is insufficient evidence of linear correlation.
Choose **1 ANOTHER x / SAME MODEL** to reuse the entered statistics.

Result pages now put compact answers and available key inputs before worked
substitutions. This covers the shared answer renderer, descriptive summaries,
confidence intervals, hypothesis tests, regression/prediction, binomial,
normal/uniform/t probabilities, CLT and sample-size planning. Hypothesis tests
open on an answer page before the existing nine steps; Clear returns to the
review menu. Detailed calculations, precision controls and graphs remain
available. Values wrap rather than being discarded when they exceed a screen.

Hypothesis page loading is staged separately from the Home 15 menu.
STHYMNU chooses a task and unloads before input; STHYFLOW returns operation
and state data to STAT1 and unloads before each operation. STHYANS supplies
the initial answer, STHYREQ formats steps 1-3, and STHYTS formats steps 4-5.
Other worked pages retain their dedicated helpers. Text formatters return
plain rows and unload before the viewer. The operational graph path uses
STCORE.ht_plot to release curve, label, heading and key code in sequence.
STHYP/STHYSH/STHYRES remain compatibility APIs; Home 15 uses the flat driver.
The previous result payload is cleared before another problem is entered.
The latest physical label-import failure is documented in MEMORY_REVIEW.md;
R10 still requires the user's manual Evo retest.

`python -B tests/hypothesis_memory_walk.py` exercises 20 continuous problems,
all nine steps and review choices 1-12, with real math and viewers and stubbed
plot/key APIs. Weak-reference checks cover modules, functions, classes and old
problem data. `artifacts/hypothesis_memory.json` records the current source
hashes. Injected import failures also check cleanup before a fresh Home route.

### Conditional events

**Home 3 > 12: GIVEN / AND / OR / NOT (A,B)** solves conditional probabilities,
intersections, inclusive unions, complements, only A/B, neither and exactly one.
Choose the supplied information: overlap and given-group probability/count;
a conditional and its given-group probability; or a complete two-event model.
Complete models provide both conditional directions, complement conditionals,
Venn regions, a probability contingency table and compound-event queries.

ASCII labels use `AND / INTERSECTION`, `OR / UNION`, `|` for GIVEN and `NOT A`
for the complement of A. No symbol entry is needed. Fraction/decimal/percent
formats and SHOW METHOD are available. Conditioning on a zero-probability group
is undefined. Independent or mutually exclusive modes require that relationship
to be explicitly supplied.

## Data, z-scores and graphs

At **Home 4 > 1**, enter a count for manual raw-data entry, or enter `L1`
through `L6` at the number-of-values prompt to import a built-in calculator list.
The raw-list follow-up menu also offers **11: LOAD L1**. The 1..100-value limit
applies. Session edits do not write back to the calculator list. The bridge uses
`ti_system.recall_list("1")` for L1; desktop tests simulate it, and physical Evo
list import remains unverified.

Raw-list and frequency summaries show sample and population SD/variance,
notation and formulas. Population variance divides by n; sample variance divides
by n-1. From **DATA > RAW > NEXT > 12: CONFIDENCE INTERVAL: MEAN**, reuse the
current list's cached x-bar, sample s and n for a one-mean t interval (df=n-1).
At least two values are required; no data re-entry is needed.

**Home 12** distinguishes individual z=(x-mu)/sigma from sample-mean
z=(x-bar-mu)/(sigma/sqrt(n)). Enter population sigma directly in sample-mean
mode. For x-bar=4.08, mu=4, sigma=0.05 and n=16, SE=0.0125 and z=6.4.
Use Home 9 for sample-mean/proportion probabilities.

Relevant results include **HOW TO DRAW** pages using the entered values:
curves and shaded areas, intervals, discrete bars, z axes, boxplots, dotplots,
histograms, QQ plots, Venn diagrams and two-dice grids. These are instructions
for drawing on paper. Table drawing guidance follows the final table page;
Binomial wording results retain their statistics pages before the calculation details.

## Sampling distributions and exact fallbacks

**Home 9** continues from a failed normal-approximation check to an exact method
when the required model is available. Existing n, p and population N carry over;
cutoffs remain in sample-mean or sample-proportion units.

- Proportions: exact Binomial for independent trials, or Hypergeometric for a
  random sample without replacement, using N and exact population success count K.
- Means: independent Uniform populations with supplied endpoints; an exact
  discrete population table; or sampling without replacement from the entire
  entered finite population.
- A census mean is a point mass. A normal population permits the normal
  sample-mean calculation even for n below 30.

Mean and SD alone do not determine small-sample probabilities for an unknown
nonnormal population. Other dependence requires a joint model; t does not replace
missing normality. Exact proportion cutoffs preserve strict/inclusive endpoints.
Exact uniform and discrete sample-mean calculations can consume substantially
more heap and time than an approximation; device capacity remains unmeasured.

## Sample size, intervals and critical values

**Home 10** offers proportion or mean sample size. Confidence accepts `95%` or
`0.95`. Leave an unknown anticipated proportion blank; 95% confidence and a 5%
margin give n=385. Mean margins use measurement units. Sample size rounds upward;
a supplied sample SD gives an approximate planning size.

**Home 11** offers proportion intervals from counts or p-hat (1/2), a mean
interval (3), two-group comparisons (4/5), margin of error (6), and an interval
from center and margin (7). Results also show margin of error.

**Home 13/14** offer two-sided confidence, two-sided alpha, right area, left
area/percentile, one-sided confidence with lower/upper cutoff, and area between
zero and the cutoff. For t, enter df directly, including fractional df, or derive
df=n-1 from a one-sample/paired n. Do not use that shortcut for two-sample Welch df.
For a two-sided 95% interval, z*=1.959964; t* with df=9 is 2.262157. One-sided
95% z is 1.644854. The t shortcuts also appear in **Home 8**, and z* in **Home 1 > 9**.

After a critical-value result, **ESTIMATE / MARGIN** accepts estimate + SE,
estimate + margin, or interval endpoints. It shows the recoverable estimate,
margin, SE and interval/bound with work and drawing guidance. Enter 0 to skip.
Confidence/area alone cannot determine an estimate or margin.

## Hypothesis testing and study tools

**Home 15** offers one proportion, two proportions, one mean, two independent
means, chi-square goodness of fit, chi-square independence and correlation/regression.
Means accept summaries or raw data. Two-proportion tests use pooled p
under H0: p1=p2; two-mean tests use Welch SE and fractional df. Paired-sample
testing is automated under Home 15 > 8 (test plus interval) and Home 11 > 8 (interval only).

The first four tests have nine review steps: requirements, H0/H1, estimate, critical values,
test statistic, drawing, p-value, decision and conclusion. Decisions use unrounded
p <= alpha. Requirement prompts distinguish null/pooled expected counts for
proportions, independence checks and small-sample mean shape/outlier conditions.
Failed or unverified assumptions leave numerical conclusions conditional.

**Home 6 > 10: RULES / FORMULAS** has 16 reusable rule pages.
**Home 6 > 9: STATISTICAL CONCEPTS** covers sampling independence, estimators,
standard errors, and interval assumptions without course/question references. **Home 6 > 7 > 5** searches definitions,
including sampling distributions, SE, p/p-hat, critical values and hypothesis
terms. Search accepts `dist` or `distr` for distribution.

## Worked calculations

Results now include their mathematical work automatically before the answer-format
menu. Option 5 remains available to review the method. Paginated tables show the
assembled work after their final rows. Back/Clear still leaves the result viewer.

Confidence intervals and margin-of-error tools show substituted standard errors,
critical-value products and both endpoint calculations. Hypothesis tests show
null/pooled SE substitutions, Welch's expanded df and the numerical distribution-tail
calculation. Binomial work expands exact, cumulative, interval and complement events
with actual n, p, q and integer cutoffs, retaining the TI commands.

Raw and frequency summaries include expanded sums and a work table for x, f,
x-mean, squared deviations and weighted squared deviations. Discrete distributions
assemble xP and x^2P sums, variance and SD. CLT boundaries, money tools, count-based
probabilities, percentage conversions and nCr/nPr identities also show their inputs
in the arithmetic. Existing sample-size, uniform, normal and z-score work is retained.

Long expansions are replayable sequences generated one line at a time. No n+1
probability list, expanded frequency population or large factorial is allocated to
display a derivation. Source size and desktop replay still do not certify device heap.

Focused checks: `python -B -m unittest discover -s tests -p test_worked_substitutions.py`.

## Desktop checks and device diagnostics

Run from the repository root:

```text
python -B -m unittest discover -s tests
python -B tests/distribution_walk.py
python -B tests/hypothesis_walk.py
python -B tests/advanced_walk.py
python -B tests/regression_walk.py
python -B tests/hypothesis_memory_walk.py
python -B tests/menu_walk.py
```

The unit suite checks calculations, menus, imports and cleanup. The focused
distribution walk reports its scoped menu/path coverage without writing the
full audit. The full menu walk regenerates `MENU_AUDIT.json` and
`MENU_AUDIT.md`, including source hashes, exercised choices and cleanup results.
Inspect failures, uncovered choices and unclassified menu sites before treating
an audit as complete. Deterministic fixtures do not cover every possible input
or sequence of prior selections.

Memory regression tests use fresh desktop processes and real module cleanup,
including large-list/table cases and weak-reference checks. Source bytes and
desktop timings do not measure the calculator heap or prove device performance.
Compare audit source hashes with the current runtime before using report counts
as current evidence.

## Workspace layout

- Root `ST*.py`: the single calculator program; transfer these together.
- `tests/`: desktop regression tests, menu replays and report generators.
- Root `MENU_AUDIT.*` and `HYPOTHESIS_AUDIT.*`: active audit reports; regenerate
  them with `python -B tests/menu_walk.py` and `python -B tests/hypothesis_walk.py`.

The active audit Markdown reports are included alongside the README so its
report links work in a checkout.

## License

Copyright (c) 2026 Gregory King. See [LICENSE](LICENSE) for the StatScholar
Free Use / No Sale license terms.

## Automatic paired-data workflow

At **Home 15 > 8**, choose manual x,y pairs or two TI lists, keeping each pair
in its original row. Enter first/second labels and choose first-minus-second
or second-minus-first. Enter the claim about the population mean difference,
null difference, alpha, sampling/shape status and the requested CI confidence.

The program automatically produces the original-list means and sample SDs,
every subtraction, mean/SD of differences, df, quartiles/fences/outliers,
all nine hypothesis-test steps, Type I/II and alpha interpretations, plus the
paired confidence interval, margin, endpoints and drawing instructions.
A review menu reuses the data for the difference boxplot and prior results.
Home 11 > 8 omits test inputs when only an interval is needed. Two to100 pairs
are supported; regression still requires at least three. The confidence level
is entered explicitly because a one-sided test and a two-sided CI need not
use the same alpha. No manual differences or re-entry between test and CI.

## Full-screen hypothesis graphs

For z and t tests in Home 15, step 6 shows two calculator graph screens:

1. **Rejection region:** solid red tail shading, alpha attached to that area,
   CV and TS labels attached to their lines, and the test decision.
2. **P-value region:** solid blue tail shading, p-value attached to that area,
   the same CV/TS markers and axes, and a description of which tail(s) to shade.

Both views label the standardized axis t/z and the original sample-statistic
axis (x-bar, p-hat, the two-group difference, or paired d-bar). Scores and
original-unit values appear at the CV and TS tick marks. The original scale
marks the null as `H0=...`; the sample estimate is below TS. Conversions use
H0 value + score*SE. The program uses computed values, not example constants.
For two-tailed tests, each shaded tail is labeled alpha/2 or p/2 and the total
alpha/p-value remains in the result text.

Enter/Right advances from rejection to p-value, then to the written work and
conclusions. Clear/Left/0 returns to review from either graph. Review 11 opens
the p-value graph alone; review 12 opens the rejection graph alone. Paired t
tests use the same two-screen sequence. Text drawing instructions remain
available when the calculator graphics module is unavailable.

Line labels are drawn at graph coordinates with a small built-in font rather
than relying on a bottom legend. Label boxes are separated, with colored
leaders pointing to the actual CV, TS, and tail areas. Shading uses 241
streamed positions and a thicker pen without allocating a curve point list.

`python -B tests/render_hypothesis_graph.py` regenerates the two desktop
previews under `artifacts/`. These previews use the calculator drawing calls;
they are not device screenshots. Physical Evo display and heap behavior
still require an on-calculator retest.

Hypothesis z/t calculations finish before the result-page module loads.
The t-distribution module does not import normal-quantile code for validation.
Transfer the current ST*.py files together so math, graph and core interfaces
are from the same version, then restart Python.

The hypothesis controller lives in `STHYP.py`. Text steps are loaded from
`STHYRES.py` (steps 1-5), `STHYDRAW.py` (step 6), `STHYPVAL.py` (step 7), or `STHYEND.py` (steps 8-9) one at a time and released before the viewer or graph opens,
so the text renderer does not remain resident while `STHTPLOT.py` imports.
Fresh-process checks exercise the real viewer and verify renderer reclamation
before graph loading, plus Back/Continue navigation. Physical heap behavior
still requires an on-calculator retry.

## Optional graph expansion

[Roadmap and phase status](roadmap.md) ? [Technical plan](GRAPH_TECHNICAL_PLAN.md) ? [Exact physical TI test cases](TI_GRAPH_TEST_CHECKLIST.md)

On relevant text results, **6 SHOW GRAPH** opens the plot only when selected.
Left/Clear returns to the same text scroll position; Right/Enter advances graph
pages and returns after the last page. Graph-specific menu choices open their
plot directly. Numerical work and existing input reuse remain available.

| Home route | New graph output |
| --- | --- |
| 1 Normal | Probability/percentile shading, original x and z axes, empirical-rule areas |
| 2 Binomial | Event bars, distribution shape/tables, paged discrete CDF |
| 3 Probability | Entered discrete distributions, hypergeometric bars, Venn event/conditional regions, ordered two-dice grids |
| 4 Data | Category charts, reused raw-data plots and QQ plots |
| 5 Graphs | Boxplots/comparisons, dotplots, histograms, scatter, fitted line and residual plots |
| 7 Uniform | Probability rectangles and cutoff shading |
| 8 Student t | Probability/percentile/critical-value curves with df |
| 9 Sampling | Sample-mean/proportion curves, exact discrete fallbacks and exact uniform sample means |
| 11 Intervals | Mean/proportion/paired intervals, given-center/margin diagrams and one-sided bounds |
| 12 z-score | Position axes without assuming a normal density |
| 13-14 Critical values | Central-confidence and tail-area views |
| 15 Inference | Existing z/t graphs retained; new chi-square and correlation test graphs |

The graph helpers load lazily, share the original hypothesis drawing primitives,
and stream curve points. Discrete table tools reuse row accessors rather than
building a second probability table. Wide bars page 16 outcomes at a time with
one vertical scale; category bars page 12 at a time with separate name keys.

`python -B tests/render_graph_gallery.py` creates desktop previews from the real
calculator drawing calls. These are not device screenshots. All physical TI
startup, heap, visual and key acceptance remains pending the checklist run.

## Type I / Type II error identifier

Home 15 > 9 opens the error identifier. Choose one of four modes:

- FROM A CLAIM: choose p, mu, p1-p2 or mu1-mu2; optionally enter context/units;
  choose the claim sign and enter its boundary value. Percentages and decimals
  are accepted. H0/H1 and both errors appear together before the detailed wording.
- FROM GIVEN H0 AND H1: enter the null sign/value and alternative direction
  when needed, then identify whether the original claim is H0, H1 or unspecified.
- IDENTIFY DECISION + TRUTH: choose reject/fail to reject H0 and the actual truth.
  The answer is Type I, Type II, correct decision or cannot determine.
- DEFINITIONS: Type I/alpha, Type II/beta, power=1-beta, and fail-to-reject meaning.

Example: claim p > .40 gives H0: p <= .40 and H1: p > .40. Type I means
concluding p > .40 when actually p <= .40; Type II means failing to find evidence
for p > .40 when actually p > .40. For a claim in H0, Type I rejects a true
claim and Type II fails to reject a false claim. The program never treats
failure to reject as proof of H0. A one-sided null may be written with equality
at its boundary in class; claim mode shows its full null range.

No sample counts, p-value or alpha entry is needed for identifying the type.
The tool classifies the decision and truth supplied by the user; it does not
parse free-form problem prose or calculate beta from a claim alone.

Error definitions are also searchable through Study > Definitions and appear
under Errors / Significance. The interactive tool uses the direct Home 15
route so larger Study/definition modules are released before it loads.

Revision 261124-R11 adds STHERR.py and changes STHYMNU.py, STCORE.py, STDEFS.py
and STSTUDY.py. From a complete R10 installation, manually select those five
files. Otherwise select the full current root ST*.py set; no package is needed.
Tests cover all six claim relations, one/two-group parameters, null/alternative
roles and every decision/truth outcome. Native fixed-heap replay exercises
24 repeated problems at both 40,000 and 48,000 bytes, including automatic
STAT1 startup and heavy-import guards. Physical Evo acceptance is pending.

## Chi-square final conclusion

GOF and independence tests now finish with a separate CHI-SQUARE FINAL
CONCLUSION page after the worked results. It states reject/fail to reject H0,
compares the numeric p-value with alpha, repeats the entered context and gives
a complete conclusion at the selected significance level. GOF describes a
difference from the specified population model; independence describes an
association between the row and column variables. Failure to reject is not
presented as proof of the model or independence. Clear/Back from earlier
results still exits without forcing the last page.

From R11, manually add STCHEND.py and replace STCHISH.py and STCORE.py.
Restart Python and confirm 261124-R12. The complete inventory is 156 root
ST*.py files / 364,761 source bytes. The new formatter loads after the worked
table and TI instruction objects have been released. Tests cover both tests,
both decisions, p=alpha, navigation and real module/function cleanup. Native
fixed-heap replay includes 60 categories and a 10x10 table with final pages
at 40,000, 48,000 and 64,000 bytes. Physical Evo acceptance remains pending.

## Equation and graph of the regression line

Home 16 > 1 accepts the x,y pairs and displays the fitted equation with results.
After that report, select 2 SCATTER + REGRESSION LINE to see data points and
the fitted red line together, or 6 REGRESSION LINE ONLY for the line without
points. Both show yhat=m*x+b, labeled x/y axes, and numeric ticks on the same
graph. Option 11 SCATTERPLOT ONLY preserves the original data-only view;
option 7 remains the residual graph. The Data, Graphs and Hypothesis regression
links use this same menu. Rounded coefficients can still be obtained through
9 ROUND EQUATION / PREDICTION; graphs use the unrounded fitted coefficients.

For the textbook pages/cost data, the graph displays yhat=0.0689596*x + 3.02855
and a visible straight line. Select 9 with four significant digits for the
homework equation yhat=0.06896*x + 3.029. Desktop previews are available in
artifacts/regression_scatter.png and artifacts/regression_line.png; these are
not calculator screenshots. The equation row has its own reserved space.
When plotting is unavailable, the text fallback supplies the equation and
two calculated points for drawing the line on paper.

R13 updates STREGIO.py, STGSCAT.py, STREGTXT.py, STREG.py and STCORE.py. From a
complete R12 installation, manually replace those five files; restart Python
and confirm 261124-R13. The root source set is 156 files / 366,170 bytes.
Regression inference now runs after fitting code unloads, while the public
fit() API retains its default complete-result behavior.

Tests verify endpoints against fitted equations for positive, negative and
zero slopes and calendar-year x values, point visibility, equation signs,
axis labels, all four graph choices, and text fallback coordinates. The
native replay completes the textbook, negative, constant and calendar cases
at 40,000 bytes; its 100-pair case stops during inference at that heap setting,
before graphing. All five cases / 20 graph frames pass at 48,000 and 64,000.
See artifacts/regression_native_memory.json. Physical Evo memory, display and
key acceptance remain pending.

## Plain-language r-squared interpretation

R14 replaces the generic r-squared sentence with the entered variable names
and a percentage, immediately after the numeric r-squared result. Example:
"About 80% of the variation in textbook cost is explained by its linear
relationship with number of pages." It explains variation as how much the y
values differ from their average, and distinguishes explained variation from
the percentage of predictions that are correct. The definition includes an
r-squared=.80 example and the distinction between association and causation.
Constant-y results remain undefined; calculations and logical row counts are
unchanged. From R13, replace STREGWK.py, STREGDEF.py and STCORE.py and confirm
261124-R14. Current inventory: 156 root files / 366,485 source bytes.
