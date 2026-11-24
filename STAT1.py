import STCORE as c

def hypothesis():
  state=None
  value=None
  while True:
    operation,args,state=c.call('STHYFLOW','advance',state,value)
    value=None
    if operation=='done':return
    if operation=='call':value=c.call(args[0],args[1],*args[2])
    elif operation=='plot':value=c.ht_plot(*args)
    elif operation=='view':value=c.view(*args)
    else:value=c.menu(*args)
    args=None

def main():
  while True:
    route=c.call('STHOME','choose')
    if route is None:return
    module,function,args=route
    route=None
    try:
      if module=='STHYP':hypothesis()
      else:c.call(module,function,*args)
    except (ValueError,ZeroDivisionError,IndexError) as exc:
      c.view('CHECK ENTERED VALUES',[str(exc)])
    args=None
if __name__=='__main__' or c.ON_TI:
  main()
