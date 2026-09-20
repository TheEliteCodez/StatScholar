# StatScholar

A question-guided statistics tutor for the TI-84 Plus CE Python / Evo project.
Run **STAT1** to identify a method, enter data, calculate an answer and work
through related parts of a question.

The project is named StatScholar; its calculator entry file remains `STAT1.py`.

## Status

The current source includes descriptive statistics, probability, dice, binomial
and without-replacement sampling, definitions, worked quizzes and all 30
questions from Practice Test 1.

**Physical calculator validation is still in progress.** Previous device runs
reported MemoryError and keyboard/navigation problems. Lazy loading and
navigation repairs have desktop regression coverage, but desktop tests do not
establish that every physical Evo workflow works.

On September 20, 2026, the desktop regression suite passed **148 tests**.
The menu review identified further improvements listed below; they remain
pending rather than completed features.

## Install and run

1. Transfer all **58 `ST*.py` files** to the calculator's Python environment
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

Some actions still use letter IDs. On the physical numeric scan path, empty
Enter opens `CHOICE / ID` text entry. Numeric replacements are planned.
Back destinations and page retention are not yet consistent across all branches.

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
median-of-halves quartiles. Follow-up event checks currently use .05 even if
the separate unusual-event tool uses another threshold; reconciliation is pending.

Example: accept a shipment if at most one of 23 tablets is defective, with
5% defects. Choose **2 -> 2 At most**, enter `23`, `5%`, and `1`.
The binomial answer is **0.6794**. For a large finite shipment this is an
approximation based on treating draws as independent.

### Defective items drawn from a box

Choose **Home 2 -> next page -> 6 Without replacement**. Enter total items N,
defective/target items K, and number selected n. The session supports event
probabilities, a distribution, mean/variance/SD and further parts with those inputs.

For 8 cameras, 5 defective, and 2 drawn without replacement, P(X=0,1,2) is
respectively **3/28, 15/28, 5/14**, with mean **1.25**. A direct box/defect
choice under Probability is planned.

### Five-number summary and more

Choose **Home 4 -> 1 Raw list of numbers**. The initial report includes n, sum,
mean, sample variance/SD, min, Q1, median, Q3, max, mode, range, IQR and midrange.
The retained-data menu adds:

- **2 Z-score a value** and **3 Usual / unusual**.
- **4 Outliers** for fences, actual outliers and whisker endpoints.
- **5 Graph this data** for plotting information.
- **6 Compare another list** and **7 Change data**.

Quartiles use medians of sorted halves, omitting the center observation for
odd n. The raw entry limit is 100 observations in source; this is not a claim
that every 100-value workflow fits the physical calculator's heap.

Value + Frequency currently reports mean, median and mode rather than the
complete raw-list summary. Full frequency/raw parity, population variance/SD
and individual-entry editing are pending.

### Study and practice

**Home 6 -> 3 -> 2** opens simple random, random, systematic, convenience,
stratified, cluster and bias definitions. Long definitions use numbered pages.
Measurement levels, errors, significance and outliers are also available.

Home **7** uses printed Practice Test 1 numbering. Each question has worked
text and general solver links. Those links currently ask for new inputs and
do not automatically select the question's event. Printed question numbers
are separate from older `PT` lookup identifiers. Search supports `pretest 24`.

## Known limitations and next work

- Physical key mappings, repeated navigation and peak heap usage need device
  verification. Desktop key simulations are not hardware evidence.
- Graph tools mostly supply values, axis labels and drawing instructions,
  rather than rendered boxplots, histograms or normal density curves.
- Normal/Z does not calculate general normal areas or inverse percentiles.
  Find x from z requires a supplied z-score.
- Frequency statistics, mode conventions, letter shortcuts, Back destinations,
  retained formatting and question-specific solver links need improvement.
- Empirical-rule cutoffs currently depend on whether mean/SD were previously
  entered. More direct question-language navigation is planned.
- Quiz/practice answers are examples; opening a solver is a separate workflow
  and does not automatically supply the example values.
- All seven home branches have been reviewed. Question Words pages 2-4 still
  need dedicated review. Proposed menu fixes are not yet implemented.

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

## Desktop verification

Run from the repository root:

```sh
python -B -m unittest discover -s tests
```

The latest run passed **148 tests** in approximately 15 seconds. Coverage
includes arithmetic, selected end-to-end menu flows, input simulation,
question routes, paging and module cleanup. It does not establish full device
compatibility or independently verify every printed worked answer.

The public repository includes source, tests and this README. Local planning,
audit documents and saved test-result logs are intentionally excluded.
