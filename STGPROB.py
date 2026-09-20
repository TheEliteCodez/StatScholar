# Author: TheEliteCodez
# STGPROB - compact guide records; only the selected record is decoded.
import STCORE

def get_guide(gid, field=None):
    if gid == 'P01':
        return STCORE.unpack_guide(
            'Basic Probability\n'
            'TYPICAL START:\t"FIND THE PROBABILITY..."\tAND YOU CAN COUNT\tFAVORABLE / TOTAL\tEQUALLY LIKELY OUTCOMES.\tQ003 ROULETTE 0 AND 00\tQ008 52-CARD DECK\tQ012 SPINNER EVEN\n'
            'NEED:\tFAVORABLE OUTCOMES.\tTOTAL OUTCOMES.\t\tP(E)=FAVORABLE/TOTAL.\n'
            '1. DEFINE EVENT E.\t2. COUNT FAVORABLE.\t3. COUNT TOTAL.\t4. DIVIDE.\t5. REDUCE IF ASKED.\n'
            'TYPE favorable/total.\tSOLVER SHOWS REDUCED\tFRACTION, DECIMAL, PERCENT.\n'
            'TWO DICE SUM=6:\t5 FAVORABLE.\t36 TOTAL.\tP=5/36.\tROULETTE 0,00,1..36:\tP(1)=1/38; P(ODD)=18/38\tCARDS: P(4S)=1/52\tACE OR 2: 8/52\tQ003: 38 spaces; single=1/38; odd=9/19\tQ008: 4S=.0192; S OR D=.5000; ace or 2=.1538\tQ012: 6/12=.5000 IF equal sectors 1..12\n'
            'DO NOT REVERSE FRACTION.\tONLY USE COUNT/TOTAL\tWHEN OUTCOMES ARE\tEQUALLY LIKELY.\n'
            'P02 COMPLEMENT\tP04 OR\tP05 AND\n'
            'BASIC_PROB'
            , field)
    if gid == 'P02':
        return STCORE.unpack_guide(
            'Complement / NOT\n'
            'TYPICAL START:\t"PROBABILITY THAT IT IS NOT..."\t"DOES NOT..."\t"NONE..."\tQ013 SURVEY NOT BELIEVING\n'
            'NEED P(E) OR PROBABILITY\tOF OPPOSITE EVENT.\t\tP(NOT E)=1-P(E).\n'
            '1. IDENTIFY ORIGINAL EVENT.\t2. FIND P(E).\t3. SUBTRACT FROM 1.\n'
            'TYPE 1-P(E).\tSOLVER ACCEPTS .18,\t18%, OR 18/100.\n'
            'P(WRONG PD)=.18.\tP(NOT WRONG PD)\t=1-.18=.82.\tQ013: 448/678=.6608\n'
            'USE 1 FOR PROBABILITY\tDECIMALS, OR 100%\tONLY IF WORKING ENTIRELY\tIN PERCENT.\n'
            'P09 AT LEAST ONE\tP01 BASIC\n'
            'COMPLEMENT'
            , field)
    if gid == 'P03':
        return STCORE.unpack_guide(
            'OR: Mutually Exclusive\n'
            'TYPICAL START:\t"E AND F ARE MUTUALLY\tEXCLUSIVE EVENTS."\t"FIND P(E OR F)."\n'
            'MUTUALLY EXCLUSIVE =\tCANNOT BOTH HAPPEN.\t\tP(E AND F)=0.\n'
            '1. SEE MUTUALLY EXCLUSIVE.\t2. KNOW OVERLAP=0.\t3. ADD P(E)+P(F).\n'
            'TYPE P(E)+P(F).\tOR USE MUT EXCL SOLVER.\n'
            'P(E)=.31, P(F)=.22.\tP(E OR F)=.53.\n'
            'MUTUALLY EXCLUSIVE IS\tNOT THE SAME AS\tINDEPENDENT.\n'
            'P04 GENERAL OR\tP05 INDEPENDENT\n'
            'MUT_OR'
            , field)
    if gid == 'P04':
        return STCORE.unpack_guide(
            'OR: General Addition Rule\n'
            'TYPICAL START:\t"FIND P(A OR B)."\tAND EVENTS CAN OVERLAP.\tMAY GIVE P(A AND B).\n'
            'NEED:\tP(A), P(B),\tP(A AND B).\t\tP(A OR B)=\tP(A)+P(B)-P(A AND B).\n'
            '1. FIND A.\t2. FIND B.\t3. FIND OVERLAP BOTH.\t4. ADD A+B.\t5. SUBTRACT BOTH ONCE.\n'
            'TYPE A+B-BOTH.\tOR USE GENERAL OR SOLVER.\n'
            'DICE:\tSUM=6 ->5/36.\tFIRST DIE=2 ->6/36.\tOVERLAP (2,4)->1/36.\tOR=10/36=5/18.\n'
            'ASK: CAN BOTH HAPPEN?\tIF YES, DO NOT JUST ADD.\n'
            'P03 MUT EXCLUSIVE\tP05 AND\n'
            'GENERAL_OR'
            , field)
    if gid == 'P05':
        return STCORE.unpack_guide(
            'AND: Independent\n'
            'TYPICAL START:\t"A AND B" OR "BOTH"\tAND EVENTS ARE INDEPENDENT.\n'
            'NEED P(A), P(B).\t\tINDEPENDENT MEANS\tONE DOES NOT CHANGE\tPROBABILITY OF OTHER.\t\tP(A AND B)=P(A)*P(B).\n'
            '1. FIND P(A).\t2. FIND P(B).\t3. CONFIRM INDEPENDENT.\t4. MULTIPLY.\n'
            'TYPE A*B.\tOR INDEP AND SOLVER.\n'
            'TWO DICE BOTH EVEN:\t(3/6)*(3/6)\t=9/36=1/4.\n'
            'AND DOES NOT MEAN ADD.\tDO NOT ASSUME INDEPENDENT\tIF QUESTION CHANGES\tPROBABILITY AFTER FIRST.\n'
            'P06 GENERAL AND\tP07 GIVEN\n'
            'INDEP_AND'
            , field)
    if gid == 'P06':
        return STCORE.unpack_guide(
            'AND: General Rule\n'
            'TYPICAL START:\t"A AND B"\tBUT SECOND EVENT DEPENDS\tON FIRST, OR P(B|A) GIVEN.\n'
            'NEED:\tP(A)\tP(B|A)\t\tP(A AND B)=\tP(A)*P(B|A).\n'
            '1. FIND P(A).\t2. FIND P(B GIVEN A).\t3. MULTIPLY.\n'
            'TYPE P(A)*P(B|A).\tOR GENERAL AND SOLVER.\n'
            'WITHOUT REPLACEMENT:\tSECOND DRAW OFTEN HAS\tDIFFERENT PROBABILITY.\n'
            'DO NOT USE P(A)*P(B)\tIF FIRST EVENT CHANGES\tSECOND EVENT.\n'
            'P05 INDEP AND\tP07 GIVEN\n'
            'GENERAL_AND'
            , field)
    if gid == 'P07':
        return STCORE.unpack_guide(
            'Conditional Probability / GIVEN\n'
            'TYPICAL START:\t"FIND P(E|F)."\t"PROBABILITY OF E GIVEN F."\t"AMONG THOSE WHO ARE F..."\t\tTHE | SYMBOL MEANS GIVEN.\n'
            'IF P(A|B):\tA = EVENT YOU WANT.\tB = EVENT YOU ALREADY KNOW.\tA AND B = OVERLAP.\t\tFORMULA:\tP(A|B)=P(A AND B)/P(B).\n'
            '1. READ A|B AS A GIVEN B.\t2. EVENT AFTER | IS B.\t3. FIND OVERLAP A AND B.\t4. FIND TOTAL PROB OF B.\t5. DIVIDE BOTH/B.\t\tWITH COUNTS:\t# BOTH / # B.\n'
            'IF PROBS GIVEN:\tTYPE BOTH/B.\t\tIF TABLE COUNTS:\tDIVIDE BOTH-CELL COUNT\tBY TOTAL COUNT FOR B.\n'
            'P(E AND F)=.18.\tP(F)=.42.\tP(E|F)=.18/.42\t=.428571...\t=42.86%.\n'
            'WRONG: P(E)/P(F).\tNUMERATOR MUST BE BOTH.\t\tWRONG: P(E)+P(F).\tTHAT IS NOT GIVEN.\t\tMEMORY:\tAFTER | = DENOMINATOR.\n'
            'P04 OR\tP06 AND\tINDEPENDENCE\n'
            'CONDITIONAL'
            , field)
    if gid == 'P08':
        return STCORE.unpack_guide(
            'Venn / Survey A OR B\n'
            'TYPICAL START:\t"IN A SURVEY OF ..."\t"... SAID A, ... SAID B,\tAND ... SAID BOTH."\n'
            'VALUES:\t#A\t#B\t#BOTH\tTOTAL n IF PROBABILITY\tOR NEITHER IS ASKED.\n'
            '1. ADD #A + #B.\t2. SUBTRACT #BOTH ONCE.\t3. RESULT = #(A OR B).\t4. DIVIDE BY n IF\t   PROBABILITY ASKED.\n'
            'BASIC +,-,/.\tGENERAL OR SOLVER CAN\tALSO BE USED WITH\tPROPORTIONS.\n'
            '184 COMPOST.\t238 RECYCLE.\t123 BOTH.\tA OR B:\t184+238-123=299.\n'
            'DO NOT COUNT BOTH TWICE.\tFOR NEITHER:\tTOTAL-(A OR B).\n'
            'P04 GENERAL OR\tP02 COMPLEMENT\n'
            ''
            , field)
    if gid == 'P09':
        return STCORE.unpack_guide(
            'At Least One\n'
            'TYPICAL START:\t"WHAT IS THE PROBABILITY\tTHAT AT LEAST ONE..."\n'
            'AT LEAST ONE = 1 OR MORE.\tOPPOSITE EVENT = NONE.\t\tIF EACH TRIAL SUCCESS p:\tFAIL=1-p.\tP(NONE)=(1-p)^n.\n'
            '1. FIND p SUCCESS.\t2. FIND 1-p FAILURE.\t3. RAISE FAILURE TO n.\t4. SUBTRACT FROM 1.\n'
            'TYPE 1-(1-p)^n.\tOR USE SOLVER.\n'
            '5 DICE, AT LEAST ONE 3:\tp=1/6.\tP=1-(5/6)^5.\n'
            "DO NOT CONFUSE WITH\tBINOMIAL 'AT LEAST x'.\tTHIS SPECIAL CASE IS\tAT LEAST ONE.\n"
            'P02 COMPLEMENT\tB05 AT LEAST x\n'
            'AT_LEAST_ONE'
            , field)
    if gid == 'P10':
        return STCORE.unpack_guide(
            'Test Mutually Exclusive\n'
            'CAN THESE OCCUR TOGETHER?\tQ016 DOG / CAT / BOTH\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'EXCLUSIVE IF P(BOTH)=0\n'
            'USE ENTER VALUES / SOLVE\n'
            'BOTH=.46: NOT EXCLUSIVE\tQ016: .6000,.4300,.8000,.6825 (dog GIVEN cat)\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SUPPLIED_SESSION'
            , field)
    if gid == 'P11':
        return STCORE.unpack_guide(
            'Test Independence\n'
            'ARE EVENTS INDEPENDENT?\tQ017 COMPOST / RECYCLE\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'P(BOTH)=P(A)*P(B)\n'
            'USE ENTER VALUES / SOLVE\n'
            '.57*.69=.3933, NOT .46: NO\tQ017: .5700,.4600,.8000,.6667; exclusive NO; independent NO\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'SUPPLIED_SESSION'
            , field)
    if gid == 'P12':
        return STCORE.unpack_guide(
            'Direct Intersection Counts\n'
            'AND / BOTH FROM COUNTS\tQ010 BOTH INTOXICATED\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'BOTH CELL / WHOLE TOTAL\n'
            'USE ENTER VALUES / SOLVE\n'
            '61/979=0.0623\tQ010: 61/979=.0623; whole total, not given group\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'TWO_WAY_SESSION'
            , field)
    if gid == 'P13':
        return STCORE.unpack_guide(
            'Valid Probability Value\n'
            'CAN THIS BE A PROBABILITY?\tQ007 VALID PROBABILITY?\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            '0<=p<=1\n'
            'USE ENTER VALUES / SOLVE\n'
            '0 AND 1 VALID; 1.2 INVALID\tQ007: Missing value; valid iff 0<=p<=1\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'VALID_PROBABILITY'
            , field)
    if gid == 'P14':
        return STCORE.unpack_guide(
            'Two-Way Table Events\n'
            'ROW/COLUMN TABLE; ONE EVENT\tQ009 GRADE TABLE: MALE\tQ014 GRADES NOT B\tQ015 MEDIUM CONCERN\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'ROW OR COLUMN / GRAND TOTAL\n'
            'USE ENTER VALUES / SOLVE\n'
            'MALE 36 / ALL 81 = 4/9\tQ009: 36/81=.4444\tQ014: 41/62=.6613\tQ015: 21/65=.3231\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'TWO_WAY_SESSION'
            , field)
    raise KeyError(gid)
