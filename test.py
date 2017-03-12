import sys
sys.path.insert(1,'/usr/site/nrniv/local/python/netpyne')
import itertools as itr
import pandas as pd
import numpy as np
import pylab as plt
import json
fig, ax, params, data = None, None, None, None
from netpyne import specs, sim
from collections import OrderedDict

c0='cell_0' # convenient since only the 1 cell
dca = {}

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

vecl,tvec,idvec = [], h.Vector(100), h.Vector(100)
def setrec ():
  global vecl,tvec,idvec
  ncl,vecl = [],[]
  for x in np.linspace(0,1,9):
    v=h.Vector(20e3+10)
    vecl.append(v)
    v.record(ax.axon(x)._ref_v)
    ncl.append(h.NetCon(ax.axon(x)._ref_v, None))
  [nc.record(tvec, idvec, id) for id,nc in enumerate(ncl)]           

def plotone ():
  tv=h.Vector(vecl[0].size())
  tv.indgen(h.dt)
  plt.clf()
  for v in vecl: plt.plot(tv,v) 

def mkdict ():
  global vecl,tvec,idvec
  di = {'v%g'%(loc):v.c() for loc,v in zip(np.linspace(0,1,9), vecl)}
  di['tvec'], di['idvec'] = tvec.c(), idvec.c()
  return di

def runfew ():
  dca = {}
  for ax.percnajr in np.linspace(0,0.9,9):
    ax.set_props()
    h.run()
    dca['perc%g'%(ax.percnajr)] = mkdict()
  return dca

def showvels ():
  L = 1  # ax.axon.L = 1000 so 1 mm; want to end up with mm/ms
  pts = dca[dca.keys()[0]]['tvec'].size()  # num of points recorded from on axon
  vec=h.Vector(pts) # of spots being recorded
  vec.fill(L/(pts-1)) # spots are 125 mu apart
  vels = {k:(vec.c().div(v['tvec'].c().deriv()), (0.9/(v['tvec'].max()-v['tvec'].min())))  for k,v in dca.iteritems() if v['tvec'].size()==9}
  return vels

# fig, ax = plt.subplots(1, 1)
# df4.query('gnabar==0.12 & temp==6.3 & rall==200').plot('percnajr','V0max',label="abc",ax=ax)
# df4[(df4.gnabar==0.12) & (df4.temp==6.3) & (df4.rall==200)].plot('percnajr','V0max',label="abc",ax=ax)

def dfq (cel,na,ra): 
  "order of temp, na, ra"
  from numpy import isclose as eq
  return df4[eq(df4.gnabar,na) & eq(df4.temp,cel) & eq(df4.rall,ra)]

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

def supfigs (y='V0max'):
  ax.clear()
  for i,tup in enumerate([zip(labs,x) for x in itr.product(*[v for x,v in vals.iteritems()])]):
    st,sr=mkqstr(tup)
    res=df4.query(st)
    if (len(res)<2): print st
    res.plot('percnajr',y,label=sr,ax=ax,linewidth=10-i)

def mkdf4 ():
  spkdi={key: max(d['simData']['V_axon_0.0']['cell_0']) for key, d in data.iteritems()}
  spks={key: max for key, max in spkdi.iteritems() if max>-30}
  pdi={k:d['paramValues'] for k,d in data.iteritems()}
  numdi={key: len(d['simData']['spkt']) for key, d in data.iteritems()}
  df1 = pd.DataFrame.from_dict(spkdi, orient='index') 
  df2 = pd.DataFrame.from_dict(pdi, orient='index') 
  df3 = pd.merge(df1,df2,left_index=True,right_index=True)
  tmp=pd.DataFrame(columns=['numspks']).from_dict(numdi, orient='index')  # can't set the column names at start??
  df4 = pd.merge(df3,tmp,left_index=True,right_index=True)
  df4.columns=['V0max','gnabar','rall','temp','percnajr','numspks']
  return df4

if __name__ == '__main__':
  createdf4=False
  if createdf4:
    loadall()      # data and params
    df4=mkdf4()
  else:
    df4=loadpd()
  labs=['temp', 'gnabar', 'rall']  # should grab param names from pandas table; would need 
  vals = OrderedDict([(x,set(df4[x].tolist())) for x in labs])  # guarantee same order
  mkfig()
  supfigs()
  plt.show()
  
