# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STGNEW3 guide records.
import STCORE


def get_guide(gid, field=None):
    if gid == 'G06':
        return STCORE.unpack_guide('Histogram Builder\nHISTOGRAM BARS OR CLASSES\nRAW VALUES, FREQUENCIES, OR P(X)\nCHOOSE CLASSES; COUNT EACH OBSERVATION ONCE\nSTAT PLOT HISTOGRAM\n0,1,2,3: WIDTH 2 GIVES COUNTS 2,2\nLABEL WHETHER HEIGHT IS COUNT OR PROBABILITY\nF08 G05\nG06', field)

    if gid == 'G07':
        return STCORE.unpack_guide('Normal Curve Axes\nLABEL BELL CURVE WITH x AND z\nx=MEAN+z*SD; z=(x-MEAN)/SD\nLABEL z=-3 THROUGH 3; MAP EACH TO x\nCALCULATE x=MEAN+z*SD\nMEAN 40 SD 4: z=1 IS x=44\nNEED MEAN AND SD; NORMALITY NOT PROVED BY LABELS\nS12 G08 G09\nG07', field)

    if gid == 'G08':
        return STCORE.unpack_guide('Empirical Rule\n68 95 99.7; BELL SHAPED\nWITHIN 1,2,3 SD: 68%,95%,99.7%\nOUTSIDE=100-WITHIN; ONE TAIL=OUTSIDE/2\nUSE PERCENT ARITHMETIC\nBEYOND +2 SD ABOUT 2.5%\nAPPROXIMATE; REQUIRES NORMAL/BELL SHAPE\nG07 S10\nG08', field)
    return None
