# StatScholar

A question-guided statistics tutor for the TI-84 Plus CE Python / Evo project.
Run **STAT1** to identify a method, enter data, calculate an answer and work
through related parts of a question.

The project is named StatScholar; its calculator entry file remains `STAT1.py`.

## Status

The current source includes descriptive statistics, probability, dice, binomial
and without-replacement sampling, definitions, worked quizzes and all 30
questions from Practice Test 1.


## Install and run

1. Transfer all **59 `ST*.py` files** to the calculator's Python environment
   using its supported transfer workflow. Preserve their filenames and make
   the modules available together.
2. Restart the Python environment after replacing modules.
3. Run **STAT1**.

Tests are desktop files, not calculator programs. `EVOPROBE.py` is an optional
device diagnostic, not a required runtime module. Source files are distributed
directly; no ZIP bundle is required.

For a desktop walkthrough, Python 3 and its standard library are sufficient:

```sh
python -B STAT1.py
```

## Navigation and input

- Enter a numeric menu choice. Multi-digit choices such as 10 or 24 work,
  including choices on another menu page.
- On the physical-key path, Right advances pages. Left goes to the previous
  page or returns from the first page. Clear/0 returns from the current viewer
  or menu. Menu pages wrap forward; result and definition viewers finish at
  their last page.
- On desktop/native text menus, empty Enter advances, `-` goes back a page,
  and `0` returns. Follow the individual prompts for data entry.
- Exact-number prompts accept decimals, fractions and percentages, such as
  `0.63`, `63/100`, or `63%`.
- Result menus offer decimal places, reduced fractions, percentages and
  calculation steps where supported.

Menu actions have numeric choices, including actions formerly labeled with
letters. Returning from a solver preserves the parent menu page. Right/Left
remain next/previous controls; legacy letter choices still work in text input.

## Home menu

| Option | Purpose |
| --- | --- |
| 1 - Question Words / Help | Match exactly, at most, at least, between, given, AND/OR and other wording to a method. |
| 2 - Binomial | Fixed-chance trial counts: probabilities, statistics, model checks and sampling detours. |
| 3 - Probability | Favorable/total, supplied probabilities, experiments, X/P tables, money, contingency tables, Venn and selections. |
| 4 - Data / Stats | Raw lists, frequencies, probability tables, categories, comparisons and percent of total. |
| 5 - Normal / Z / Graphs | Z-scores, empirical rule, usual limits, relative position and plotting values/instructions. |
| 6 - Study / Concepts | Sampling, measurement, definitions, significance, errors and quiz guides. |
| 7 - Practice Test 1 | Printed questions 1-30, worked answers and solver links. |

Home shows six choices per page. Option 7 is on the next page; entering 7
directly also selects it.

### Binomial: reuse n and p

Home 2 offers Exactly, At most, At least, Less than, More than, Between and
At least one. Between asks which endpoints to include.

Probability answers have subsequent pages for mean, variance, SD, usual
limits, integer bounds, binomial-model quartiles/IQR fences, and cutoff
z-scores/classifications. The same-n,p menu supports another part, explanations,
formatting, an unusual-event check and statistics.

Two-SD unusual counts, IQR outliers and low event probability are distinct
criteria. Model quartiles are discrete binomial quantiles, not raw-data
median-of-halves quartiles. The chosen event threshold and answer format carry
across parts of the same session. Probability appears first; model quartiles
are calculated only when their page is opened.

Example: accept a shipment if at most one of 23 tablets is defective, with
5% defects. Choose **2 -> 2 At most**, enter `23`, `5%`, and `1`.
The binomial answer is **0.6794**. For a large finite shipment this is an
approximation based on treating draws as independent.

### Defective items drawn from a box

Choose **Home 3 -> 14 Defective items / box**, then choose without replacement,
with replacement, or a supplied probability table. For without replacement, enter total items N,
defective/target items K, and number selected n. The session supports event
probabilities, a distribution, mean/variance/SD and further parts with those inputs.

For 8 cameras, 5 defective, and 2 drawn without replacement, P(X=0,1,2) is
respectively **3/28, 15/28, 5/14**, with mean **1.25**.

### Five-number summary and more

Choose **Home 4 -> 1 Raw list of numbers**. The initial report includes n, sum,
mean, sample variance/SD, min, Q1, median, Q3, max, mode, range, IQR and midrange.
It also includes fences, whiskers, outliers and usual limits.
The retained-data menu adds:

- **2 Z-score a value** and **3 Usual / unusual**.
- **4 Outliers** for fences, actual outliers and whisker endpoints.
- **5 Graph this data** for plotting information.
- **6 Compare another list** and **7 Change data**.
- **8 Sample / population**, **9 Edit one value**, and **10 Check all values**.

Quartiles use medians of sorted halves, omitting the center observation for
odd n. The raw entry limit is 100 observations in source; this is not a claim
that every 100-value workflow fits the physical calculator's heap.

Value + Frequency provides the full summary without expanding repeated
observations in memory. Its retained-data menu includes editing a row,
sample/population variance and SD, z-scores, usual checks, and frequency events.
Both input forms use the same mode convention: no repeated value, no peak,
or more than two modes gives DNE.

### Dice and experiments

**Home 3 -> 4** opens dice, coins, cards and other experiments. Guided
event menus cover sums, faces, AND/OR and complements; typed expressions
remain available for more complex events. Multiple-dice sums support strict
and inclusive bounds, including Between. Fair coin counts reuse the binomial
workflow with p = 1/2. Graph actions provide drawing values and instructions.

### Study and practice

**Home 6 -> 3 -> 2** opens simple random, random, systematic, convenience,
stratified, cluster and bias definitions. Long definitions use numbered pages.
Measurement levels, errors, significance, empirical rule and outliers are
also available. Sampling identification separates the selection procedure from
possible bias. Applicable definitions offer a matching calculation action.

Home **7** uses printed Practice Test 1 numbering. Each question has worked
text and question-specific solver actions, including At least one, At most,
full binomial distributions and several z-scores. Solvers ask for your inputs;
they do not silently insert example numbers. Previous/Next question actions
and the retained question-list page make returning to nearby questions easier. Printed question numbers
are separate from older `PT` lookup identifiers. Search supports `pretest 24`.


## Source layout

| Files | Role |
| --- | --- |
| `STAT1.py` | Entry point and home routing |
| `STCORE.py`, `STVIEW.py`, `STPAGE.py` | Arithmetic helpers, input, paging and module lifecycle |
| `STB*.py`, `STSAMPLE.py`, `STFINITE.py` | Binomial and finite-population workflows |
| `STDATA.py`, `STDMATH.py`, `STDESC.py` | Descriptive data workflows and arithmetic |
| `STPROB.py`, `STCOUNT.py`, `STVENN.py` | Probability tables, counting, payoffs and groups |
| `STDICE.py`, `STMDICE.py`, `STEXPER.py` | Dice and other experiments |
| `STNORM.py`, `STZLIST.py`, `STGRAPH.py`, `STHIST.py` | Z/normal helpers and plotting data |
| Other `ST*.py` files | Search, guides, definitions and question banks |
| `tests/` | Desktop regression tests and audit checks |
| `EVOPROBE.py` | Optional device diagnostic |

All runtime source files are below 64 KiB. File size does not measure live
heap: imports and objects need additional memory. Topic modules load on demand
and are released through the shared call mechanism.

## License

Copyright (c) 2026 Gregory King. Licensed under the custom
[StatScholar Free Use / No Sale License](LICENSE), version 1.0.

Personal, educational and internal business use are allowed. You may modify
and share it for free while retaining its notices and terms. Selling the
software, modified versions, or paid products, bundles, subscriptions or hosted
services incorporating its code is prohibited without Gregory King's written
permission. Internal use and ordinary numerical results remain allowed.

These are custom source-available terms, not MIT or GPL. The complete license
is also included as comments in `STAT1.py`.
