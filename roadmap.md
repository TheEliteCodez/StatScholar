# Full-screen graph roadmap

New graphs open only when selected. All implementation precedes the combined physical TI test run. Source must remain below 384,000 bytes. Device results are recorded by the user.

## Phase 1: Shared rendering and navigation

[Technical plan](GRAPH_TECHNICAL_PLAN.md#shared)

Optional graph descriptors, small lazy drawing helpers, existing hypothesis compatibility, and key-release handling.

Dependency: none

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

## Phase 2: Continuous probability and sampling distributions

[Technical plan](GRAPH_TECHNICAL_PLAN.md#continuous)

Normal, t, uniform, empirical-rule, positions, sample means and sample proportions with shaded events.

Dependency: phase 1

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

## Phase 3: Intervals and inference distributions

[Technical plan](GRAPH_TECHNICAL_PLAN.md#inference)

Confidence intervals, one-sided bounds, critical areas, chi-square and correlation inference.

Dependency: phase 2

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

## Phase 4: Discrete distributions and event membership

[Technical plan](GRAPH_TECHNICAL_PLAN.md#discrete)

Binomial, hypergeometric, entered/exact distributions, discrete CDFs and paged bars.

Dependency: phase 3

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

## Phase 5: Descriptive plots and set diagrams

[Technical plan](GRAPH_TECHNICAL_PLAN.md#data)

Boxplots, dots, histograms, scatter/fitted line/residuals, QQ, categories, Venn and dice.

Dependency: phase 4

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

## Phase 6: Desktop acceptance and TI checklist

[Technical plan](GRAPH_TECHNICAL_PLAN.md#acceptance)

Route checks, numerical and navigation tests, source inventory, previews and manual TI cases.

Dependency: phase 5

- [ ] Implement all described graph entry points.
- [ ] Verify numerical geometry, menu navigation and lazy loading on desktop.
- [ ] Include exact menu/input/expected-output cases in the TI checklist.
- [ ] User verifies this phase physically on TI.

