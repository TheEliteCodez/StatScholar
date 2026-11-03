# StatScholar

A general-purpose introductory college statistics calculator for the TI-84 Evo Python environment. Run
**STAT1**. Calculators accept your own numbers and show results, formulas and
worked substitutions where supported, with optional full-screen graphs and
paper-drawing guidance for relevant results.

There is one program: **130 root `ST*.py` files, totaling 352,352 source bytes**
(as checked November 2, 2026). No separate build folder or build step is required.

## Install and run

1. Remove the previous StatScholar modules from the calculator. Overwriting
   matching names leaves obsolete modules taking up space.
2. Transfer all 130 current root `ST*.py` files together, preserving their names.
   Do not transfer tests, helper scripts, documentation or backups.
3. Restart Python and run **STAT1**.

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

Use 0 to return/exit menus. In paged text menus, empty Enter advances and minus
returns to the previous page. Physical-key navigation uses Right/Left and Clear
where supported. See [MENU_AUDIT.md](MENU_AUDIT.md) for the detailed menu matrix
and the scope of its replay evidence.

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
```

Chi-square tests show hypotheses, requirements, expected counts, every cell's
substituted contribution, the expanded statistic sum, degrees of freedom,
critical value, right-tail p-value, conclusions and drawing instructions.
Goodness of fit accepts 2..60 categories and an estimated-parameter df adjustment;
independence accepts 2..10 rows and columns, using uncorrected Pearson chi-square.
Low expected counts leave the asymptotic result conditional.

Regression accepts 3..100 manually entered pairs or paired TI lists L1-L6 without
sorting them independently. Enter variable/unit labels and alpha. Work appears
automatically, followed by: **1 results, 2 scatterplot, 3 prediction, 4 residual,
5 paired work table**. Outputs include centered sums, slope/intercept, r, r^2,
two-sided correlation t test and critical r, plus units and interpretation.
The scatterplot is a small text plot with numeric axis ranges; overlapping
display cells are marked #. Predictions use the centered line for precision.
These four modules load on demand; source totals are not peak-heap estimates.

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
