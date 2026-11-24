import STCORE as c

def menu():
  while True:
    route=c.call('STHYMNU','choose')
    if route is None:return
    kind,module,function,args=route
    payload=c.call(module,function,*args)
    if payload is not None:
      if kind=='test':c.call('STHYSH','show',*payload)
      elif kind=='chi':c.call('STCHISH','show',payload)
    payload=None

def inference(ts,alpha,alternative,degrees=None):
  return c.call('STHYINF','inference',ts,alpha,alternative,degrees)

def page_module(index):
  if index<=3:return 'STHYREQ'
  if index<=5:return 'STHYTS'
  if index==6:return 'STHYDRAW'
  if index==7:return 'STHYPVAL'
  return 'STHYEND'

def show(setup,result,inference_result=None):
  return c.call('STHYSH','show',setup,result,inference_result)
