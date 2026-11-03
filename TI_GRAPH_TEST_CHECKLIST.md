# Physical TI graph acceptance checklist

**Every device result is pending.** Desktop tests/previews do not count as calculator passes.

Device model: __________  OS: __________  Python version: __________  Test date: __________

## Install and controls

1. Remove the previous calculator copies before transferring the current root `ST*.py` files together. Launch **STAT1** after restarting Python. Do not transfer tests, Markdown/JSON reports, desktop images, caches or helper scripts. No EVOMEM/EVOPROBE is needed.
2. First record whether the Python file selector and STAT1 start successfully. If either fails, record the exact message; do not mark later cases passed.
3. Menu paths below start at STAT1. Choose the numbered option and confirm with Enter. Where a menu is paged, use Right to find the stated label; the printed option ID is unchanged.
4. On a text result showing **6 SHOW GRAPH**, press **6** directly. Graph-specific menu choices open the plot directly. Right/Enter advances a graph page and returns to results after the last page; Left/Clear returns immediately. Existing hypothesis automatic graph screens keep their original review flow.
5. For every case: check the numbers, title/axes/units, readable labels, shaded region, Left and Clear, Right completion, reopening without re-entry, and the text scroll position after returning. Press/release keys normally, then repeat once while holding a key slightly longer.
6. A number is approximate unless shown as an exact fraction. Allow the last displayed digit to round; do not accept a wrong tail, wrong axis, missing outcome, overlapping label or exception.

Use Enter for every explicitly blank context/population/reference prompt. Random/independent and normal-shape checks below are supplied test conditions, not findings about an unknown dataset.

## A ? Continuous distributions and sampling

| ID | Exact route and inputs | Expected result and picture | Device |
|---|---|---|---|
| A01 | **1 ? 1**; mean 100, SD 15; **2 ABOVE**, x=115; graph 6; skip number of individuals afterward. | P=.1586553; shade right of 115; aligned x/z marks 100/0 and 115/1. | Pending |
| A02 | Same normal data; probability **1 BELOW**, x=85. | P=.1586553; shade left; 85 aligns with z=-1. | Pending |
| A03 | Same; probability **3 BETWEEN**, low=85, high=115. | P=.6826895; shade only between z=-1 and +1. | Pending |
| A04 | **1 ? 2**; mean 100, SD 15; wording **3 PERCENTILE**, area 95%. | x=124.6728; z=1.64485; left area .95. Repeat wording **2 AT LEAST**, 5%: same cutoff, right area .05. | Pending |
| A05 | **1 ? 2**; mean 0, SD 1; percentile 0%, then repeat 100%. | Cutoff -INFINITY/+INFINITY; empty/full left area; no fake finite cutoff or crash. | Pending |
| A06 | **1 ? 6 DRAW/LABEL**; mean 100, SD 15. | Normal graph opens directly; correctly aligned x/z axes. | Pending |
| A07 | **1 ? 4 EMPIRICAL RULE ? 1 WITHIN 1 SD**, then **4 OUTSIDE 1 SD**. Leave optional mean/SD unset. | Text rule is approximately 68%/32%; graph's exact normal areas are about .6826895/.3173105. Correct central/outside shading on z units. | Pending |
| A08 | **8 ? 2**; df=9; event **2 ABOVE**, t=2. Then repeat below -2 and between -2,+2. | One tail about .0382764; middle about .9234472; t axis and df=9, not a claim that t has SD=1. | Pending |
| A09 | **8 ? 3**; df=9; wording **3 PERCENTILE**, 95%. Then **8 ? 5** with df=9. | Percentile t=1.833113; left area .95; draw-curve choice opens directly. | Pending |
| A10 | **7 ? 1**; a=2,b=12; **3 BETWEEN**, low=4,high=8. | P=.4; rectangle only on [2,12], height .1; shade [4,8]. | Pending |
| A11 | **7 ? 2**; a=0,b=20; wording **2 AT LEAST**, 30%. Then **7 ? 4**. | Cutoff 14; shade right with area .3; rectangle option opens directly. | Pending |
| A12 | **9 ? 2**; context blank, mu=100,sigma=15,n=36; random **1 YES**, population N blank, population normal **1 YES**; probability **2 ABOVE**, cutoff 105. | SE=2.5, z=2, P=.0227501; x-bar/z axes and sample-mean curve. | Pending |
| A13 | **9 ? 4**; context blank,p=.4,n=100; random **1 YES**, population N blank; **2 ABOVE**, cutoff .5. | SE=.0489898,z=2.04124,P=.0206134; p-hat/z axes. | Pending |
| A14 | **9 ? 3**; p=.4,n=100, random YES,N blank. Repeat **9 ? 1** with mu=100,sigma=15,n=36, random YES,N blank,normal YES. | Sampling-distribution graphs without selected probability; correct centers and SEs. | Pending |
| A15 | **9 ? 2**; mu=5,sigma=0,n=1, random YES,N blank,normal YES; event BELOW, cutoff 5. | P=0; one point at 5, no bell or division by zero. Repeat ABOVE 5, then BETWEEN 5 and 5: P=0 and 1. | Pending |
| A16 | **12 ? 1**; x=115,mean=100,SD=15. | z=1; graph offers aligned position axes without claiming a normal density merely from a z score. | Pending |

## B ? Intervals and inference

| ID | Exact route and inputs | Expected result and picture | Device |
|---|---|---|---|
| B01 | **11 ? 1**; x=60,n=100,C=95%. Repeat **11 ? 2**; context blank,p-hat=.6,n=100,C=95%. | Both intervals (.5039818,.6960182); PE=.6,E=.0960182; confidence 95%. | Pending |
| B02 | **11 ? 4**; x1=60,n1=100,x2=50,n2=100,C=95%. | Difference .1; interval (-.0371975,.2371975); zero visibly inside. | Pending |
| B03 | **11 ? 3 ? 1 SUMMARY**; mean=100,s=15,n=36,C=95%; skip reference mean. | t*=2.0301079; interval (94.9247302,105.0752698); PE=100; no forced zero squashing this ordinary mean interval. | Pending |
| B04 | **11 ? 5**; group 1 **1 SUMMARY**,100,15,36; group 2 **1 SUMMARY**,105,18,40; C=95%. | Difference=-5,df=73.58635; interval (-12.5487376,2.5487376); zero inside. | Pending |
| B05 | **11 ? 7 ? 1 PROPORTION**; center=.6,E=.05. Repeat mean option **2**, center=100,E=5. | Endpoints (.55,.65) and (95,105); E shown; no invented confidence level. | Pending |
| B06 | **13 ? 1**; C=95%; use graph 6, then Right through text and **0 SKIP** estimate work. Repeat **13 ? 2**, alpha=.05. | z*=1.959964; first shades central .95, second both tails total .05. | Pending |
| B07 | **14 ? 1**; C=95%; df source **1**, df=9; graph; skip estimate work with 0. | t*=2.262157; central .95, df=9. | Pending |
| B08 | **13 ? 5**; one-sided C=95%; cutoff **1 LOWER**; view critical graph; continue to estimate source **1 PE+SE**, PE=100,SE=2; graph 6 on resulting work. | Critical=-1.644854; upper bound=103.289707; confidence region arrow extends left. Repeat cutoff **2 UPPER**: lower bound=96.710293, arrow right. | Pending |
| B09 | **11 ? 6 ? 1 PROPORTION**; C=95%,x=60,n=100. | E=.0960182; optional critical curve has middle .95 and symmetric cutoffs. | Pending |
| B10 | **15 ? 5 GOODNESS OF FIT**; context blank,random **1 YES**,alpha=.05,k=4; observed 30,10,20,20; expected **1 EQUAL**; fitted parameters=0. On result graph 6, choose **1 REJECTION**, reopen and choose **2 p-VALUE**. | chi-square=10,df=3,CV=7.8147279,p=.0185661; asymmetric nonnegative curve; right-tail alpha and p views. | Pending |
| B11 | **15 ? 6 INDEPENDENCE**; context blank,random YES,alpha=.05,rows=2,columns=2; row-major counts 30,10,10,30; graph choices as above. | chi-square=20,df=1,p=.0000077442,CV=3.841459; no negative support; infinite peak is clipped for display, not replaced by a normal bell. | Pending |
| B12 | **11 ? 8 PAIRED**; input **1 ENTER PAIRS**,n=4; pairs (5,4),(7,5),(8,6),(10,7); labels BEFORE,AFTER; difference **1 FIRST-SECOND**; random YES,normal differences YES,C=95%. Continue summary/work to interval; use graph 6. | d-bar=2,sd=.8164966; interval about (.7008,3.2992); difference axis includes zero. Review **5 SUMMARY AGAIN** or **3 DIFFERENCE BOXPLOT** as labeled. | Pending |
| B13 | **15 ? 1 ONE PROPORTION**; context APPROVAL,random YES,claim **2 GREATER**,null=.5,alpha=.05,x=60,n=100,population N blank. Repeat with x=51. | z=2,p=.0227501,REJECT/TISE support claim; x=51 gives z=.2,p=.4207403,FAIL/TINSE support wording. Existing rejection/p graphs still work. | Pending |
| B14 | Same as B13 but claim **6 EQUAL**; test x=60 then x=51. | Two-tail p=.0455001 then .8414806; final wording warrants rejection / does not warrant rejection of original equality claim. | Pending |
| B15 | **15 ? 3 ONE MEAN**; context SCORES,random YES,claim GREATER,null=65,alpha=.05; **1 SUMMARY**,mean=68.84,s=7.424314,n=10,N blank,normal/no-outlier check YES. | t=1.63559,df=9,p=.068177; existing labeled t graphs and fail-to-reject conclusion retained. | Pending |

## C ? Discrete and exact models

| ID | Exact route and inputs | Expected result and picture | Device |
|---|---|---|---|
| C01 | **2 BINOMIAL ? EVENT page ? 3 AT LEAST**; n=10,p=.5,cutoff=7; graph 6 on first answer. | P=176/1024=.171875; highlight exactly bars 7,8,9,10. | Pending |
| C02 | Same n,p; **6 BETWEEN**,low=2,high=5; endpoints **2 NEITHER**. Repeat endpoints **1 BOTH**, **3 LOWER ONLY**, **4 UPPER ONLY** as labeled. | Open: bars 3,4; closed:2,3,4,5; lower-only:2,3,4; upper-only:3,4,5. Numeric answer and highlighted bars agree. | Pending |
| C03 | New binomial n=40,p=.5,event AT LEAST 20; graph 6; Right through all graph pages. | Three horizontal pages, rows 1-16,17-32,33-41; same y scale; P about .5626853. Left/Clear returns without another input prompt. | Pending |
| C04 | **2 ? Right to STATS/TABLES ? 5 PROBABILITY TABLE/HEIGHTS**; n=4,p=.5; graph 6. Use **6 CDF/WORK/CUTOFF/COUNTS** on that binomial question page, then **2 CUMULATIVE** and graph 6. | Bar masses 1,4,6,4,1 divided by 16; CDF at 0..4 is .0625,.3125,.6875,.9375,1. | Pending |
| C05 | **3 ? 14 DEFECTIVE ITEMS ? 1 NO REPLACE**; N=10,K=4,n=3; **5 SHOW DISTRIBUTION**, graph 6. | Bars x=0,1,2,3; P(X=1)=.5. No normal curve. | Pending |
| C06 | **3 ? 5 DISCRETE TABLE**; 3 rows (0,.25),(2,.5),(5,.25); **10 TABLE/CDF/WORK ? 2 CDF**, graph 6. | Steps jump at 0,2,5 to .25,.75,1; numeric gaps remain unequal. Repeat **1 PROBABILITY TABLE** for bars. | Pending |
| C07 | **9 ? 4**; context blank,p=.1,n=4,random YES,N blank. Continue failed-normal result to exact method; **2 ABOVE**, proportion cutoff=0; graph 6. | Exact binomial P(p-hat>0)=.3439; highlight X=1..4; second labeling states p-hat=X/4. | Pending |
| C08 | **9 ? 2**; mu=.5,sigma=.2886751346,n=2,random YES,N blank,population normal **2 NO**. Exact model **1 KNOWN UNIFORM**,a=0,b=1; event **3 BETWEEN**,low=.25,high=.75; graph 6. | Exact P=.75; triangular sample-mean density on [0,1], center .5, shaded middle. | Pending |
| C09 | Same small-mean route,mu=.5,sigma=.5,n=2,normal NO; exact model **2 DISCRETE TABLE**; 2 rows (0,.5),(1,.5); BETWEEN 0 and .5 inclusive. | Exact P=.75; sample-mean masses .25,.5,.25 at 0,.5,1; included bars 0,.5. | Pending |
| C10 | Repeat C06 with rounded input markers: (0,~.25),(2,~.5),(5,~.24). | APPROX retained in graph title; actual CDF ends .99, not silently normalized to 1. | Pending |

## D ? Data and probability diagrams

| ID | Exact route and inputs | Expected result and picture | Device |
|---|---|---|---|
| D01 | **5 ? 2 BOXPLOT ? 1 RAW**; count=8,values 1,2,3,4,5,6,7,20. | Modified plot opens directly: Q1=2.5,median=4.5,Q3=6.5,whiskers 1/7,outlier dot 20. | Pending |
| D02 | **5 ? 2 ? 2 FIVE-NUMBER SUMMARY**; min=1,Q1=2,median=3,Q3=4,max=5. | Ordinary plot, whiskers min/max; no invented raw-data outliers. | Pending |
| D03 | **5 ? 2 ? 3 SIDE-BY-SIDE**; A has4 values 1,2,3,4; B has4 values 2,3,4,5. | Both boxes appear together on the same numeric axis; then existing work/results remain available. | Pending |
| D04 | **5 ? 3 DOTPLOT**; count=4,values 1,1,2,4. | Two stacked dots at1,one at2,none at3,one at4; preserve the gap. | Pending |
| D05 | **5 ? 4 HISTOGRAM ? 1 RAW**; count=5,values 0,1,2,3,4. Then histogram **4 GROUP CLASSES**, **1 NUMBER OF CLASSES**,start=0,unit=0,count=2. | Class [0,2) count2; final [2,4] count3; touching bars at exactly 2. | Pending |
| D06 | **5 ? 4 ? 3 X+P(X)**; rows (0,.25),(2,.5),(5,.25). | Probability bar heights .25,.5,.25, numeric gaps retained; not category positions 1,2,3. | Pending |
| D07 | **5 ? 1 SCATTER/REGRESSION**; **1 ENTER**,n=4,pairs (1,2),(2,4),(3,5),(4,4); labels x,y;alpha=.05. Continue initial work to review: **2 SCATTER**, **6 FITTED LINE**, **7 RESIDUAL**, **8 TEST GRAPH ? 1**, then repeat **8 ? 2**. | Fit yhat=2+.7x;r=.71818485,t=1.4596009,df=2,p=.28181515. Residuals -.7,.6,.9,-.8; zero reference line. Rejection/p views both two-tailed. | Pending |
| D08 | Repeat regression with (1,3),(2,3),(3,3). Then repeat with (1,2),(2,4),(3,6). | Constant y: scatter works,inference undefined. Perfect line: fitted/residual graphs work,p=0; infinite t is explained rather than plotted at a false finite location. | Pending |
| D09 | **4 ? 1 RAW**; count=3,values 1,2,3; continue summary; **5 GRAPH THIS DATA ? 4 NORMAL PROBABILITY PLOT**; choose **1 BLOM**. Repeat **2 HAZEN**, **3 RANK**. | QQ graph opens; middle point (z=0,x=2); ordered x increases; all conventions retain their own horizontal quantiles. | Pending |
| D10 | **4 ? 5 CATEGORY COUNTS**; n=3; A=1,B=2,C=3; choose category2, graph6. Then **T SHOW ALL PROPORTIONS**,graph6. | Heights1,2,3; B highlighted; category indices match separate name key; proportions1/6,2/6,3/6. | Pending |
| D11 | Repeat category entry with 13 categories named C1..C13 and counts1..13. | First graph page1-12,second13; common y scale13; all category names reachable through keys. | Pending |
| D12 | **3 ? 10 TOTAL/A/B/BOTH**; total100,A60,B50,both30; **1 REGIONS**,graph6. In graph selector test **1 ALL**, **2 OR**, **3 AND**, **6 GIVEN A**, **7 GIVEN B**. | A-only30,both30,B-only20,neither20; P(OR)=.8; P(B|A)=.5 with denominator60; P(A|B)=.6 with denominator50. | Pending |
| D13 | **3 ? 2 GIVEN P(A),P(B),P(BOTH)**; .6,.5,.3; graph6. Then **3 ? 12 GIVEN/AND/OR/NOT**, **3 GIVEN P(A), P(B), P(AND)** and enter the same values; **2 BUILD EVENT**, event **2 B**, probability **2 CONDITIONAL**, given **1 A**; graph6. | P(B|A)=.5; blue overlap; remaining conditioning A region gray; denominator .6, not whole population. | Pending |
| D14 | **3 ? 4 RANDOM EXPERIMENT ? 1 DICE**; n=2; **1 ONE EVENT**,kind **1 SUM**,word **1 EXACTLY**,value7; graph6. Then dice **4 SAMPLE SPACE**. | Event grid has exactly6 highlighted ordered cells; P=6/36; sample-space grid shows all36. | Pending |
| D15 | Same dice route; **2 A AND B**; first SUM EXACTLY7,second DOUBLES; then **3 A OR B** with same events. | AND has0 cells; OR has12 distinct cells; no double counting. | Pending |

## E ? Navigation, memory and completion

- [ ] Start Python/file selector and STAT1 successfully with the transferred set.
- [ ] Run A01 ? B01 ? C01 ? D01 ? D07 ? D12 ? D14 without restarting Python, then repeat twice.
- [ ] In a long text result, scroll down, press6, exit plot with Left, and verify the previous text position is restored. Reopen, then exit with Clear.
- [ ] Hold/release the graph-opening 6 key and closing Right/Left key; ensure the following page is not accidentally dismissed.
- [ ] Run C03's wide graph, both comparison boxes, 100-value raw data with repeated values, and 13-category paging; record readability, delays and any allocation failure.
- [ ] Run the four conclusion combinations in B13-B14; check all decision/p-versus-alpha/claim wording and existing graphs.
- [ ] Exit to Home, reopen the same topic and confirm inputs/results do not become corrupted.
- [ ] Record every failure before changing inputs or restarting. No program/phase is physically verified solely because a later case passed.

## Device result log

Copy a row for each case tested. Use PASS, FAIL or BLOCKED; leave untested cases PENDING.

| Case | Status | Observed result / label issue / delay | Full traceback or startup message | Model / OS |
|---|---|---|---|---|
| | PENDING | | | |

All roadmap device checkboxes remain unchecked until these results are supplied.
