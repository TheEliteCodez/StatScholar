import STCORE as c

def conclusion(setup,reject):
    parameter={'mu':'THE POPULATION MEAN','p':'THE POPULATION PROPORTION',
               'mu1-mu2':'THE DIFFERENCE IN POPULATION MEANS',
               'p1-p2':'THE DIFFERENCE IN POPULATION PROPORTIONS',
               'mu_d':'THE POPULATION MEAN PAIRED DIFFERENCE'}.get(setup['parameter'],'THE POPULATION PARAMETER')
    relation={'<':'IS LESS THAN','>':'IS GREATER THAN','!=':'IS NOT EQUAL TO',
              '=':'IS EQUAL TO','<=':'IS LESS THAN OR EQUAL TO','>=':'IS GREATER THAN OR EQUAL TO'}[setup['claim']]
    statement=parameter+(' FOR '+setup['context'] if setup['context'] else '')+' '+relation+' %.8g.' % setup['null']
    action='WARRANT REJECTION OF' if setup['claim'] in ('=','<=','>=') else 'SUPPORT'
    lead='THERE IS '+('SUFFICIENT' if reject else 'NOT SUFFICIENT')+' EVIDENCE TO '+action+' THE CLAIM THAT '
    return lead+statement

def step(index,setup,result,probability,critical,reject):
    null=setup['null'];alt=setup['alternative'];alpha=setup['alpha']
    parameter=setup['parameter'];kind='z' if result['df'] is None else 't'
    if index==7:
        return c.call('STHYPVAL','step',index,setup,result,probability,critical,reject)
    if index==8:
        return ['REJECT H0' if reject else 'FAIL TO REJECT H0',
                'INITIAL CONCLUSION: SINCE THE p-VALUE, %.10g, IS %s THE SIGNIFICANCE LEVEL, %.8g, WE %s THE NULL HYPOTHESIS.' %
                (probability,'LESS THAN OR EQUAL TO' if reject else 'GREATER THAN',alpha,
                 'REJECT' if reject else 'FAIL TO REJECT')]
    return ['REJECT H0' if reject else 'FAIL TO REJECT H0',
            'BECAUSE p=%.10g %s alpha=%.10g.' % (probability,'<=' if reject else '>',alpha),
            'FINAL CONCLUSION ('+('TISE' if reject else 'TINSE')+'):',
            'AT THE %.8g%% SIGNIFICANCE LEVEL, ' % (100*alpha)+conclusion(setup,reject)]
