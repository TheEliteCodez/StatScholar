import STCORE as c

def inference(ts,alpha,alternative,degrees=None):
  return c.call('STHYP','inference',ts,alpha,alternative,degrees)

def conclusion(setup,reject):
  return c.call('STHYEND','conclusion',setup,reject)

def drawing(setup,result,critical):
  return c.call('STHYDRAW','drawing',setup,result,critical)

def step(index,setup,result,probability,critical,reject):
  module=c.call('STHYP','page_module',index)
  return c.call(module,'step',index,setup,result,probability,critical,reject)

def show(setup,result,inference_result=None):
  return c.call('STHYP','show',setup,result,inference_result)
