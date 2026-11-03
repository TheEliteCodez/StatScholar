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

## As-built integration details

`STGPEN` owns shared pixel drawing, the original 5x7 font, coordinate scaling and native key handling. Renderers are separated into curves, intervals, discrete bars, descriptive bars/dots, boxplots, scatter/residuals, QQ preparation, exact uniform means, inference selection and Venn/dice diagrams. The original hypothesis renderer imports the same shared primitives.

The public optional descriptor is `(module_name, function_name, args_tuple)`. `STCORE.graph_lines(lines, descriptor)` adds metadata without duplicating the underlying sequence. Graph-aware drawing instructions preserve metadata through concatenation and the existing work-chain container. Existing two-argument viewer call sites and capture adapters remain compatible.

On a graph-enabled page, 6 returns a request plus scroll position from STVDISP. STCORE releases the viewer through the normal lazy-call cleanup, then invokes the graph descriptor and reconstructs the text page at the same scroll offset. Merely reading or skipping a result does not import its renderer. Right/Enter advances plot pages; Left/Clear returns to the invoking result. Graph-specific options open directly because selecting that option is the explicit request.

Discrete renderers accept model descriptors (binomial/hypergeometric), existing row sequences, or existing row accessors. Table tools reuse the accessor instead of allocating a second probability table. Bars page 16 outcomes at a time with a global vertical scale; categories page 12 at a time with a separate name key. Selected outcomes are red, other bars blue. Event probabilities come from the selected model without rounding outcome cutoffs. CDF jumps use the model's actual mass, including rounded input totals.

Curves have streamed 241-point outlines and shading, not a saved point array. Normal/sample-statistic axes are aligned by the entered mean and SD/SE. Distribution-free z positions show axes without claiming a normal density. Infinite normal percentile cutoffs are labeled at infinity with the corresponding full/empty area. For chi-square df<2, the infinite peak at zero is clipped to the first positive sample height so the right tail remains visible; the x scale and supplied tail area are unchanged.

Interval diagrams distinguish one-sided confidence regions from two-sided intervals; arrows extend in the permitted direction. Only difference intervals force zero onto the axis. Density graphs use relative vertical height except uniform rectangles, whose numerical density is explicitly shown. Venn circle sizes are schematic; region numbers, selected event masks and conditioning denominator carry the exact meaning. For arbitrary conditional events, blue is the selected intersection and gray is the remainder of the conditioning group.

Desktop previews are generated by `python -B tests/render_graph_gallery.py` and use the calculator drawing calls, not independently re-created curves. They are not device screenshots. The original hypothesis preview remains available separately.

## Reproducible checks

- `python -B -m unittest discover -s tests`
- `python -B tests/menu_walk.py`
- `python -B tests/render_graph_gallery.py`

The graph suite includes analytic/reference areas, binomial/hypergeometric mass, strict/open event endpoints, CDF jump geometry, histogram boundaries, interval bounds, QQ positions, constant data, all graph renderers, actual input-route descriptor construction, regression graph menu choices, numeric shortcut behavior and weak-reference cleanup. Physical checks remain in the separate checklist. Tests/helper scripts and artifacts are desktop files and must not be transferred.

Memory details: residual plots transform each observation during axis-range scans and drawing instead of allocating another point list. Exact uniform-mean drawing compares floating display coordinates directly with the requested continuous bounds; exact answer arithmetic stays in its existing solver. Close axis labels use the shared leader-label placement rather than drawing on top of neighboring labels.
