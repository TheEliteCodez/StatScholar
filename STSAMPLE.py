import STCORE
def probability(total,targets,draws,k):
    return STCORE.call('STSAMP1', 'probability', total, targets, draws, k)
def moments(total,targets,draws):
    return STCORE.call('STSAMP1', 'moments', total, targets, draws)
def show_distribution(total,targets,draws,summary=False):
    return STCORE.call('STSAMP1', 'show_distribution', total, targets, draws, summary)
def event_probability(total,targets,draws,event):
    return STCORE.call('STSAMP1', 'event_probability', total, targets, draws, event)
def hyper_distribution(npop, targets, draws):
    return STCORE.call('STSAMP1', 'hyper_distribution', npop, targets, draws)
def sample_session():
    return STCORE.call('STSAMP2', 'sample_session')
def sample_word_session(word=None):
    return STCORE.call('STSAMP2', 'sample_word_session', word)
def read_parameters():
    return STCORE.call('STSAMP2', 'read_parameters')
def sample_tasks(total,targets,draws,word=None):
    return STCORE.call('STSAMP2', 'sample_tasks', total, targets, draws, word)
def box_session():
    return STCORE.call('STSAMP2', 'box_session')
