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

def mkdict (): 
  tD = {'TC': {'cel': [], 'gnabar': h.TC[0].soma[0].gnabar_hh2, 'ncl': []},
        'RE': {'cel': [], 'gnabar': h.RE[0].soma[0].gnabar_hh2, 'ncl': []},
        'PY': {'cel': [], 'gnabar': h.PY[0].soma[0].gnabar_hh2, 'ncl': []},
        'IN': {'cel': [], 'gnabar': h.TC[0].soma[0].gnabar_hh2, 'ncl': []}}
  for i in range(int(h.nthalamiccells)):
    tD['TC']['cel'].append(h.TC[i]) 
    tD['RE']['cel'].append(h.RE[i])
    tD['PY']['cel'].append(h.PY[i])
    tD['IN']['cel'].append(h.IN[i]) 
  for tyl in tD.values():
    for i,ce in enumerate(tyl['cel']):
      ncl = h.cvode.netconlist(ce,'','')
      if len(ncl)>0: tyl['ncl'].append(ncl[0]) # just take one
      else: print 'No netcons found for cell %s'%str(ce)
  return tD

def setup ():
  h.tstop=1e3
  for vals in thalDict.values():
    for ce in vals['cel']:
      ce.soma[0].insert('hh2nafjr')
      ce.soma[0].gnabar_hh2nafjr = 0.0
      
def setparams (pnafjr=0.0, gnamult=1.0, tyli=['TC', 'RE', 'PY', 'IN']):
  for vals in thalDict.values():
    for ce in vals['cel']:
      ce.soma[0].gnabar_hh2nafjr = pnafjr *  gnamult * vals['gnabar']
      ce.soma[0].gnabar_hh2  =  (1-pnafjr) * gnamult * vals['gnabar']

# recording
def recv (thresh=-5):
  global spkt,spkid,nrec
  spkt, spkid, nrec, n = h.Vector(5e3), h.Vector(5e3), [], 0
  for k,v in thalDict.iteritems():
    for ce, nc in zip(v['cel'],v['ncl']):
      ve = h.Vector(h.tstop/h.dt+10)
      ve.record(ce.soma[0](0.5)._ref_v)
      nrec.append(ve)
      nc.record(spkt, spkid, n)
      n+=1  # counter

thalDict = mkdict()
setup()
setparams()
