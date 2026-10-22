# StatScholar

A statistics calculator for the TI-84 Python environment. Run **STAT1**.
There is one program: the **100 root `ST*.py` files**, totaling **270,808 bytes**.
No separate build folder or build step is required.

## Install

1. Remove the previous StatScholar modules from the calculator. Overwriting
   matching files leaves deleted quiz and guide modules taking up space.
2. Transfer only the 100 root `ST*.py` files together, preserving their names.
   Do not transfer tests, probes, helper scripts, documentation, or backups.
3. Restart Python and run **STAT1**.

Python's app-start requirement is free calculator RAM, separate from the
Python interpreter heap used after STAT1 starts. Source-byte totals do not
prove that the calculator has enough free RAM to launch Python.

## Menus

Existing calculator option numbers are preserved:

| Home | Calculator |
| --- | --- |
| 2 | Binomial: exactly, tails, between, statistics and subsequent parts |
| 3 | Probability: counts, supplied probabilities, tables, experiments, payoffs and sampling |
| 4 | Data / statistics: raw lists, frequency tables, comparisons and percent of total |
| 5 | Normal / z / graphs: normal, uniform and t distributions plus plotting values |
| 6 | Study / concepts: classification tools, definitions and sampling-distribution concepts |
| 9 | CLT / sampling distributions |
| 10 | Sample size |
| 11 | Confidence intervals / margin of error |
| 12 | Z-score calculator: individual value or sample mean |
| 13 | z* critical value from confidence, alpha or areas |
| 14 | t* critical value from confidence, alpha or areas |

**Home 1, worked quizzes, practice tests, numbered homework banks, guide-page
libraries, guide/search indexes and the question wizard have been removed.**
Their source modules are deleted, rather than hidden behind unused menu entries.
Numeric percent/frequency tools formerly stored in a quiz module now live in
`STPCT.py`.

Enter a menu number directly, including 10, 11 or 12. In text menus, empty Enter
advances, minus goes to the previous page, and 0 returns. Physical-key menus
use Right/Left and Clear where supported.

Calculators with a relevant graph now include **HOW TO DRAW** guidance after
the results: normal / t / uniform probabilities and percentiles, sampling
distributions, confidence intervals, empirical-rule regions, discrete
probability bars, z-score axes, boxplots, dotplots, histograms, QQ plots,
Venn diagrams and two-dice grids. Scroll onward through the result pages;
for probability tables, drawing guidance follows the final table page.
Binomial wording results retain their statistics pages before the drawing
guide. These are instructions for drawing on paper, using entered values,
cutoffs and endpoint rules. Transfer the new `STSKETCH.py` with the other
root files. Physical calculator display and RAM remain unverified.

## Sample size

Choose **Home 10**, then proportion or mean. Confidence accepts `95%` or `0.95`.
For a proportion, leave the anticipated proportion blank if unknown; a margin
of `5%` at 95% confidence gives **385**. Mean margins use the measurement units.
Sample size rounds upward. A supplied sample SD gives an approximate planning size.

## Confidence intervals and margin of error

Choose **Home 11**. Options 1/2 calculate a proportion interval from success
counts or a supplied p-hat; option 3 calculates a mean interval. Options 4/5
compare two groups. Option 6 finds margin of error; option 7 constructs an
interval from a supplied center and margin. Interval results also show margin
of error. Confidence accepts percentages or decimals.

## Source and checks

Desktop launch: `python -B STAT1.py`.
Desktop checks: `python -B -m unittest discover -s tests`.
Tests cover the remaining calculations, menus, imports and module cleanup.
They do not establish physical calculator RAM capacity or transfer success.

The memory regression suite runs in fresh processes with real module cleanup.
It checks literal dispatch targets and repeated calculations across all eight
home categories, including 100-value raw lists, 25-row frequency/probability
tables, a 10-by-10 table, and 60 categories. Result viewers are closed after
their first page in these stress runs; separate navigation tests cover paging.
Weak references check that completed workflows release their topic modules.
Normal, uniform and Student t menus load separate helpers; normal quantiles and
t calculations do not import the legacy `STCI` bundle. Raw summaries stream
observations into the frequency accumulator, and permutations multiply only
the requested factors instead of allocating two factorials.

Physical verification remains required with the calculator's available heap,
especially for very large exact fractions, trial counts or requested precision.
Desktop memory measurements cannot certify those device allocations.

`EVOPROBE.py` is an optional device diagnostic and is not part of the program.

The systematic menu walk is `python -B tests/menu_walk.py`. It exercises real
menu/result renderers and calculations, including shared follow-up menus, and
writes `MENU_AUDIT.json` with the paths, menu choices, cleanup results and runtime
source hashes. See [MENU_AUDIT.md](MENU_AUDIT.md) for the checked menu matrix and
the remaining device verification. Loaded source bytes in that report are not
Python heap measurements.

For actual device readings, optionally transfer `EVOMEM.py` and run **EVOMEM**
instead of STAT1. Use the normal menus, then exit Home with 0. It reports start,
minimum observed and final free heap, the menu at the minimum, remaining topic
modules and any exception. It uses the device's `gc.mem_free` counter; if that
counter is unavailable, it explicitly records no RAM result. Readings include
the monitor's overhead and sample checkpoints, so compilation/arithmetic
transient peaks can be missed. The monitor is not part of the 100 runtime files.

## License

Copyright (c) 2026 Gregory King. See [LICENSE](LICENSE) for the StatScholar
Free Use / No Sale license terms.

Choose **Home 12: Z-SCORE CALCULATOR**, then **1: INDIVIDUAL VALUE x**
or **2: SAMPLE MEAN x-bar**. Individual mode takes x, mean and SD. Sample-mean
mode takes x-bar, population mu, population sigma and sample size n, computes
SE=sigma/sqrt(n), then z=(x-bar-mu)/SE. Do not pre-divide sigma in that mode.
For x-bar=4.08, mu=4, sigma=0.05 and n=16, SE=0.0125 and z=6.4. Results
include the inputs, formulas, substituted work and axis drawing guidance.
Home 9 remains the full sampling-distribution probability workflow.

## Sampling probabilities when the normal checks fail

Home 9 now continues from a failed normal-approximation check into an exact
method when the needed model is available. Existing n, p and population N
carry over. Cutoffs remain in sample-mean or sample-proportion units.

- Proportions: exact binomial for independent trials, or hypergeometric for
  a random sample without replacement. The latter uses N and the exact
  population success count K (inferred from N*p when integral).
- Means: exact calculations for independent uniform populations (enter a,b),
  an exact discrete population probability table, or a random sample without
  replacement from the entire entered finite population. Endpoint / table
  inputs define the exact model; their resulting center and SD are shown.
- A census mean is a point mass at the population mean. A normal population
  still permits the normal sample-mean calculation for n below 30.
- Mean and SD alone do not determine a small-sample probability for an unknown
  nonnormal population. Other dependence needs a joint model; t is not a
  substitute for missing normality. The calculator explains these limits.

Exact proportion cutoffs are converted to counts without rounding, preserving
strict inequalities and included interval endpoints. Uniform sample-mean
probabilities use exact rational arithmetic for the sum-of-uniforms CDF;
discrete means combine all possible sample sums. These finite distributions
can use substantially more calculator heap than an approximation. Desktop
checks do not establish on-device RAM or execution time. Include the new
`STCLTF.py` when transferring the current root runtime.

Definitions search (Home 6 > 7 > 5) includes sample mean, sample proportion,
population mean/proportion, sample/population SD, sampling distribution,
standard error, point estimate and the central limit theorem.

Raw-list and frequency summaries show both sample SD/variance and population
SD/variance together. Scroll past the results for mu / x-bar and sigma / s
notation, the sum of squared deviations, and the SD formulas. Population
sigma uses n in the denominator; sample s uses n-1.

Choose **Home 13: Z* CRITICAL VALUE** or **Home 14: T* CRITICAL VALUE**.
Both offer: (1) two-sided confidence, (2) two-sided alpha, (3) area to the
right, (4) area to the left / percentile, (5) one-sided confidence with
lower/upper cutoff selection, and (6) area between zero and the cutoff.
Enter probabilities as decimals or percentages. For t, enter df directly
(including fractional Welch df), or enter n for a one-sample / paired test
so df=n-1. Do not use that n-1 shortcut for a two-sample problem.

For a two-sided 95% interval, choose option 1 and enter `95%` or `0.95`:
z*=1.959964; t* with df=9 is 2.262157. A one-sided 95% z cutoff is
1.644854 instead. Output shows the signed cutoff or symmetric pair, the
converted left area, equivalent invNorm/invT input, and drawing guidance.
Home 5 > 10 retains confidence + df as option 1 and adds other inputs as
option 4.

**Home 6 > 10: RULES / FORMULAS** contains 16 reusable rule pages covering
empirical / range / IQR rules, independence and CLT conditions, proportions,
z versus t, critical-value tails, binomial requirements, probability rules,
discrete versus continuous events, population versus sample SD, confidence
intervals, sample size, rounding, LLN and significance decisions. Include
the new lazily loaded `STRULE.py` in the root runtime transfer.

After a z*/t* result, the optional **ESTIMATE / MARGIN** menu accepts a point
estimate plus standard error, a point estimate plus margin of error, or
two-sided interval endpoints. Enter 0 to skip. Results show the estimate,
margin, SE when recoverable, formulas with substitutions, interval or
one-sided bound, and number-line drawing guidance. Endpoints give the
midpoint estimate and half-width margin; estimate + SE gives E=|critical|*SE.
Confidence/area inputs alone cannot determine the estimate or margin.

**Home 6 > 11: WHICH FORMULA? EXAM GUIDE** gives exam wording, notation,
formula, assumptions and a calculator path for sample means, sample sums,
sample proportions, mean/proportion intervals and sample sizes. It also
covers individual normal values, binomial/hypergeometric counts, paired
differences, two-group intervals, critical values and interval endpoints.
Sample sums use Home 9 > 2 after dividing total cutoffs by n. Known-sigma
mean intervals use Home 11 > 6 > 2 to get E, then Home 11 > 7 > 2 for ends.

Definitions now explicitly identify p, p-hat, mu_xbar, mu_phat and SE, with
mean/SD of sampling distributions. Related entries cover margin of error,
confidence level, critical value, alpha, df, n/N, sample sums, variance,
unbiased estimation, normal/discrete uniform distributions, percentiles and
hypothesis terminology. Search accepts `dist` or `distr` for distribution.

For **Home 4 > 1: RAW LIST OF NUMBERS**, enter `L1` at the number-of-values
prompt to read the calculator's built-in L1 list. `L2` through `L6` also work.
Or choose **11: LOAD L1** from the raw-list follow-up menu. Entering a count
still starts manual entry. Imported data feed the existing summaries,
z-scores and graph tools; edits within the session do not write back to L1.
The existing 1..100-value limit applies. The TI bridge uses
`ti_system.recall_list("1")` for built-in L1, not the custom-list name "L1".
Desktop tests simulate this bridge; physical Evo behavior remains unverified.

Raw-list arithmetic keeps its exact-arithmetic helpers loaded for the duration
of reading/calculating, then releases them with the topic. A fresh 30-value
descriptive-statistics desktop profile fell from 336 explicit collections to
6 (0.2434s to 0.0220s in the measured runs). Exact sample/population results
and topic cleanup are checked at 30 and 100 values. These timings are desktop
evidence; actual calculator speed must be measured on the device.

From **DATA > RAW > NEXT**, choose **12: CONFIDENCE INTERVAL: MEAN** to use
the current manual or imported list directly. Enter the confidence level;
the one-mean t interval reuses cached x-bar, sample s and n, with df=n-1.
No list re-entry or repeated descriptive calculation is required. Sample s
is used even if the summary display is set to population mode. Results
include SE, t*, margin, endpoints and drawing guidance; the optional
reference-mean check follows. The list needs at least two sample values.

Normal, uniform and t percentiles display a short answer screen first, with
the numerical cutoff at the top. Drawing pages repeat the cutoff. Back/Clear
on the answer screen returns instead of opening the drawing instructions.

Normal, uniform and t percentile/cutoff solvers first ask the question wording:
**AT MOST / BELOW / LESS THAN**, **AT LEAST / ABOVE / MORE THAN**, or
**PERCENTILE / AREA TO LEFT**. Enter the given percentage without manually
complementing it. At-least converts right area r to left area 1-r, shows
that calculation and shades the right tail. For Uniform(0,20), 30% at least
means a 14.0000-minute cutoff; 30% at most means 6.0000 minutes.
