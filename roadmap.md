# Full-screen graph roadmap

[Technical plan](GRAPH_TECHNICAL_PLAN.md) ? [Physical TI checklist](TI_GRAPH_TEST_CHECKLIST.md)

One root program. New graphs require explicit selection; existing graph-specific menu choices open plots directly. Runtime source must remain below 384,000 bytes. Desktop results do not establish TI startup, heap, display or key behavior.

## Phase 1: Shared rendering and navigation

[Technical plan: Shared rendering and navigation](GRAPH_TECHNICAL_PLAN.md#shared)

Dependency: none.

- [x] Extract the existing hypothesis font, line/text primitives and key-release reader into the shared lazy drawing helper; retain existing hypothesis appearance.
- [x] Accept optional (module, function, args) graph descriptors in view/results/paged_results; carry them through drawing/work sequences without copying the text.
- [x] Expose 6 SHOW GRAPH on relevant result pages; unload the text viewer before importing the renderer and restore its scroll position afterward.
- [x] Preserve numeric menu IDs and Left/Clear return behavior; use one navigation line on graphs.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Phase 2: Continuous probability and sampling distributions

[Technical plan: Continuous probability and sampling distributions](GRAPH_TECHNICAL_PLAN.md#continuous)

Dependency: phase 1.

- [x] Normal probabilities, percentiles, labeled axes and empirical-rule regions; observation positions retain the distinction between a z score and a normal model.
- [x] t probabilities, percentiles and critical-value curves with the selected df and signed cutoffs.
- [x] Uniform probability/cutoff rectangles with correct support, density height and shaded areas.
- [x] Sample-mean and sample-proportion sampling distributions with aligned statistic/z axes, SE and probability shading; zero-spread cases render as points.
- [x] Keep unsupported normal approximations on their existing exact-model or explanatory routes; never infer normality from a mean/SD alone.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Phase 3: Intervals and inference distributions

[Technical plan: Intervals and inference distributions](GRAPH_TECHNICAL_PLAN.md#inference)

Dependency: phase 2.

- [x] One/two proportion and one/two mean intervals: estimate, endpoints, E and confidence; include zero for difference intervals.
- [x] Paired intervals and given-center/margin intervals use the same interval renderer; existing numerical methods are unchanged.
- [x] One-sided confidence-bound arrows and critical-value central/tail areas use the existing signed critical values.
- [x] Chi-square has selectable rejection/p-value views on the nonnegative asymmetric curve, labeled CV or TS and alpha or p.
- [x] Correlation review adds selectable test-distribution rejection/p-value views; mean/proportion hypothesis graphs and conclusions remain intact.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Phase 4: Discrete distributions and event membership

[Technical plan: Discrete distributions and event membership](GRAPH_TECHNICAL_PLAN.md#discrete)

Dependency: phase 3.

- [x] Binomial answer, table and shape routes show individual probability bars and exact event membership.
- [x] Hypergeometric, entered x/P(x), exact sample-proportion and available exact sample-mean routes show their actual distributions.
- [x] Exact uniform sample means use the finite convolution density; exact discrete sample means use their calculated probability rows.
- [x] Discrete CDF routes draw right-continuous steps; wide graphs page horizontally with one global y scale and explicit row ranges.
- [x] Sample-proportion count graphs label p-hat=X/n; rounded tables retain their approximate status and are not normalized for display.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Phase 5: Descriptive plots and set diagrams

[Technical plan: Descriptive plots and set diagrams](GRAPH_TECHNICAL_PLAN.md#data)

Dependency: phase 4.

- [x] Ordinary/modified boxplots, outliers and side-by-side comparisons share numeric scales and existing quartile/whisker calculations.
- [x] Dotplots and frequency/grouped/probability histograms preserve numeric spacing, empty gaps, counts and selected class boundaries.
- [x] Regression review provides scatter, fitted line and residual plots; constant-y and perfect-fit cases retain their existing inference meanings.
- [x] QQ graphs honor Blom, Hazen and rank plotting-position choices; category charts page with numeric keys, category names and selection highlighting.
- [x] Venn graphs label all four regions; event masks and conditional denominators use the original A/B model. Dice grids highlight ordered outcomes.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Phase 6: Desktop acceptance and TI checklist

[Technical plan: Desktop acceptance and TI checklist](GRAPH_TECHNICAL_PLAN.md#acceptance)

Dependency: phase 5.

- [x] Run full numerical/regression tests, real graph-descriptor routes, key-release/navigation tests, source compatibility checks and fresh-process module reclamation checks.
- [x] Generate and inspect desktop previews from actual drawing calls; record current runtime inventory and menu replay evidence.
- [x] Provide exact menu/input/expected-picture cases in TI_GRAPH_TEST_CHECKLIST.md, including four conclusion patterns, edge cases and repeated switching.
- [x] Commit graph implementation, tests and documentation; leave every physical TI pass/fail entry pending until the user tests it.

Implementation: complete. Desktop verification: complete. **Physical TI verification: pending.**

- [ ] User verifies this phase on the calculator and records any failure.

## Acceptance status

The combined manual TI run starts after implementation and desktop checks. Record device observations in the checklist; do not convert desktop passes into physical passes. Any device failure reopens the applicable phase.


Desktop evidence (November 2, 2026): 283 tests passed; 38 real-input graph cases plus five regression graph choices; 151 text-menu variants / 1021 paths, zero failures or unchecked discovered choices. Optional graph-only selectors have separate focused coverage. 130 runtime modules / 352,352 source bytes; 31,648 bytes below the limit. See [record](artifacts/graph_validation.json), [menu audit](MENU_AUDIT.md), and [desktop preview gallery](artifacts/graph_gallery.png). All 56 physical TI cases remain pending.
