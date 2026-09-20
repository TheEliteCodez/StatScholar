# Guide metadata loaded only for a requested lookup.
GUIDES = {'D01': ('Qualitative vs Quantitative', ''), 'D02': ('Discrete vs Continuous', ''), 'D03': ('Population vs Sample', ''), 'D04': ('Parameter vs Statistic', ''), 'F01': ('Frequency', 'FREQUENCY_SESSION'), 'F02': ('Relative Frequency', 'CATEGORY_SESSION'), 'F03': ('Cumulative Frequency', 'FREQUENCY_SESSION'), 'F04': ('Sample Proportion / Percent', 'REL_FREQ'), 'S01': ('Mean from Raw Data', ''), 'S02': ('Median / Half', ''), 'S03': ('Mode', ''), 'S04': ('Range', 'RANGE_IQR'), 'S05': ('Five-Number Summary', ''), 'S06': ('First Quartile Q1', ''), 'S07': ('Third Quartile Q3', ''), 'S08': ('Interquartile Range IQR', 'RANGE_IQR'), 'S09': ('Sample Standard Deviation', ''), 'S10': ('Maximum Usual Value', 'USUAL'), 'S11': ('Minimum Usual Value', 'USUAL'), 'S12': ('Z-Score', 'ZSCORE'), 'G01': ('Right vs Left Skew', ''), 'G02': ('Does Data Look Normal?', ''), 'G03': ('Outlier Fences', 'OUTLIER'), 'P01': ('Basic Probability', 'BASIC_PROB'), 'P02': ('Complement / NOT', 'COMPLEMENT'), 'P03': ('OR: Mutually Exclusive', 'MUT_OR'), 'P04': ('OR: General Addition Rule', 'GENERAL_OR'), 'P05': ('AND: Independent', 'INDEP_AND'), 'P06': ('AND: General Rule', 'GENERAL_AND'), 'P07': ('Conditional Probability / GIVEN', 'CONDITIONAL'), 'P08': ('Venn / Survey A OR B', ''), 'P09': ('At Least One', 'AT_LEAST_ONE'), 'C02': ('Dice Sample Space', 'DICE_SPACE'), 'C07': ('Multiple-Dice Event Helper', 'MULTI_DICE'), 'B01': ('Identify a Binomial Problem', 'BINOMIAL_CONDITIONS'), 'B02': ('Binomial Exactly x', 'BINOMIAL_SESSION'), 'B03': ('Binomial At Most x', 'BINOMIAL_SESSION'), 'B04': ('Binomial Less Than x', 'BINOMIAL_SESSION'), 'B05': ('Binomial At Least x', 'BINOMIAL_SESSION'), 'B06': ('Binomial More Than x', 'BINOMIAL_SESSION'), 'B07': ('Binomial Formula Printed', 'BIN_EXACT'), 'B08': ('Binomial Mean', 'BINOMIAL_SESSION'), 'B09': ('Binomial Variance / SD', 'BINOMIAL_SESSION'), 'B10': ('Binomial Between a and b', 'BINOMIAL_SESSION'), 'C01': ('Multiplication Principle', 'SAMPLE_SPACE'), 'C03': ('Combination nCr', 'NCR'), 'C04': ('Permutation nPr', 'NPR'), 'R01': ('Valid Probability Distribution', ''), 'R02': ('Expected Value E(X)', 'DISTRIBUTION_SESSION'), 'R03': ('Variance / SD of Distribution', 'DISTRIBUTION_SESSION'), 'F05': ('Mean from Frequency Table', 'FREQUENCY_SESSION'), 'F06': ('Median from Frequency Table', 'FREQUENCY_SESSION'), 'F07': ('Mode from Frequency Table', 'FREQUENCY_SESSION'), 'C05': ('List Sample Space', 'COIN_SESSION'), 'P10': ('Test Mutually Exclusive', 'SUPPLIED_SESSION'), 'P11': ('Test Independence', 'SUPPLIED_SESSION'), 'P12': ('Direct Intersection Counts', 'TWO_WAY_SESSION'), 'P13': ('Valid Probability Value', 'VALID_PROBABILITY'), 'P14': ('Two-Way Table Events', 'TWO_WAY_SESSION'), 'R04': ('Probability from X/P Table', 'DISTRIBUTION_SESSION'), 'R05': ('Missing Probability', 'MISSING_PROBABILITY'), 'R06': ('Unusual Event Probability', 'DISTRIBUTION_SESSION'), 'R07': ('Sample Without Replacement', 'SAMPLE_SESSION'), 'R08': ('Expected Profit or Loss', 'PAYOFF_SESSION'), 'B11': ('Full Binomial Distribution', 'BINOMIAL_SESSION'), 'B12': ('Binomial Shape and Symmetry', 'SHAPE_TASKS'), 'B13': ('Binomial Usual Counts', 'BINOMIAL_SESSION')}

NEW_ROUTES = {
 'S13':('Raw Data Summary','STDATA','raw_session'),
 'S14':('Sample Variance','STDATA','raw_session'),
 'S15':('Midrange','STDATA','raw_session'),
 'S16':('Compare Two Data Sets','STDATA','compare_session'),
 'G04':('Boxplot Builder','STGRAPH','boxplot_session'),
 'G05':('Dotplot Builder','STGRAPH','dotplot_session'),
 'G06':('Histogram Builder','STHIST','histogram_session'),
 'G07':('Normal Curve Axes','STNORM','axes_session'),
 'G08':('Empirical Rule','STNORM','empirical_session'),
 'G09':('Relative Position','STNORM','relative_session'),
 'F08':('Grouped Frequency Table','STHIST','group_session'),
 'D05':('Sampling Methods','STSTUDY','sampling_menu'),
 'D06':('Observational vs Experiment','STSTUDY','experiment_classifier'),
 'D07':('Measurement Levels','STSTUDY','measurement_menu'),
 'D08':('Statistical vs Practical','STSTUDY','significance_menu'),
 'D09':('Law of Large Numbers','STSTUDY','large_numbers'),
 'P15':('Certain / Impossible','STPROB','valid_probability')}
for gid in NEW_ROUTES:
    GUIDES[gid]=(NEW_ROUTES[gid][0],gid)


def lookup(group,key):
    return globals()[group][key]
