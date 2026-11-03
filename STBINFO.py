import STCORE as c
def show_answer(n, p, event, answer, title, first_page=None, threshold=(1, 20), cache=None):
    cache = {} if cache is None else cache
    index = 0
    sketch_index = None
    while True:
        if first_page is not None and index == 0:
            page = first_page
        else:
            target = index - (1 if first_page is not None else 0)
            page = c.call('STBINFO2', 'page', n, p, event, answer, threshold, cache, target)
            if page is None:
                if sketch_index is None: sketch_index=index
                if index != sketch_index: return
                page=c.call('STSKETCH','bars',0,n,event)
        action = c.view(title,c.graph_lines(page,('STGBARS','show',(('binomial',n,p),event,'BINOMIAL'))))
        if action == 'exit': return
        if action == 'back':
            if index == 0: return
            index -= 1
        else: index += 1
