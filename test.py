import sys
import itertools as itr
import pandas as pd
import numpy as np
import pylab as plt
fig, ax, params, data = None, None, None, None

# reading data section
def read ():
    global params, data
    sys.path.append('/usr/site/nrniv/local/python/netpyne/examples/batchCell')
    from utils import readBatchData
    params, data = readBatchData('data/', 'baxA', loadAll=1, saveAll=0, vars=None, maxCombs=None) 

def loadall (filename = 'data/baxA/baxA_allData.json'): 
  global params, data
  with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
  params, data = dataLoad['params'], dataLoad['data']

def loadpd (filename = 'data/baxA/df4.pd'):
  "need precise_float=True to get the correct numbers"
  return pd.read_json('data/baxA/df4.pd',precise_float=True)

# fig, ax = plt.subplots(1, 1)
# df4.query('gnabar==0.12 & temp==6.3 & rall==200').plot('percnajr','V0max',label="abc",ax=ax)
# df4[(df4.gnabar==0.12) & (df4.temp==6.3) & (df4.rall==200)].plot('percnajr','V0max',label="abc",ax=ax)

def mkfig (): 
  global fig,ax
  fig, ax = plt.subplots(1, 1)

def mkqstr (l):
  'Create a query string from a list of tuples with (name, value)'
  st,sr = '',''
  for x in l: 
    st+="%s==%g&"%(x[0],x[1])
    sr+="%g,"%(x[1])
  return (st.strip('[ &]'),sr.strip('[,]'))

def supfigs ():
  ax.clear()
  for i,tup in enumerate([zip(labs,x) for x in itr.product(*[v for x,v in vals.iteritems()])]):
    st,sr=mkqstr(tup)
    res=df4.query(st)
    res.plot('percnajr','V0max',label=sr,ax=ax,linewidth=10-i)

if __name__ == '__main__':
  df4=loadpd()
  labs=['temp', 'gnabar', 'rall']  # should grab labs from pandas table
  vals = {x:set(df4[x].tolist())) for x in labs}
  mkfig()
  supfigs()
  
