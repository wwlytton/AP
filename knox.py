''' USAGE example
import knox as kx
h.run()
import graph as g
g.TCraster(kx.thalDict)
'''

from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
from collections import OrderedDict as OD
datestr = os.popen('datestring').read()
h.load_file('stdrun.hoc')
h.load_file('Fspikewave.oc')
it2l = ['it2WT', 'it2C456S', 'it2R788C', 'it2', 'itrecustom'] # it2 is RE, it is TC channel
                                                               # RERE    RETCa  RETCb  TCRE  PYPY  PYIN  INPYa    INPYb  PYRE  PYTC   TCPY  TCIN  
synparams = OD({'synaptic weights J neurophys':                  (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.1500,  0.03,  1.2,  0.01,  1.2,  0.4), 
'75% IN->PY weight (0.1125)':                                    (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.1125,  0.03,  1.2,  0.01,  1.2,  0.4), 
'50% IN->PY weight (0.075)':                                     (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0750,  0.03,  1.2,  0.01,  1.2,  0.4), 
'40% IN->PY weight (0.06)':                                      (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0600,  0.03,  1.2,  0.01,  1.2,  0.4), 
'25% IN->PY weight (0.0375)':                                    (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0375,  0.03,  1.2,  0.01,  1.2,  0.4), 
'10% IN->PY weight (0.015)':                                     (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0150,  0.03,  1.2,  0.01,  1.2,  0.4), 
'0% IN->PY A weight':                                            (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0000,  0.03,  1.2,  0.01,  1.2,  0.4), 
'orig IN->PY A weight':                                          (0.20,  0.02,  0.04,  0.2,  0.6,  0.2,  0.1500,  0.03,  1.2,  0.01,  1.2,  0.4), 
'10% IN->PY A weight better RERE for new synapses':              (0.12,  0.02,  0.04,  0.2,  0.6,  0.2,  0.0000,  0.03,  1.2,  0.01,  1.2,  0.4), 
'0% RERE and RETC':                                              (0.00,  0.00,  0.04,  0.2,  0.6,  0.2,  0.1500,  0.03,  1.2,  0.01,  1.2,  0.4)})
# gababapercent, gababpercent were both == 1

def setsyns (k='orig IN->PY A weight'):
  '''Allow abbreviation of dict key for synparams'''
  k1 = [x for x in synparams.keys() if k in x][0]
  print k1
  apply(h.assign_synapses, synparams[k])

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
  tD = {k: {'cel': list(h.List('s%s'%k)), 'ncl': [], 'stims': []} for k in ['TC', 'RE', 'PY', 'IN']}
  for tyl in tD.values():
    for i,ce in enumerate(tyl['cel']):
      ncl = h.cvode.netconlist(ce,'','')
      if len(ncl)>0: tyl['ncl'].append(ncl[0]) # just take one
      else: print 'No netcons found for cell %s'%str(ce)
  tD['RE']['T'], tD['TC']['T']={n:barname(n) for n in it2l}, {n:barname(n) for n in ['ittccustom', 'it']}
  for v in tD.itervalues(): v['gnabar'] = v['cel'][0].soma[0].gnabar_hh2
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
      
def setchans (mun=3, pnafjr=0.0, gnamult=1.0, gcabar=3e-3, gcavfac=1.0, tyli=['TC', 'RE', 'PY', 'IN']):
  it2= it2l[mun]
  ms = h.MechanismStandard(it2, 1)
  print "Using %s channels"%it2
  for vals in thalDict.values():
    for ce in vals['cel']:
      ce.soma[0].gnabar_hh2nafjr = pnafjr *  gnamult * vals['gnabar'] # what is this??
      ce.soma[0].gnabar_hh2  =  (1-pnafjr) * gnamult * vals['gnabar']
  for ce in thalDict['RE']['cel']: # just set the RE one for now; corrD=3.777 for surface correction (Cav32RE3cc.hoc:105:257)
    sec=ce.soma[0]
    for v in thalDict['RE']['T'].values(): sec.__setattr__(v, 0.0) # turn all off
    sec.__setattr__(thalDict['RE']['T'][it2], gcabar*gcavfac)

def setstims (ctype='PY', nl=[11,30,49,68], amp=0.7, dly=10.0, dur=50.0):
  stims = thalDict[ctype]['stims']
  if len(nl)>len(stims): stims += [h.IClamp() for i in range(len(nl) - len(stims))] # extend stim list
  for x in stims: 
    if x.get_segment(): x.amp=0.0 # clear
  for x,n in zip(stims,nl): # nl may be shorter than stim
    loc=thalDict[ctype]['cel'][n].soma[0](0.5)
    x.loc(loc)
    x.amp, x.dur, x.delay = amp, dur, dly

# recording
def recv (thresh=-5):
  for k,v in thalDict.iteritems():
    v['spkt'], v['spkid'], v['vrec'] = h.Vector(5e3), h.Vector(5e3), []
    for j, (ce, nc) in enumerate(zip(v['cel'],v['ncl'])):
      nc.record(v['spkt'], v['spkid'], j)
    for j in [30, 70]:
      ce = v['cel'][j]
      ve = h.Vector(h.tstop/h.dt+10)
      v['vrec'].append(ve)
      ve.record(ce.soma[0](0.5)._ref_v)

thalDict = mkdict()
setup()
recv()
setchans() # used to be setparams()
setsyns()
setstims()
