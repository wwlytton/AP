''' USAGE example
import knox
knox.setparams(pnafjr=0.5, tyli=['RE','TC'])
h.run()
'''
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
fig, axi = None, None
datestr = os.popen('datestring').read()

h.load_file('Fspikewave.oc')

def mksecls (): 
  global TCsl, REsl, PYsl, INsl, thalDict
  TCsl, REsl, PYsl, INsl = [],[],[],[]
  for i in range(int(h.nthalamiccells)):
    TCsl.append(h.TC[i]) 
    REsl.append(h.RE[i])
    PYsl.append(h.PY[i])
    INsl.append(h.IN[i]) 
  thalDict = {'TC': {'sl': TCsl, 'gnabar': TCsl[0].soma[0].gnabar_hh2, 'ncl': []},
              'RE': {'sl': REsl, 'gnabar': REsl[0].soma[0].gnabar_hh2, 'ncl': []},
              'PY': {'sl': PYsl, 'gnabar': PYsl[0].soma[0].gnabar_hh2, 'ncl': []},
              'IN': {'sl': INsl, 'gnabar': TCsl[0].soma[0].gnabar_hh2, 'ncl': []}}
  for tyl in thalDict.values():
    for i,ce in enumerate(tyl['sl']):
      ncl = h.cvode.netconlist(ce,'','')
      if len(ncl)>0: tyl['ncl'].append(ncl[0]) # just take one
      else: print 'No netcons found for cell %s'%str(ce)

def setup ():
  h.tstop=1e3
  for ty in [TCsl, REsl, PYsl, INsl]:
    for ce in ty:
      ce.soma[0].insert('hh2nafjr')
      ce.soma[0].gnabar_hh2nafjr = 0.0
      
def setparams (pnafjr=0.0, gnamult=1.0, tyli=['TC', 'RE', 'PY', 'IN']):
  for ty in tyli:
    for ce in thalDict[ty]['sl']:
      ce.soma[0].gnabar_hh2nafjr = pnafjr *  gnamult * thalDict[ty]['gnabar']
      ce.soma[0].gnabar_hh2  =  (1-pnafjr) * gnamult * thalDict[ty]['gnabar']

# recording
def recv (thresh=-5):
  global spkt,spkid,ncl,nrec
  tyli=['TC', 'RE', 'PY', 'IN']
  spkt, spkid = h.Vector(1e3), h.Vector(1e3)
  for nc in ncl: nc.threshold=thresh
  nrec = [h.Vector(h.tstop/h.dt+10) for x in range(len(nodl))]
  for i,nc in enumerate(ncl): nc.record(spkt,spkid, i)  # netcon.record(tvec, idvec, id)
  for v,n in zip(nrec,nodl): v.record(n(0.5)._ref_v)

mksecls()
setup()
setparams()
