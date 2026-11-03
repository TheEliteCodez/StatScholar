import STCORE
def data_tasks(g):
    while True:
        key=STCORE.menu('DATA / STATISTICS',[('1','RAW LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','DISCRETE DISTR: x / P(x)'),('4','ROW / COLUMN TABLE'),('5','CATEGORY COUNTS'),('6','COMPARE TWO DATA SETS'),('7','PERCENT OF TOTAL'),('8','CORRELATION / REGRESSION')],page_size=7)
        if key=='0': return
        if key=='8':
            STCORE.call('STREGIO','session');continue
        routes={'1':('STDATA','raw_session'),'2':('STDATA','frequency_data_session'),'3':('STCOUNT','distribution_session'),'4':('STPROB','two_way_session'),'5':('STPROB','category_session'),'6':('STDATA','compare_session'),'7':('STPCT','percent_session')}
        if key in routes: STCORE.call(*routes[key])
def graph_tasks(g):
    while True:
        key=STCORE.menu('GRAPHS / DATA SHAPE',[('1','SCATTER / REGRESSION'),('2','BOXPLOT'),('3','DOTPLOT'),('4','HISTOGRAM'),('5','INTERPRET SHAPE / NORMALITY'),('6','OUTLIERS'),('7','COMPARE RELATIVE POSITION')])
        if key=='0': return
        if key=='1':
            STCORE.call('STREGIO','session');continue
        if key=='5': STCORE.call('STGRAPH','shape_guide')
        elif key=='6':
            choice=STCORE.menu('GRAPH > OUTLIERS',[('1','FROM RAW DATA'),('2','GIVEN Q1 AND Q3')])
            if choice=='1': STCORE.call('STGRAPH','raw_outliers')
            elif choice=='2': STCORE.call('STDESC','solver_outlier')
        elif key!='0': STCORE.call(*{'2':('STGRAPH','boxplot_session'),'3':('STGRAPH','dotplot_session'),'4':('STHIST','histogram_session'),'7':('STNORM','relative_session')}[key])
def experiment_tasks(g, word=None):
    while True:
        key=STCORE.menu('PROB > RANDOM EXPERIMENT',[('1','ONE / MULTIPLE DICE'),('2','DIE + COIN'),('3','COIN FLIPS'),('4','52 CARDS'),('5','ROULETTE'),('6','SPINNER')],page_size=6)
        if key=='0': return
        if key=='1': STCORE.call('STDICE','dice_session',word)
        elif key=='3': STCORE.call('STBWORD','wording_session',word,None,(1,2))
        elif key!='0': STCORE.call('STEXPER','experiment_session',{'2':'coin','4':'cards','5':'roulette','6':'spinner'}[key],word)
        word=None
