import STCORE
class DefinitionBank:
    def __init__(self,name): self.name=name
    def __iter__(self): return iter(STCORE.call('STDEFS','get_definitions',self.name))
    def __getitem__(self,index): return STCORE.call('STDEFS','get_definitions',self.name,index)
DEFINITIONS = DefinitionBank('DEFINITIONS')
SAMPLING_DEFINITIONS = DefinitionBank('SAMPLING_DEFINITIONS')
MEASUREMENT_DEFINITIONS = DefinitionBank('MEASUREMENT_DEFINITIONS')
STUDY_DEFINITIONS = DefinitionBank('STUDY_DEFINITIONS')
BIAS_DEFINITIONS = DefinitionBank('BIAS_DEFINITIONS')
def definition_pages(title, definition):
    return STCORE.call('STPAGE','text_pages',title,definition)
def definition_list(title, entries):
    while True:
        key = STCORE.menu(title, [(str(i+1), entry[0].upper())
                                 for i, entry in enumerate(entries)])
        if key == '0': return
        term, definition = entries[int(key)-1]
        definition_pages(term, definition)
        definition_solver(term)
def normalized_term(text):
    words=text.lower().replace('convienience','convenience').replace('nonsampling','non sampling').replace('-',' ').replace('sampling','sample').split()
    return ' '.join('distribution' if word in ('dist','distr') else word for word in words)
def definition_solver(term):
    routes={'mean':('STDATA','raw_session'),'median':('STDATA','raw_session'),'z score':('STNORM','normal_session',None,None,'1'),
        'outlier':('STDESC','solver_outlier'),'empirical rule':('STNORM','empirical_session'),
        'range rule of thumb':('STNORM','normal_session',None,None,'5'),'expected value':('STCOUNT','distribution_session')}
    if term in routes and STCORE.menu('USE THIS DEFINITION',[('1','OPEN CALCULATION')])=='1': STCORE.call(*routes[term])
def study_yesno(prompt):
    key=STCORE.menu(prompt,[('1','YES'),('2','NO'),('3','UNSURE / NEED DETAILS')],('Y','N'))
    if key in ('0','3'):
        if key=='3': definition_pages('NEED DETAILS','CHECK WHAT THE QUESTION SAYS ABOUT THE TARGET GROUP OR SELECTION PROCEDURE.')
        return None
    return key in ('1','Y')
def definitions_menu():
    while True:
        key = STCORE.menu('DEFINITIONS', [
            ('1', 'SAMPLING TYPES / BIAS'),
            ('2', 'LEVELS OF MEASUREMENT'),
            ('3', 'ERRORS / SIGNIFICANCE'),
            ('4', 'OUTLIER'), ('5', 'SEARCH ALL DEFINITIONS'), ('6', 'SURVEY BIAS / QUOTAS')])
        if key == '0': return
        if key == '1': definition_list('SAMPLING TYPES / BIAS', SAMPLING_DEFINITIONS)
        elif key == '2': definition_list('MEASUREMENT LEVELS', MEASUREMENT_DEFINITIONS)
        elif key == '3': definition_list('ERRORS / SIGNIFICANCE', STUDY_DEFINITIONS[:4])
        elif key == '4': definition_pages(*STUDY_DEFINITIONS[-1])
        elif key == '6': definition_list('BIAS / QUOTAS', BIAS_DEFINITIONS)
        elif key == '5':
            term = input('SEARCH TERM: ').strip().lower()
            term = normalized_term(term)
            if not term: continue
            matches = []
            for group in (SAMPLING_DEFINITIONS, MEASUREMENT_DEFINITIONS,
                          STUDY_DEFINITIONS, BIAS_DEFINITIONS, DEFINITIONS):
                for name, definition in group:
                    if group is DEFINITIONS and name == 'outlier': continue
                    if term in normalized_term(name) or term in normalized_term(definition):
                        matches.append((name, definition))
            if matches: definition_list('SEARCH RESULTS', matches)
            else: definition_pages('NO MATCH', 'TRY SAMPLE, BIAS, ORDINAL, ERROR, SIGNIFICANT, OR OUTLIER.')
def study_menu():
    routes=(population_classifier,parameter_classifier,sampling_menu,experiment_classifier,measurement_menu,significance_menu,definitions_menu,large_numbers)
    while True:
        key=STCORE.menu('STUDY / CONCEPTS',[(str(i+1),label) for i,label in enumerate(('SAMPLE / POPULATION','PARAMETER / STATISTIC','SAMPLING METHOD','OBSERVATIONAL / EXPERIMENT','MEASUREMENT LEVEL','SIGNIFICANCE / ERROR','DEFINITIONS','LAW OF LARGE NUMBERS','STATISTICAL CONCEPTS','RULES / FORMULAS'))])
        if key=='0': return
        if key=='9': STCORE.call('STSTU2','statistical_concepts')
        elif key=='10': STCORE.call('STRULE','rules_menu')
        else: routes[int(key)-1]()
def population_classifier(): STCORE.call('STSTU1','population_classifier')
def parameter_classifier(): STCORE.call('STSTU1','parameter_classifier')
def sampling_menu(): STCORE.call('STSTU2','sampling_menu')
def experiment_classifier(): STCORE.call('STSTU1','experiment_classifier')
def measurement_menu(): STCORE.call('STSTU2','measurement_menu')
def significance_menu(): STCORE.call('STSTU2','significance_menu')
def large_numbers(): STCORE.call('STSTU2','large_numbers')
