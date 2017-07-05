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
h.load_file('stdrun.hoc')
h.load_file('Fspikewave.oc')
it2l = ['it2WT', 'it2C456S', 'it2R788C', 'it2', 'it', 'itrecustom', 'ittccustom'] # it2 is RE, it is TC channel

def barname (mech='it'):
  '''return the name of a gbar (max conductance) for a given mechanism name'''
  l = []
  pname, ms  = h.ref(''), h.MechanismStandard(mech, 1)
  for i in range(int(ms.count())):
    ms.name(pname, i)
    l.append(pname[0])
  ll=[x for x in l if 'bar' in x]
  if len(ll)!=1: raise Exception("Can't identify proper parameter for %s: %s"%(mech, ll))
  return ll[0]

def mkdict (): 
  global Tdi
  Tdi = {n:barname(n) for n in it2l}
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
  for ce in thalDict['RE']['cel']:
    sec=ce.soma[0]
    for mech in it2l:
      ce.soma[0].insert(mech)
      h('%s.gcabar_%s = 0.0'%(str(sec),mech))
  recv()
      
def setparams (mun=0, pnafjr=0.0, gnamult=1.0, gcabar=3e-3, gcavfac=1.0, tyli=['TC', 'RE', 'PY', 'IN']):
  it2= it2l[mun]
  ms = h.MechanismStandard(it2, 1)
  print "Using %s channels"%it2
  for vals in thalDict.values():
    for ce in vals['cel']:
      ce.soma[0].gnabar_hh2nafjr = pnafjr *  gnamult * vals['gnabar']
      ce.soma[0].gnabar_hh2  =  (1-pnafjr) * gnamult * vals['gnabar']
  for ce in thalDict['RE']['cel']: # just set the RE one for now; corrD=3.777 for surface correction (Cav32RE3cc.hoc:105:257)
    sec=ce.soma[0]
    for v in Tdi.values(): sec.__setattr__(v, 0.0) # turn all off
    sec.__setattr__(Tdi[it2], gcabar*gcavfac)

# recording
def recv (thresh=-5):
  for k,v in thalDict.iteritems():
    v['spkt'], v['spkid'], v['vrec'] = h.Vector(5e3), h.Vector(5e3), []
    for j, (ce, nc) in enumerate(zip(v['cel'],v['ncl'])):
      ve = h.Vector(h.tstop/h.dt+10)
      ve.record(ce.soma[0](0.5)._ref_v)
      v['vrec'].append(ve)
      nc.record(v['spkt'], v['spkid'], j)

thalDict = mkdict()
setup()
setparams()
