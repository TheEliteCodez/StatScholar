# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGDESC - compact guide records; only the selected record is decoded.
import STCORE

def get_guide(gid, field=None):
    if gid == 'D01':
        return STCORE.unpack_guide(
            'Qualitative vs Quantitative\n'
            'TYPICAL START:\t"CLASSIFY THE VARIABLE..."\t"IS THIS QUALITATIVE OR\tQUANTITATIVE?"\t\tASK YOURSELF:\tIS THE ANSWER A CATEGORY\tOR A NUMBER WITH MEANING?\n'
            'QUALITATIVE:\tCATEGORY/LABEL.\tEX: CITY, COLOR, MAJOR.\t\tQUANTITATIVE:\tNUMERICAL COUNT/MEASURE.\tEX: AGE, MILES, HEIGHT.\n'
            '1. IDENTIFY WHAT IS RECORDED.\t2. CATEGORY/LABEL?\t   -> QUALITATIVE.\t3. NUMERICAL VALUE WHERE\t   ARITHMETIC MAKES SENSE?\t   -> QUANTITATIVE.\n'
            'NO CALCULATOR NEEDED.\tTHIS IS A DEFINITION/\tCLASSIFICATION QUESTION.\n'
            '"WHAT CITY DO YOU LIVE IN?"\t-> QUALITATIVE.\t\t"HOW MANY MILES DO YOU\tCOMMUTE?"\t-> QUANTITATIVE.\n'
            'DIGITS DO NOT AUTOMATICALLY\tMAKE DATA QUANTITATIVE.\tJERSEY #17 IS A LABEL,\tNOT A MEASUREMENT.\n'
            'D02 DISCRETE/CONTINUOUS\tD03 POPULATION/SAMPLE\n'
            ''
            , field)
    if gid == 'D02':
        return STCORE.unpack_guide(
            'Discrete vs Continuous\n'
            'TYPICAL START:\t"IS THE QUANTITATIVE\tVARIABLE DISCRETE OR\tCONTINUOUS?"\t\tMEMORY:\tCOUNT -> DISCRETE.\tMEASURE -> CONTINUOUS.\n'
            'DISCRETE:\tCOUNTABLE SEPARATE VALUES.\t\tCONTINUOUS:\tMEASUREMENT CAN TAKE\tVALUES BETWEEN VALUES.\n'
            '1. CONFIRM IT IS NUMERIC.\t2. IS IT A COUNT?\t   -> DISCRETE.\t3. IS IT MEASURED?\t   -> CONTINUOUS.\n'
            'NO CALCULATOR NEEDED.\n'
            '# OF CHILDREN -> DISCRETE.\tHEIGHT -> CONTINUOUS.\tCOMMUTE DISTANCE ->\tCONTINUOUS.\n'
            'A MEASURED VALUE MAY BE\tROUNDED TO A WHOLE NUMBER\tAND STILL BE CONTINUOUS.\n'
            'D01 QUAL/QUANT\n'
            ''
            , field)
    if gid == 'D03':
        return STCORE.unpack_guide(
            'Population vs Sample\n'
            'TYPICAL START:\t"IDENTIFY THE POPULATION\tAND SAMPLE."\t\tLOOK FOR:\tWHO STUDY WANTS TO DESCRIBE\tVS WHO WAS ACTUALLY ASKED.\n'
            'POPULATION = ENTIRE TARGET.\tSAMPLE = OBSERVED SUBSET.\t\tYOU NEED TO IDENTIFY:\tWHO SHOULD CONCLUSION APPLY TO?\tWHO ACTUALLY PROVIDED DATA?\n'
            '1. READ PURPOSE OF STUDY.\t2. TARGET WHOLE GROUP\t   -> POPULATION.\t3. ACTUAL OBSERVED GROUP\t   -> SAMPLE.\n'
            'NO CALCULATOR NEEDED.\n'
            'OUR COMMUTE PROJECT:\tPEOPLE WE ASKED -> SAMPLE.\tLARGER RELEVANT SRJC\tSTUDENT GROUP -> POPULATION.\n'
            'COLLECTION LOCATION IS NOT\tAUTOMATICALLY POPULATION.\tPOPULATION IS A GROUP OF\tPEOPLE/OBJECTS.\n'
            'D04 PARAMETER/STATISTIC\n'
            ''
            , field)
    if gid == 'D04':
        return STCORE.unpack_guide(
            'Parameter vs Statistic\n'
            'TYPICAL START:\t"IS THIS VALUE A PARAMETER\tOR STATISTIC?"\t\tFIRST ASK WHETHER VALUE\tCOMES FROM POPULATION\tOR SAMPLE.\n'
            'PARAMETER:\tNUMBER DESCRIBING POPULATION.\t\tSTATISTIC:\tNUMBER DESCRIBING SAMPLE.\n'
            '1. IDENTIFY GROUP USED.\t2. WHOLE POPULATION?\t   -> PARAMETER.\t3. SAMPLE?\t   -> STATISTIC.\n'
            'NO CALCULATOR NEEDED.\n'
            'MEAN OF OUR 16 COMMUTES\tIS A STATISTIC.\tTRUE MEAN FOR ENTIRE TARGET\tPOPULATION IS A PARAMETER.\n'
            'MEAN/SD/PROPORTION CAN EACH\tBE PARAMETER OR STATISTIC.\tGROUP SOURCE DECIDES.\n'
            'D03 POPULATION/SAMPLE\n'
            ''
            , field)
    if gid == 'F01':
        return STCORE.unpack_guide(
            'Frequency\n'
            'TYPICAL START:\t"FIND THE FREQUENCY..."\t"HOW MANY OBSERVATIONS..."\tOR A FREQUENCY TABLE.\n'
            'f = NUMBER OF TIMES\tCATEGORY/VALUE OCCURS.\t\tNO DIVISION YET.\n'
            '1. IDENTIFY CATEGORY.\t2. COUNT OCCURRENCES.\t3. THAT COUNT IS f.\n'
            'NO SPECIAL CALCULATOR CMD.\n'
            'IF 6 OF 44 STUDENTS ARE\tIN CATEGORY A:\tFREQUENCY = 6.\n'
            'DO NOT DIVIDE BY n UNLESS\tQUESTION ASKS RELATIVE\tFREQUENCY.\n'
            'F02 RELATIVE FREQUENCY\tF03 CUMULATIVE\n'
            'FREQUENCY_SESSION'
            , field)
    if gid == 'F02':
        return STCORE.unpack_guide(
            'Relative Frequency\n'
            'TYPICAL START:\t"FIND THE RELATIVE\tFREQUENCY..."\t"WHAT PROPORTION IS IN\tTHIS CATEGORY?"\tLONG-RUN PROPORTION\tESTIMATES EVENT PROBABILITY\tQ005 SCRATCHED LENSES\tQ006 LONG-RUN PROPORTION\tQ011 GREEN PEAS\n'
            'f = CATEGORY COUNT.\tn = TOTAL SAMPLE SIZE.\t\tFORMULA:\tREL FREQ = f/n.\n'
            '1. FIND f.\t2. FIND TOTAL n.\t3. DIVIDE f/n.\t4. IF PERCENT ASKED,\t   MULTIPLY BY 100.\n'
            'TYPE f/n ENTER.\tOR CHOOSE SOLVE NOW.\t\tANSWER IS USUALLY DECIMAL\tOR PERCENT.\n'
            'HOMEWORK:\t6 OUT OF 44.\t6/44=.13636...\tREL FREQ=.13636.\tPERCENT=13.636%.\tQ005: 5840/12712=730/1589=0.459 (3 places)\tQ006: Relative frequency estimates event probability\tQ011: 465/609=76.35%; comparison target missing\n'
            'WRONG: n/f.\tPART GOES ON TOP.\t\tDO NOT MULTIPLY BY 100\tUNLESS PERCENT IS WANTED.\n'
            'F01 FREQUENCY\tF03 CUMULATIVE\tF04 PROPORTION\n'
            'CATEGORY_SESSION'
            , field)
    if gid == 'F03':
        return STCORE.unpack_guide(
            'Cumulative Frequency\n'
            'TYPICAL START:\t"COMPLETE THE CUMULATIVE\tFREQUENCY COLUMN."\t\tWORD CUE:\tCUMULATIVE = RUNNING TOTAL.\n'
            'YOU NEED:\tTHE FREQUENCY IN EACH ROW.\t\tLAST CUMULATIVE FREQUENCY\tSHOULD EQUAL TOTAL n.\n'
            '1. FIRST CUM = FIRST f.\t2. NEXT = PREVIOUS CUM\t   + CURRENT f.\t3. KEEP RUNNING DOWN TABLE.\n'
            'USE + TO CHECK TOTALS.\n'
            'FREQUENCIES: 4,6,3.\tCUMULATIVE:\t4\t4+6=10\t10+3=13.\n'
            'DO NOT START OVER EACH ROW.\tYOU KEEP ALL PREVIOUS\tFREQUENCIES.\n'
            'F01 FREQUENCY\tF02 REL FREQ\n'
            'FREQUENCY_SESSION'
            , field)
    if gid == 'F04':
        return STCORE.unpack_guide(
            'Sample Proportion / Percent\n'
            'TYPICAL START:\t"WHAT PROPORTION OF\tSTUDENTS..."\t"WHAT PERCENT..."\t"HOW MANY OUT OF THE SAMPLE"\n'
            'PART = COUNT MEETING CONDITION.\tWHOLE = TOTAL SAMPLE SIZE.\t\tPROPORTION=PART/WHOLE.\tPERCENT=PROPORTION*100.\n'
            '1. COUNT WHO MEET CONDITION.\t2. FIND TOTAL n.\t3. DIVIDE PART/n.\t4. *100 IF PERCENT.\n'
            'TYPE PART/n ENTER.\tOR USE REL FREQ SOLVER.\n'
            'COMMUTE GROUP:\t22 OF 80 >10 MILES.\t22/80=.275\t=27.5%.\n'
            'THIS IS DESCRIBING OBSERVED\tDATA, NOT AUTOMATICALLY\tA BINOMIAL PROBABILITY.\n'
            'F02 REL FREQ\tP01 BASIC PROB\n'
            'REL_FREQ'
            , field)
    if gid == 'S01':
        return STCORE.unpack_guide(
            'Mean from Raw Data\n'
            'TYPICAL START:\t"FOR THE DATA SHOWN, FIND\tTHE MEAN..."\t"FIND x-bar..."\t\tYOU SEE A LIST/COLUMN\tOF NUMBERS.\n'
            'x values = RAW DATA.\tn = NUMBER OF VALUES.\t\txbar = SAMPLE MEAN.\n'
            'BY HAND:\t1. ADD ALL x VALUES.\t2. COUNT VALUES n.\t3. xbar=SUM(x)/n.\t\tFOR LONG LIST, USE EVO.\n'
            'STAT > EDIT.\tENTER DATA IN L1.\tSTAT > CALC.\t1-VAR STATS.\tLIST=L1.\tREAD xbar.\n'
            'COMMUTE DATA:\t16 VALUES.\t1-VAR STATS GAVE\txbar=11.5625.\n'
            'DO NOT USE MEDIAN.\tDO NOT DIVIDE BY WRONG n.\tCLEAR OLD L1 DATA FIRST.\n'
            'S02 MEDIAN\tS09 SD\tS05 FIVE NUMBER\tF05 MEAN WITH FREQUENCIES\n'
            ''
            , field)
    if gid == 'S02':
        return STCORE.unpack_guide(
            'Median / Half\n'
            'TYPICAL START:\t"FIND THE MEDIAN."\t"HALF OF STUDENTS TRAVEL\tUNDER WHAT DISTANCE?"\t"50TH PERCENTILE"\n'
            'MEDIAN = MIDDLE OF\tORDERED DATA.\t\tEVEN n:\tAVERAGE TWO MIDDLE VALUES.\n'
            '1. ORDER LOW TO HIGH.\t2. FIND MIDDLE.\t3. IF TWO MIDDLE VALUES,\t   ADD THEM /2.\n'
            '1-VAR STATS.\tREAD Med.\n'
            'COMMUTE n=16.\tMIDDLE VALUES 10 AND 11.\t(10+11)/2=10.5.\n'
            'MEDIAN IS NOT 50% OF MAX.\tIT IS A POSITION IN\tORDERED DATA.\n'
            'S06 Q1\tS07 Q3\tS01 MEAN\tF06 MEDIAN WITH FREQUENCIES\n'
            ''
            , field)
    if gid == 'S03':
        return STCORE.unpack_guide(
            'Mode\n'
            'TYPICAL START:\t"FIND THE MODE."\t"MOST FREQUENT VALUE."\n'
            'MODE = VALUE OCCURRING\tMOST OFTEN.\t\tTHERE CAN BE MULTIPLE MODES\tOR NO MODE.\n'
            '1. COUNT EACH VALUE.\t2. FIND HIGHEST COUNT.\t3. REPORT VALUE(S),\t   NOT THE COUNT.\n'
            'NO SPECIAL CMD NEEDED.\n'
            '2,3,3,4,5\t3 OCCURS MOST.\tMODE=3.\n'
            'DO NOT REPORT FREQUENCY\tAS MODE.\tMODE IS THE VALUE.\n'
            'F01 FREQUENCY\tS01 MEAN\tS02 MEDIAN\tF07 MODE WITH FREQUENCIES\n'
            ''
            , field)
    if gid == 'S04':
        return STCORE.unpack_guide(
            'Range\n'
            'TYPICAL START:\t"FIND THE RANGE."\tNEEDS MINIMUM AND MAXIMUM.\n'
            'MIN = SMALLEST VALUE.\tMAX = LARGEST VALUE.\t\tRANGE=MAX-MIN.\n'
            '1. FIND MAX.\t2. FIND MIN.\t3. SUBTRACT MIN FROM MAX.\n'
            '1-VAR STATS GIVES\tminX AND maxX.\n'
            'COMMUTE DATA:\tMAX=29, MIN=2.\tRANGE=27.\n'
            'Q3-Q1 IS IQR,\tNOT RANGE.\n'
            'S08 IQR\tS05 FIVE NUMBER\n'
            'RANGE_IQR'
            , field)
    if gid == 'S05':
        return STCORE.unpack_guide(
            'Five-Number Summary\n'
            'TYPICAL START:\t"FIND THE FIVE-NUMBER\tSUMMARY."\tOR NEEDS VALUES FOR BOXPLOT.\n'
            'FIVE VALUES:\tMIN\tQ1\tMEDIAN\tQ3\tMAX\n'
            'BY HAND REQUIRES ORDERING\tDATA AND FINDING QUARTILES.\tON TEST, EVO IS FASTER.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tSCROLL TO:\tminX,Q1,Med,Q3,maxX.\n'
            'COMMUTE:\t2, 5.5, 10.5, 16.5, 29.\n'
            'DO NOT INCLUDE MEAN.\tFIVE-NUMBER SUMMARY DOES\tNOT CONTAIN xbar.\n'
            'S06 Q1\tS07 Q3\tG01 BOXPLOT\n'
            ''
            , field)
    if gid == 'S06':
        return STCORE.unpack_guide(
            'First Quartile Q1\n'
            'TYPICAL START:\t"UNDER WHAT DISTANCE DO\tTHE SHORTEST 25%..."\t"FIND Q1."\t"25TH PERCENTILE."\n'
            'Q1 = FIRST QUARTILE.\tIT MARKS ABOUT LOWEST 25%.\t\t25% -> Q1.\t50% -> MEDIAN.\t75% -> Q3.\n'
            '1. RECOGNIZE 25% -> Q1.\t2. ENTER RAW DATA IF GIVEN.\t3. RUN 1-VAR STATS.\t4. READ Q1.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tREAD Q1.\n'
            'COMMUTE QUESTION:\t"UNDER WHAT DISTANCE DO\tSHORTEST 25% TRAVEL?"\tQ1=5.5 MILES.\n'
            'WRONG: .25*MAX.\tQ1 IS A LOCATION IN\tORDERED DATA.\n'
            'S02 MEDIAN\tS07 Q3\tS08 IQR\n'
            ''
            , field)
    if gid == 'S07':
        return STCORE.unpack_guide(
            'Third Quartile Q3\n'
            'TYPICAL START:\t"FIND Q3."\t"75TH PERCENTILE."\t"75% ARE BELOW WHAT VALUE?"\n'
            'Q3 = THIRD QUARTILE.\tABOUT 75% OF DATA IS\tAT OR BELOW THIS REGION.\n'
            '1. RECOGNIZE 75% -> Q3.\t2. ENTER DATA L1.\t3. RUN 1-VAR STATS.\t4. READ Q3.\n'
            'STAT > EDIT -> L1.\t1-VAR STATS -> Q3.\n'
            'COMMUTE Q3=16.5.\n'
            'WRONG: .75*MAX.\tQ3 IS A DATA POSITION.\n'
            'S06 Q1\tS08 IQR\n'
            ''
            , field)
    if gid == 'S08':
        return STCORE.unpack_guide(
            'Interquartile Range IQR\n'
            'TYPICAL START:\t"FIND THE IQR."\t"INTERQUARTILE RANGE."\t"SPREAD OF MIDDLE 50%."\n'
            'YOU NEED Q1 AND Q3.\t\tIQR=Q3-Q1.\n'
            '1. FIND Q1.\t2. FIND Q3.\t3. SUBTRACT Q1 FROM Q3.\n'
            '1-VAR STATS FOR Q1,Q3.\tTHEN TYPE Q3-Q1.\n'
            'COMMUTE:\t16.5-5.5=11.\n'
            'MAX-MIN IS RANGE.\tQ3-Q1 IS IQR.\n'
            'S04 RANGE\tG03 OUTLIERS\n'
            'RANGE_IQR'
            , field)
    if gid == 'S09':
        return STCORE.unpack_guide(
            'Sample Standard Deviation\n'
            'TYPICAL START:\t"FIND THE SAMPLE STANDARD\tDEVIATION."\t"FIND s."\n'
            'ON EVO:\tSx = SAMPLE SD.\tsigma-x = POPULATION SD.\t\tIF DATA IS A SAMPLE,\tREPORT Sx.\n'
            'BY-HAND FORMULA USES n-1,\tBUT FOR LONG RAW DATA\tUSE 1-VAR STATS.\n'
            'STAT > EDIT -> L1.\tSTAT > CALC -> 1-VAR STATS.\tREAD Sx.\n'
            'COMMUTE SAMPLE:\tSx ABOUT 7.6243.\n'
            'COMMON ERROR:\tREPORTING sigma-x FOR\tA SAMPLE.\n'
            'S01 MEAN\tS12 Z-SCORE\n'
            ''
            , field)
    if gid == 'S10':
        return STCORE.unpack_guide(
            'Maximum Usual Value\n'
            'TYPICAL START:\t"CALCULATE THE MAXIMUM\tUSUAL VALUE = MEAN +\t2*(STANDARD DEVIATION)."\n'
            'NEED:\tMEAN\tSTANDARD DEVIATION\t\tFORMULA:\tMEAN+2(SD).\n'
            '1. GET MEAN.\t2. GET SD.\t3. MULTIPLY SD BY 2.\t4. ADD TO MEAN.\t5. VALUES ABOVE ARE\t   OFTEN STAT HIGH.\n'
            'GET xbar AND Sx USING\t1-VAR STATS IF NEEDED.\tTHEN TYPE xbar+2*Sx.\n'
            'COMMUTE:\t11.5625+2(7.6243)\tABOUT 26.81.\t29 > 26.81.\n'
            'WRONG: MEAN+SD+2.\tWRONG: 2*MEAN+SD.\n'
            'S11 MIN USUAL\tS12 Z-SCORE\n'
            'USUAL'
            , field)
    if gid == 'S11':
        return STCORE.unpack_guide(
            'Minimum Usual Value\n'
            'TYPICAL START:\t"MINIMUM USUAL VALUE"\tOR MEAN-2(SD).\n'
            'NEED MEAN AND SD.\t\tFORMULA:\tMEAN-2(SD).\n'
            '1. GET MEAN.\t2. GET SD.\t3. COMPUTE 2*SD.\t4. SUBTRACT FROM MEAN.\n'
            '1-VAR STATS FOR xbar,Sx.\tTHEN xbar-2*Sx.\n'
            'MEAN=20, SD=3:\t20-2(3)=14.\n'
            'SUBTRACT WHOLE 2*SD.\tUSE PARENTHESES.\n'
            'S10 MAX USUAL\tS12 Z-SCORE\n'
            'USUAL'
            , field)
    if gid == 'S12':
        return STCORE.unpack_guide(
            'Z-Score\n'
            'TYPICAL START:\t"FIND THE z-SCORE."\t"ARE ANY VALUES\tSTATISTICALLY HIGH?"\t"HOW MANY SDs FROM MEAN?"\n'
            'NEED:\tx = VALUE BEING CHECKED.\tMEAN = CENTER.\tSD = STANDARD DEVIATION.\t\tz=(x-MEAN)/SD.\n'
            '1. IDENTIFY x.\t2. IDENTIFY MEAN.\t3. IDENTIFY SD.\t4. COMPUTE x-MEAN.\t5. DIVIDE BY SD.\t6. z>2 OFTEN HIGH.\t   z<-2 OFTEN LOW.\n'
            'TYPE (x-mean)/sd.\tPARENTHESES MATTER.\tOR USE SOLVER.\n'
            'COMMUTE x=29:\t(29-11.5625)/7.6243\tABOUT 2.29.\tSTATISTICALLY HIGH.\n'
            'WRONG: x-mean/sd.\tWITHOUT PARENTHESES\tORDER OF OPERATIONS\tCHANGES ANSWER.\n'
            'S10/S11 USUAL VALUES\n'
            'ZSCORE'
            , field)
    if gid == 'G01':
        return STCORE.unpack_guide(
            'Right vs Left Skew\n'
            'TYPICAL START:\t"DESCRIBE THE BOXPLOT."\t"IS DATA SKEWED?"\t"LEFT, RIGHT, OR NORMAL?"\n'
            'LOOK AT TAIL.\t\tLONG TAIL RIGHT\t-> RIGHT SKEW.\t\tLONG TAIL LEFT\t-> LEFT SKEW.\n'
            '1. FIND BULK OF DATA.\t2. FIND SIDE THAT STRETCHES\t   FARTHER.\t3. NAME SKEW BY THAT TAIL.\n'
            'GRAPH WITH STAT PLOT.\tBOXPLOT OR HISTOGRAM.\tZOOMSTAT TO FIT.\n'
            'COMMUTE DATA HAD A LONGER\tHIGH-DISTANCE TAIL.\t-> RIGHT-SKEWED.\n'
            'DO NOT NAME SKEW BY\tWHERE THE BOX/BULK SITS.\tNAME IT BY TAIL.\n'
            'G02 NORMAL\tG03 OUTLIERS\n'
            ''
            , field)
    if gid == 'G02':
        return STCORE.unpack_guide(
            'Does Data Look Normal?\n'
            'TYPICAL START:\t"DOES THE DATA APPEAR TO\tCOME FROM A NORMALLY\tDISTRIBUTED POPULATION? WHY?"\n'
            'LOOK FOR:\tROUGH SYMMETRY,\tBELL SHAPE,\tNO STRONG OUTLIERS,\tNO STRONG SKEW.\n'
            '1. LOOK AT HISTOGRAM.\t2. CHECK SYMMETRY.\t3. CHECK TAILS.\t4. CHECK OUTLIERS.\t5. EXPLAIN USING GRAPH.\n'
            'MAKE HISTOGRAM/BOXPLOT.\tCALCULATOR SHOWS GRAPH;\tYOU MUST INTERPRET.\n'
            'A CLEAR RIGHT-SKEWED\tCOMMUTE GRAPH IS NOT\tVERY NORMAL-LOOKING.\n'
            'DO NOT SAY NORMAL JUST\tBECAUSE A MEAN AND SD\tCAN BE CALCULATED.\n'
            'G01 SKEW\tG03 OUTLIERS\n'
            ''
            , field)
    if gid == 'G03':
        return STCORE.unpack_guide(
            'Outlier Fences\n'
            'TYPICAL START:\t"ARE THERE OUTLIERS?"\t"USE THE 1.5 IQR RULE."\t"FIND LOWER/UPPER FENCE."\n'
            'NEED Q1 AND Q3.\tIQR=Q3-Q1.\t\tLOW=Q1-1.5(IQR).\tHIGH=Q3+1.5(IQR).\n'
            '1. FIND Q1,Q3.\t2. COMPUTE IQR.\t3. COMPUTE LOW FENCE.\t4. COMPUTE HIGH FENCE.\t5. VALUES OUTSIDE ARE\t   POTENTIAL OUTLIERS.\n'
            '1-VAR STATS FOR Q1,Q3.\tTHEN USE SOLVER OR\tTYPE FENCE FORMULAS.\n'
            'Q1=10,Q3=18.\tIQR=8.\tLOW=-2.\tHIGH=30.\n'
            'FENCES ARE CUTPOINTS,\tNOT NECESSARILY ACTUAL\tDATA VALUES.\n'
            'S08 IQR\tG01 BOXPLOT\n'
            'OUTLIER'
            , field)
    if gid == 'F05':
        return STCORE.unpack_guide(
            'Mean from Frequency Table\n'
            'VALUES + FREQUENCY; MEAN\tQ001 DELIVERIES: FREQUENCY MEAN\n'
            'x=DATA VALUE\tf=HOW OFTEN IT OCCURS\tn=SUM(f), NOT NUMBER OF ROWS\tWEIGHTED TOTAL=SUM(x*f)\n'
            'SUM(x*f)/SUM(f)\n'
            '1-VAR STATS: DATA LIST L1\tFREQUENCY LIST L2\tL1: VALUES, L2: COUNTS\tREAD xbar; LABELS MAY VARY\n'
            '3,6,9,12; f=1,2,6,5: 9.2143\tQ001: 129/14=9.2143; n=14\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)
    if gid == 'F06':
        return STCORE.unpack_guide(
            'Median from Frequency Table\n'
            'FREQUENCY TABLE; MEDIAN\tQ002 RAIN: MEDIAN AND MODE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ORDER VALUES LOW TO HIGH\tn=SUM(FREQUENCIES)\tODD: POSITION (n+1)/2\tEVEN: n/2 AND n/2+1\tLOCATE VIA CUMULATIVE f\tAVERAGE THOSE TWO VALUES\n'
            'USE ENTER VALUES / SOLVE\n'
            'n=20: POS 10 AND 11 BOTH 7\tQ002: n=20; positions 10,11=7; mode=7\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)
    if gid == 'F07':
        return STCORE.unpack_guide(
            'Mode from Frequency Table\n'
            'FREQUENCY TABLE; MODE\tQ002 RAIN: MEDIAN AND MODE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'VALUE WITH GREATEST COUNT\n'
            'USE ENTER VALUES / SOLVE\n'
            '6 HAS f=5; 7 HAS f=6: MODE 7\tQ002: n=20; positions 10,11=7; mode=7\n'
            'REPORT VALUE, NOT FREQUENCY\tCOMBINE REPEATED VALUE ROWS\tIGNORE ZERO FREQUENCIES\tASSIGNMENT: >2 MODES -> DNE\tALL EQUAL COUNTS -> NO MODE\tONE DISTINCT VALUE: ITS MODE\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'FREQUENCY_SESSION'
            , field)
    raise KeyError(gid)
