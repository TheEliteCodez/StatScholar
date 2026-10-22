"""Optional device diagnostic. Run EVOMEM instead of STAT1 for a manual audit.

Checkpoint readings include this diagnostic's overhead. They do not measure
the allocator's transient peak during compilation or arithmetic.
"""
import builtins
import gc
import STCORE as c


def main():
    free=getattr(gc,'mem_free',None)
    if free is None:
        print('DEVICE HEAP COUNTER UNAVAILABLE')
        print('No calculator RAM result recorded.')
        return
    gc.collect()
    start=free()
    state=[start,'START','START']
    importing=builtins.__import__
    calling=c.call
    menu=c.menu

    def sample():
        available=free()
        if available<state[0]:
            state[0]=available
            state[1]=state[2]

    def load(name,*args,**kwargs):
        sample()
        value=importing(name,*args,**kwargs)
        sample()
        return value

    def call(module,function,*args):
        sample()
        value=calling(module,function,*args)
        sample()
        return value

    def choose(title,*args,**kwargs):
        state[2]=title
        sample()
        key=menu(title,*args,**kwargs)
        state[2]=title+' > '+str(key)
        sample()
        return key

    failure=None
    try:
        builtins.__import__=load
        c.call=call
        c.menu=choose
        c.call('STHOME','quick_main')
    except Exception as exc:
        failure=type(exc).__name__+': '+str(exc)
    finally:
        builtins.__import__=importing
        c.call=calling
        c.menu=menu
    gc.collect()
    print('MEMORY AUDIT CHECKPOINTS')
    print('START FREE: '+str(start))
    print('MIN FREE: '+str(state[0]))
    print('AT: '+state[1])
    print('END FREE: '+str(free()))
    print('REMAINING TOPICS: '+str(len(c.topic_modules())))
    print('ERROR: '+(failure or 'NONE'))


if __name__=='__main__' or c.ON_TI:
    main()
