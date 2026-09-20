# Author: Gregory King
# STGDICE - compact guide records; only the selected record is decoded.
import STCORE

def get_guide(gid, field=None):
    if gid == 'C02':
        return STCORE.unpack_guide(
            'Dice Sample Space\n'
            'TYPICAL START:\t"YOU ROLL TWO FAIR DICE."\t"HOW MANY EQUALLY LIKELY\tOUTCOMES?"\t"ROLL 5 DICE..."\n'
            'EACH SIX-SIDED DIE HAS\t6 POSSIBLE RESULTS.\t\tk DICE -> 6^k.\n'
            '1. COUNT DICE k.\t2. COMPUTE 6^k.\n'
            'TYPE 6^k ENTER.\tOR DICE SOLVER.\n'
            '2 DICE: 6^2=36.\t3 DICE: 216.\t5 DICE: 7776.\n'
            'WRONG: 6*k.\tOUTCOMES MULTIPLY.\n'
            'C01 MULTIPLICATION\tP01 BASIC PROB\n'
            'DICE_SPACE'
            , field)
    if gid == 'C07':
        return STCORE.unpack_guide(
            'Multiple-Dice Event Helper\n'
            'ROLL 3, 4, 5, 6 OR MORE DICE.\tASKS A SUM, FACE COUNT,\tPARITY OR MATCHING RESULTS.\n'
            'n = NUMBER OF DICE.\tFAIR, INDEPENDENT, SIX-SIDED.\tTOTAL ORDERED OUTCOMES=6^n.\n'
            'SUM: COUNT ORDERED RESULTS.\tAT LEAST ONE: 1-(5/6)^n.\tEXACTLY r: nCr*5^(n-r)/6^n.\tALL EVEN OR ODD: (1/2)^n.\tALL SAME: 6/6^n.\n'
            'OPEN THE DIRECT SOLVER.\tENTER DICE AND EVENT.\tSUM COUNTS USE FREQUENCIES.\n'
            '5 DICE, AT LEAST ONE 3:\t1-(5/6)^5=4651/7776.\t3 DICE, SUM=6: 10/216.\t4 DICE, ALL EVEN: 1/16.\n'
            'SUMS ARE NOT EQUALLY LIKELY.\tCOUNT ORDERED OUTCOMES.\tALL SAME ALLOWS ANY FACE.\tALL=3 ALLOWS ONLY FACE 3.\n'
            'C02 DICE OUTCOMES\tP09 AT LEAST ONE\tB02 EXACTLY x\n'
            'MULTI_DICE'
            , field)
    if gid == 'C05':
        return STCORE.unpack_guide(
            'List Sample Space\n'
            'DIE THEN COIN; LIST OUTCOMES\tQ004 DIE THEN COIN\n'
            'ENTER THE NUMBERS ON YOUR PAGE\n'
            'PAIR EACH DIE VALUE WITH H,T\n'
            'USE ENTER VALUES / SOLVE\n'
            '6-SIDED DIE + COIN: 12 OUTCOMES\tQ004: 12 outcomes; H=1/2; 6=1/6; 3 OR H=7/12; 6T=1/12\n'
            'KEEP FULL PRECISION UNTIL END\n'
            'TYPE Q001-Q049 FOR EXAMPLES\n'
            'COIN_SESSION'
            , field)
    raise KeyError(gid)
