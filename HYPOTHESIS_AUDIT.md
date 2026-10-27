# Hypothesis testing audit

16 scoped menu variants; 89 paths; 0 failures; 0 menus with unchecked options.

All seven Home 15 routes are seeded separately, including both chi-square tests and paired-data regression. Randomness, claim operators, expected-count modes, summary/raw mean input, normality checks, review steps, predictions and residuals are exercised. Calculators, result viewers and module cleanup run normally; menu choices and numeric entries are deterministic desktop fixtures. No remaining topic module entries or live module objects are permitted after a path returns.

Physical TI-84 heap capacity remains unverified. Full path records and runtime hashes are in HYPOTHESIS_AUDIT.json.

| Menu | Checked choices |
| --- | --- |
| STCHI.py:session / EXPECTED FREQUENCIES | 1 ALL EQUALLY LIKELY; 2 GIVEN EXPECTED COUNTS; 3 GIVEN PROBABILITIES |
| STHYIO.py:check / GROUP 1 NORMAL, NO STRONG SKEW / OUTLIERS? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:check / GROUP 2 NORMAL, NO STRONG SKEW / OUTLIERS? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:check / INDEPENDENT GROUPS (NOT PAIRED)? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:check / RANDOM INDEPENDENT OBSERVATIONS? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:check / SRS / RANDOM INDEPENDENT SAMPLE(S)? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:check / TWO GROUPS INDEPENDENT? | 1 YES / GIVEN; 2 NO; 3 NOT GIVEN / UNSURE |
| STHYIO.py:mean_data / GROUP 1 MEAN INPUT | 1 SUMMARY: x-bar, s, n; 2 RAW MEASUREMENTS |
| STHYIO.py:mean_data / GROUP 2 MEAN INPUT | 1 SUMMARY: x-bar, s, n; 2 RAW MEASUREMENTS |
| STHYIO.py:setup / CLAIM ABOUT mu | 1 <; 2 >; 3 NOT EQUAL; 4 <=; 5 >=; 6 = |
| STHYIO.py:setup / CLAIM ABOUT mu1-mu2 | 1 <; 2 >; 3 NOT EQUAL; 4 <=; 5 >=; 6 = |
| STHYIO.py:setup / CLAIM ABOUT p | 1 <; 2 >; 3 NOT EQUAL; 4 <=; 5 >=; 6 = |
| STHYIO.py:setup / CLAIM ABOUT p1-p2 | 1 <; 2 >; 3 NOT EQUAL; 4 <=; 5 >=; 6 = |
| STHYRES.py:show / HYPOTHESIS > REVIEW STEPS | 1 REQUIREMENTS; 2 H0 AND H1; 3 POINT ESTIMATE; 4 CRITICAL VALUES; 5 TEST STATISTIC; 6 DRAW SAMPLING DISTRIBUTION; 7 p-VALUE; 8 INITIAL CONCLUSION; 9 FINAL CONCLUSION; 10 ALL NINE STEPS |
| STREGIO.py:read_pairs / PAIRED DATA INPUT | 1 ENTER x,y PAIRS; 2 TI LISTS L1-L6 (KEEP PAIRS) |
| STREGIO.py:session / REGRESSION / CORRELATION | 1 ALL WORK / RESULTS; 2 SCATTERPLOT / AXES; 3 PREDICT y FROM x; 4 RESIDUAL: OBSERVED - PREDICTED; 5 PAIRED WORK TABLE |
