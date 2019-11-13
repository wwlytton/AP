# execfile('test.py')
# %reset -f

from cfg import cfg
simConfig=cfg
from netParams import netParams
sim.create()
run() # sim.runSim()
sim.analyze() # data/sim1.json

import sys
sys.path.insert(1,'/usr/site/nrniv/local/python/netpyne')
import itertools as itr
import pandas as pd
import numpy as np
import pylab as plt
import json
fig, ax, params, data, pdi = None, None, None, None, None
from netpyne import specs, sim
from collections import OrderedDict

import axonA
ax=axonA.AxonA()
h.dt=0.00025
h.tstop=10
stim=h.IClamp(0.0,sec=ax.axon)
stim.amp, stim.dur = 2, 5

c0='cell_0' # convenient since only the 1 cell
dca = {}

# reading data section
def read ():
    global params, data
    sys.path.append('/usr/site/nrniv/local/python/netpyne/examples/batchCell')
    from utils import readBatchData
    params, data = readBatchData('data/', 'baxA', loadAll=1, saveAll=0, vars=None, maxCombs=None) 

def loadall (filename = 'data/baxA/baxA_allData.json'): 
  global params, data, pdi
  with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
  params, data = dataLoad['params'], dataLoad['data']
  pdi={k:str(d['paramValues'])[1:-1].replace(',','')  for k,d in data.items()} # pdi gives the values in a list for each of those codes
  for k in list(data.keys()): data[str(pdi[k])] = data.pop(k)

def loadpd (filename = 'data/baxA/df4.pd'):
  "need precise_float=True to get the correct numbers"
  return pd.read_json('data/baxA/df4.pd',precise_float=True)

vecl,tvec,idvec = [], h.Vector(100), h.Vector(100)
def setrec ():
  global vecl,tvec,idvec
  ncl,vecl = [],[]
  for x in np.linspace(0,0.5,9): # these are relative locations so only go halfway
    v=h.Vector(20e3+10)
    vecl.append(v)
    v.record(ax.axon(x)._ref_v)
    nc = h.NetCon(ax.axon(x)._ref_v, None)
    nc.threshold=-35 # default is -25
    ncl.append(nc)
  [nc.record(tvec, idvec, id) for id,nc in enumerate(ncl)]           

def plotone (key='perc0'):
  plt.clf()
  tv1=dca[key]['tvec']; vl=h.Vector(tv1.size()); vl.fill(-35.0)
  tv=h.Vector(dca[key]['v0'].size()); tv.indgen(h.dt)
  plt.scatter(tv1,vl)
  for k,v in dca[key].items(): 
    if k.startswith('v'):
      plt.plot(tv,v)

def mkdict ():
  global vecl,tvec,idvec
  di = {'v%g'%(loc):v.c() for loc,v in zip(np.linspace(0,1,9), vecl)}
  di['tvec'], di['idvec'] = tvec.c(), idvec.c()
  return di

def runfew ():
  dca = {}
  setrec()
  for ax.percnajr in np.linspace(0,0.9,9):
    ax.set_props()
    h.run()
    dca['perc%g'%(ax.percnajr)] = mkdict()
  return dca

def showvels ():
  vels={}
  L = 1.0  # ax.axon.L = 2mm but only looking at first 1mm
  pts = dca[list(dca.keys())[0]]['tvec'].size()  # num of points recorded from on axon
  vec=h.Vector(pts) # of spots being recorded
  for k,v in dca.items():
    if v['tvec'].size()>2:
      vec.resize(v['tvec'].size())
      vec.fill(L/(pts-1)) # spots are 125 mu apart
      vels[k] = (vec.c().div(v['tvec'].c().deriv()), (1.0/(v['tvec'].max()-v['tvec'].min())))  
  return vels

# fig, axi = plt.subplots(1, 1)
# df4.query('gnabar==0.12 & temp==6.3 & rall==200').plot('percnajr','V0max',label="abc",ax=axi)
# df4[(df4.gnabar==0.12) & (df4.temp==6.3) & (df4.rall==200)].plot('percnajr','V0max',label="abc",ax=axi)

def dfq (cel,na,ra): 
  "order of temp, na, ra"
  from numpy import isclose as eq
  return df4[eq(df4.gnabar,na) & eq(df4.temp,cel) & eq(df4.rall,ra)]

def mkfig (): 
  global fig,axi
  fig, axi = plt.subplots(1, 1)

def mkqstr (l):
  'Create a query string from a list of tuples with (name, value)'
  st,sr = '',''
  for x in l: 
    st+="%s==%g&"%(x[0],x[1])
    sr+="%g,"%(x[1])
  return (st.strip('[ &]'),sr.strip('[,]'))

def supfigs (y='V0max'):
  axi.clear()
  for i,tup in enumerate([list(zip(labs,x)) for x in itr.product(*[v for x,v in vals.items()])]):
    st,sr=mkqstr(tup)
    res=df4.query(st)
    if (len(res)<2): print(st)
    res.plot('percnajr',y,label=sr,ax=axi,linewidth=10-i)

def mkdf4 ():
  spkdi={key: max(d['simData']['V_axon_0.0']['cell_0']) for key, d in data.items()}
  spks={key: max for key, max in spkdi.items() if max>-30}
  pdi1={ str(d['paramValues'])[1:-1].replace(',',''): d['paramValues'] for k,d in data.items()}
  numdi={key: len(d['simData']['spkt']) for key, d in data.items()}
  df1 = pd.DataFrame.from_dict(spkdi, orient='index') 
  df2 = pd.DataFrame.from_dict(pdi1, orient='index') 
  df3 = pd.merge(df1,df2,left_index=True,right_index=True)
  tmp=pd.DataFrame(columns=['numspks']).from_dict(numdi, orient='index')  # can't set the column names at start??
  df4 = pd.merge(df3,tmp,left_index=True,right_index=True)
  df4.columns=['V0max','gnabar','rall','temp','percnajr','numspks']
  return df4

'''
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
'''
