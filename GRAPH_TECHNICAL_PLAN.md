# Graph technical plan

One root runtime; no diagnostic programs or alternate build. Preserve existing calculations, input reuse, and paper-style output.

<a id="shared"></a>
## Shared rendering and navigation

Optional graph descriptors, small lazy drawing helpers, existing hypothesis compatibility, and key-release handling.

<a id="continuous"></a>
## Continuous probability and sampling distributions

Normal, t, uniform, empirical-rule, positions, sample means and sample proportions with shaded events.

<a id="inference"></a>
## Intervals and inference distributions

Confidence intervals, one-sided bounds, critical areas, chi-square and correlation inference.

<a id="discrete"></a>
## Discrete distributions and event membership

Binomial, hypergeometric, entered/exact distributions, discrete CDFs and paged bars.

<a id="data"></a>
## Descriptive plots and set diagrams

Boxplots, dots, histograms, scatter/fitted line/residuals, QQ, categories, Venn and dice.

<a id="acceptance"></a>
## Desktop acceptance and TI checklist

Route checks, numerical and navigation tests, source inventory, previews and manual TI cases.

## Integration contract

Graph descriptors are (module, function, args). STCORE.view/results/paged_results accept an optional graph descriptor. A numeric SHOW GRAPH action invokes it lazily; graph-specific routes invoke directly. Descriptors contain existing scalar/row data, not compiled graph functions. Existing positional APIs remain compatible.

Small STGP* modules draw on ti_plotlib. Shared coordinates cover 320 by 210 pixels, with a title, plot, labels and one control line. Shared helpers own text, lines, points, scaling and key release. Existing hypothesis rendering uses those same helpers. Left/Clear returns to caller; Right advances pages then returns; reopening retains source data.

Curves use original and standardized axes when applicable. Density shapes are calculated from their distributions, including asymmetric chi-square; shading uses the exact requested event. Computed answers remain independent from rendering. A zero spread is a point, not a bell. A z score without a normal model gets aligned axes without a claimed density.

Discrete renderers evaluate rows lazily, retain exact event comparisons, use one global y scale and horizontal pages, and do not merge distinct outcomes. CDFs are right-continuous steps. Data plots preserve numeric gaps, class boundaries, outliers and selected QQ convention. Venn area is schematic, with exact labeled regions and conditioning denominator.

## Acceptance matrix

Desktop: analytic normal and uniform areas, t CDF checks, chi-square support and right-tail geometry, interval endpoint mapping, strict/inclusive discrete membership, CDF jumps, bin totals, outliers, fitted line/residual and QQ coordinates; keys and releases; fresh-process imports and reclamation; root source under 384000 bytes; source parser compatibility (no positional args after starred args). Generate previews from real drawing calls.

TI: provide exact paths and inputs for every family and branch, expected numeric values, visible labels/shading, return and reopen behavior, repeated switching and startup. All physical statuses remain pending until user reports results. Never infer device memory behavior from desktop tests.
