# StatScholar

Introductory college statistics for the **TI-84 Evo Python environment**.

Enter your own data, calculate results, and follow the formulas and worked
substitutions. StatScholar brings probability, statistical inference, regression,
and graphing together in one calculator program: **STAT1**.

## Features

- **Distributions and probability:** normal, binomial, uniform, Student t,
  discrete probability tables, conditional events, counting, and sampling
  without replacement.
- **Descriptive statistics:** raw data, frequency tables, measures of center and
  spread, percentiles, z-scores, and outlier checks.
- **Statistical inference:** confidence intervals, margins of error, sample
  sizes, one- and two-sample tests, paired data, and chi-square tests.
- **Regression and correlation:** fitted equations, predictions, residuals,
  correlation tests, and contextual interpretations of r-squared.
- **Graphs and worked solutions:** labeled plots, rejection regions, p-value
  shading, substituted calculations, and drawing guidance where supported.
- **Study tools:** definitions, statistical concepts, and rules and formulas.

## Install on the calculator

1. Download the repository using **Code > Download ZIP** and extract it.
2. Remove the previous StatScholar modules from the calculator before updating;
   overwriting matching filenames can leave obsolete modules behind.
3. Open [TI Connect Evo](https://connectevo.ti.com/) in your browser and connect
   your calculator. Use it to transfer **all root files matching `ST*.py`**
   together, keeping their names. This includes `STAT1.py` and its supporting
   modules. Leave `tests/` and repository documentation on your computer.
4. Restart the calculator's Python environment and run **STAT1**.

The program runs directly from the source files. No build step or separate
package is required. Keep the complete module set together when installing
or updating.

## Find a calculator

Enter the displayed option number, including two-digit choices.

| Home | Calculator | Typical uses |
| --- | --- | --- |
| 1 | Normal distribution | Probabilities, percentiles, cutoffs, empirical rule |
| 2 | Binomial | Wording-based events, model checks, distribution tables |
| 3 | Probability | Counting, conditional events, discrete tables, experiments |
| 4 | Data / stats | Raw lists, frequency tables, categories, comparisons |
| 5 | Graphs / data shape | Scatterplots, boxplots, histograms, shape, outliers |
| 6 | Study / concepts | Definitions, sampling, study design, rules and formulas |
| 7 | Uniform distribution | Probabilities, cutoffs, mean, variance, rectangle graphs |
| 8 | Student t distribution | Probabilities, percentiles, critical values |
| 9 | CLT / sampling distributions | Sample means and proportions |
| 10 | Sample size calculator | Planning for a mean or proportion |
| 11 | Confidence interval / MOE | One or two groups, paired data, margins of error |
| 12 | Z-score calculator | Individual values and sample means |
| 13 | Z* critical value | Confidence, alpha, or area inputs |
| 14 | T* critical value | Confidence, alpha, or area inputs with degrees of freedom |
| 15 | Hypothesis testing | Proportions, means, paired data, chi-square, correlation |
| 16 | Linear regression / correlation | Fit, predict, interpret, and graph |

Use **0** to return or exit a menu. In paged text menus, **Enter** advances and
**minus** returns to the previous page. Calculator screens use Right/Left and
Clear where supported.

### Common workflows

- **Fit a regression line:** Home **16 > 1**. Enter paired data manually or
  import paired TI lists. Review the equation and calculations, then use the
  results menu for predictions, rounding, fitted-line plots, and residuals.
- **Test goodness of fit:** Home **15 > 5**. Enter observed counts and choose
  equal expectations, expected counts, or supplied probabilities.
- **Test independence:** Home **15 > 6**. Enter the observed contingency table
  and review the statistic, degrees of freedom, p-value, and conclusion.
- **Analyze paired measurements:** Home **15 > 8** for a test and interval,
  or Home **11 > 8** for a confidence interval.
- **Work with a discrete distribution:** Home **3 > 5** or **4 > 3** for
  custom X/P(X) data, moments, and cumulative probabilities.

Distribution tools reuse entered parameters within a session. Use the menu's
change-parameters option when moving to a different problem. Regression keeps
paired observations together and retains full precision for predictions;
rounding changes the displayed answer.

## Run on a computer

From the repository root, start an interactive session:

```sh
python -B STAT1.py
```

Run the desktop test suite:

```sh
python -B -m unittest discover -s tests
```

Desktop checks cover calculations and supported menu and graph routes.
Calculator-specific display, keys, startup memory, and available heap require
physical TI-84 Evo validation; desktop results do not establish device acceptance.
Graph availability depends on the runtime, with text or drawing guidance where
supported.

## Repository layout

| Path | Purpose |
| --- | --- |
| `STAT1.py` | Program entry point |
| Other root `ST*.py` files | Calculator modules; transfer together with `STAT1.py` |
| `tests/` | Desktop regression tests, workflow replays, and development utilities |
| `LICENSE` | Usage and distribution terms |

## License

Copyright (c) 2026 Gregory King.

StatScholar uses the [Free Use / No Sale License](LICENSE). Personal,
educational, and internal business use is permitted under its terms.
Sale or paid commercialization requires prior written permission.
