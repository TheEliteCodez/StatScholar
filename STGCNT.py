# Author: TheEliteCodez
# STGCNT - compact guide records; only the selected record is decoded.
import STCORE

def get_guide(gid, field=None):
    if gid == 'C01':
        return STCORE.unpack_guide(
            'Multiplication Principle\n'
            'TYPICAL START:\t"HOW MANY POSSIBLE OUTCOMES"\t"STATE SIZE OF SAMPLE SPACE"\tFOR MULTIPLE STAGES.\n'
            'EACH STAGE HAS SOME\tNUMBER OF CHOICES.\t\tTOTAL OUTCOMES =\tPRODUCT OF CHOICES.\n'
            '1. COUNT CHOICES STAGE 1.\t2. COUNT CHOICES STAGE 2.\t3. CONTINUE FOR ALL STAGES.\t4. MULTIPLY.\n'
            'TYPE PRODUCT.\tOR SAMPLE SPACE SOLVER.\n'
            'DIE + COIN:\t6*2=12.\t\tTWO DICE:\t6*6=36.\n'
            'DO NOT ADD CHOICES\tFOR SEQUENTIAL STAGES.\n'
            'C02 DICE\tC03 nCr\tC04 nPr\n'
            'SAMPLE_SPACE'
            , field)
    if gid == 'C03':
        return STCORE.unpack_guide(
            'Combination nCr\n'
            'TYPICAL START:\t"CHOOSE..."\t"SELECT..."\t"PAIR..."\t"COMMITTEE..."\t\tORDER DOES NOT MATTER.\n'
            'n = TOTAL ITEMS.\tr = NUMBER CHOSEN.\t\tnCr=n!/[r!(n-r)!].\n'
            '1. IDENTIFY n.\t2. IDENTIFY r.\t3. ASK IF A,B SAME AS B,A.\t4. IF YES -> nCr.\n'
            'MATH > PRB > nCr.\tENTER n nCr r.\tOR SOLVER.\n'
            'CHOOSE 2 FROM 8:\t8C2=28.\t\t8*7=56 COUNTS EACH\tPAIR TWICE.\n'
            'IF ORDER MATTERS,\tUSE nPr INSTEAD.\n'
            'C04 nPr\tC01 MULTIPLICATION\n'
            'NCR'
            , field)
    if gid == 'C04':
        return STCORE.unpack_guide(
            'Permutation nPr\n'
            'TYPICAL START:\t"ARRANGE..."\t"ORDER..."\t"RANK..."\t"PRESIDENT AND VP..."\t\tORDER MATTERS.\n'
            'n = TOTAL ITEMS.\tr = POSITIONS FILLED.\t\tnPr=n!/(n-r)!.\n'
            '1. IDENTIFY n.\t2. IDENTIFY r.\t3. ASK IF A,B DIFFERENT\t   FROM B,A.\t4. IF YES -> nPr.\n'
            'MATH > PRB > nPr.\tENTER n nPr r.\tOR SOLVER.\n'
            '8 PEOPLE, PRESIDENT+VP:\t8P2=8*7=56.\n'
            'DO NOT USE nCr WHEN\tROLES/POSITIONS DIFFER.\n'
            'C03 nCr\n'
            'NPR'
            , field)
    if gid == 'R01':
        return STCORE.unpack_guide(
            'Valid Probability Distribution\n'
            'TYPICAL START:\tTABLE WITH x AND P(x).\t"IS THIS A VALID\tPROBABILITY DISTRIBUTION?"\n'
            'CHECK TWO THINGS:\t1. EACH P(x) BETWEEN 0 AND 1.\t2. SUM OF P(x)=1.\n'
            '1. INSPECT EACH P(x).\t2. ADD ALL PROBABILITIES.\t3. IF ANY OUTSIDE 0..1\t   -> INVALID.\t4. IF TOTAL !=1 -> INVALID.\n'
            'USE + OR LIST SUM.\tEXPECTED VALUE SOLVER\tALSO REPORTS SUM P(x).\n'
            '.2 + .5 + .3 = 1.\tALL ARE BETWEEN 0 AND 1.\t-> VALID.\n'
            'DO NOT USE EXPECTED VALUE\tTO DECIDE VALIDITY.\n'
            'R02 EXPECTED VALUE\tR03 VAR/SD\n'
            ''
            , field)
    if gid == 'R02':
        return STCORE.unpack_guide(
            'Expected Value E(X)\n'
            'TYPICAL START:\tTABLE WITH x AND P(x).\t"FIND THE EXPECTED VALUE\tOF X."\t"FIND E(X)."\tQ021 SCORE EXPECTED VALUE\tQ023 RAFFLE EV IS WIN %?\tQ024 GAME EV IS WIN %?\n'
            'x = POSSIBLE VALUE.\tP(x) = ITS PROBABILITY.\t\tE(X)=SUM[x*P(x)].\n'
            '1. CHECK PROBS SUM TO 1.\t2. MULTIPLY EACH x*P(x).\t3. ADD ALL PRODUCTS.\t4. RESULT IS LONG-RUN MEAN.\n'
            'OPTION 1:\tL1=x VALUES.\tL2=P(x).\t1-VAR STATS, FREQ=L2.\txbar=E(X).\t\tOPTION 2: PROGRAM SOLVER.\n'
            'x: 0,1,2\tP: .2,.5,.3\tE=0(.2)+1(.5)+2(.3)\t=1.1.\tQ021: SUM(score*probability)=6.37\tQ023: FALSE: dollars are not a probability\tQ024: FALSE: long-run average dollars per play\n'
            'DO NOT SIMPLY AVERAGE x.\tP(x) VALUES ARE WEIGHTS.\tEXPECTED VALUE CAN BE\tA NON-POSSIBLE DECIMAL.\tEXPECTED DOLLARS ARE NOT %\tE=.85 DOES NOT MEAN 85% WIN\n'
            'R01 VALID DISTRIBUTION\tR03 VAR/SD\n'
            'DISTRIBUTION_SESSION'
            , field)
    if gid == 'R03':
        return STCORE.unpack_guide(
            'Variance / SD of Distribution\n'
            'TYPICAL START:\tx,P(x) TABLE.\t"FIND VARIANCE"\tOR "STANDARD DEVIATION".\n'
            'mu=E(X).\tE(X^2)=SUM[x^2P(x)].\t\tVAR=E(X^2)-mu^2.\tSD=sqrt(VAR).\n'
            '1. FIND E(X).\t2. FIND E(X^2).\t3. SUBTRACT mu^2.\t4. SQRT FOR SD.\n'
            'USE EXPECTED VALUE\tPROGRAM SOLVER FOR\tmu, VAR, SD.\n'
            'IF mu=2 AND E(X^2)=5:\tVAR=5-4=1.\tSD=1.\n'
            'DO NOT FORGET SQRT\tWHEN QUESTION ASKS SD.\n'
            'R02 EXPECTED VALUE\tB09 BINOM SD\n'
            'DISTRIBUTION_SESSION'
            , field)
    if gid == 'R04':
        return STCORE.unpack_guide(
            'Probability from X/P Table\n'
            'TABLE ALREADY GIVES P(X)\tQ020 JURY EXACTLY / FEW\tQ022 WEBCAM DEFECT TABLE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ADD ONLY MATCHING ROWS\n'
            'USE ENTER VALUES / SOLVE\n'
            'P(2<=X<=4)=.024+.018+.005\tQ020: Exactly 5=.0004; <=5 approx .0004; unusual YES at .05. 0+ is rounded.\tQ022: .904; 1-.904=.096; 2..4=.047; exactly 1=.047 unusual at .05\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'DISTRIBUTION_SESSION'
            , field)
    if gid == 'R05':
        return STCORE.unpack_guide(
            'Missing Probability\n'
            'ONE BLANK IN P(X) COLUMN\tQ018 ONE MISSING P(X)\tQ019 COMPLETE P COLUMN\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            '1-SUM(KNOWN PROBABILITIES)\n'
            'USE ENTER VALUES / SOLVE\n'
            '1-(.18+.13+.2+.13+.2)=.16\tQ018: 1-.84=.16\tQ019: 1-(.1+.2+.2)=.5\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'MISSING_PROBABILITY'
            , field)
    if gid == 'R06':
        return STCORE.unpack_guide(
            'Unusual Event Probability\n'
            'IS AN EVENT UNUSUAL?\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'COMPARE EVENT P WITH CUTOFF\n'
            'USE ENTER VALUES / SOLVE\n'
            '.047<=.05: UNUSUAL\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'DISTRIBUTION_SESSION'
            , field)
    if gid == 'R07':
        return STCORE.unpack_guide(
            'Sample Without Replacement\n'
            'BOX; TARGET COUNT; SELECT n\tQ025 8 CAMERAS 5 DEFECTIVE\tQ026 6 CAMERAS 4 DEFECTIVE\tQ027 17 PENS 5 DEFECTIVE\tQ037 8 CAMERAS 3 DEFECTIVE\n'
            'N=ALL OBJECTS\tK=TARGET/DEFECTIVE OBJECTS\tn=OBJECTS DRAWN\tk=TARGET COUNT IN SAMPLE\tE(X)=n*K/N\n'
            'C(K,k)*C(N-K,n-k)/C(N,n)\n'
            'USE ENTER VALUES / SOLVE\n'
            'N=8 K=5 n=2: E=5/4\tQ025: P(0..2)=3/28,15/28,5/14; E=5/4\tQ026: .0667,.5333,.4000; E=1.3333\tQ027: 11/34,33/68,3/17,1/68; E=15/17\tQ037: 5/14,15/28,3/28; E=3/4\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SAMPLE_SESSION'
            , field)
    if gid == 'R08':
        return STCORE.unpack_guide(
            'Expected Profit or Loss\n'
            'PRIZES, COSTS, PROFIT, LOSS\tQ028 FOUR SUIT GUESSES\tQ029 MARBLE PRIZES AND COST\tQ030 INSURER EXPECTATION\tQ031 RAFFLE BUYER / PTO\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'SUM(NET PAYOFF*PROBABILITY)\n'
            'USE ENTER VALUES / SOLVE\n'
            'GOLD/SILVER/BLACK: E=-1/7\tQ028: P(win)=1/256; E=-1.93359375; SD=17.0291422\tQ029: NET outcomes 5,1,-1; P=3/42,9/42,30/42; E=-1/7\tQ030: 259-206000*(1-.999363)=127.78\tQ031: -1.67; eight=-13.33; PTO one=1.67; all=400\n'
            'CHOOSE WHOSE PROFIT\tSUBTRACT COST ONLY ONCE\tKEEP NEGATIVE LOSSES\tE(DOLLARS) IS NOT A WIN %\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'PAYOFF_SESSION'
            , field)
    raise KeyError(gid)
