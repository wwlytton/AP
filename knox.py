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
for hoc in ['stdrun.hoc', 'TC.tem', 'RE.tem', 'sPY.tem', 'sIN.tem']: h.load_file(hoc)

ncorticalcells, nthalamiccells = 100, 100
axondelay, narrowdiam, widediam = 0, 5, 10

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

def mkcells (): 
  types = ['TC', 'RE', 'PY', 'IN']
  tD = {k: {'cel': [], 'ncl': [], 'stims': [], 'predi': {}} for k in types}
  for pre, ei in zip(types, ['ampapost','gabaapost','ampapost','gabaapost']): 
    tD[pre]['targ'] = {}
    for post in types:
      tD[pre]['targ'][post] = ei
  tD['PY']['targ']['PY'], tD['TC']['targ']['PY'] = 'ampapostPY', 'ampapostTC'
  for k in ['TC','RE']:
    tD[k]['num'] = nthalamiccells
    for i in range(nthalamiccells): 
      tD[k]['cel'].append(h.__getattribute__('s'+k)())
  for k in ['PY','IN']:
    tD[k]['num'] = ncorticalcells
    for i in range(ncorticalcells): 
      tD[k]['cel'].append(h.__getattribute__('s'+k)())
  tD['RE']['T'], tD['TC']['T']={n:barname(n) for n in it2l}, {n:barname(n) for n in ['ittccustom', 'it']}
  for v in tD.itervalues(): v['gnabar'] = v['cel'][0].soma[0].gnabar_hh2
  return tD

def mksyns (tD):
  global dbl
  dbl=[]
  for k in tD.keys(): tD[k]['lambda'] = {k1:narrowdiam for k1 in tD.keys()}  # default narrowdiam
  for zero in ['INTC', 'INRE', 'TCTC', 'ININ', 'REPY', 'REIN']: tD[zero[:2]]['lambda'][zero[2:]] = 0
  for wide in ['PYRE', 'PYTC', 'TCPY', 'TCIN']:                 tD[wide[:2]]['lambda'][wide[2:]] = widediam
  for k in tD.keys():
    for k1 in tD.keys():
      if tD[k]['lambda'][k1] > 0:
        connect(k,k1,tD)
  for tyl in tD.values():
    for i,ce in enumerate(tyl['cel']):
      ncl = h.cvode.netconlist(ce,'','')
      if len(ncl)>0: tyl['ncl'].append(ncl[0]) # just take one
      else: print 'No netcons found for cell %s'%str(ce)

def assignSyns (k='orig IN->PY A weight', tD=None):
  '''Assign weight strengthes for synapses'''
  if not tD: tD=thalDict
  w = synparams[[x for x in synparams.keys() if k in x][0]] # allow abbreviating these long titles
  print w
  syid = ['RERE', 'RETCga', 'RETCgb', 'TCRE', 'PYPY', 'PYIN', 'INPYga', 'INPYgb', 'PYRE', 'PYTC', 'TCPY', 'TCIN']
  ty = None
  for sy, wt in zip(syid, w):
    prty, poty = sy[:2], sy[2:4]
    if len(sy)==6: syty=sy[-2:] # ga or gb (can also use later for am AMPA vs nm NMDA)
    for nc in tD[poty]['predi'][prty]:
      nc.weight[0]=wt/(2*tD[poty]['lambda'][prty] + 1) # denominator will be to big at the edges since no wraparound

def connect (kpr, kpo, tD):
  global dbl
  lam = tD[kpr]['lambda'][kpo]
  for npost,cepost in enumerate(tD[kpo]['cel']):
    if not kpr in tD[kpo]['predi']: tD[kpo]['predi'][kpr] = [] # or can use get()
    for pre in range(npost-lam, npost+lam+1):
      if pre >= 0 and pre < tD[kpo]['num']: # no wraparound
        if kpr=='RE' and pre==50: dbl.append(cepost)
        tD[kpo]['predi'][kpr].append(h.NetCon(tD[kpr]['cel'][pre].soma[0](0.5)._ref_v, 
                                              cepost.__getattribute__(tD[kpr]['targ'][kpo]), 
                                              0, axondelay, 1, sec=tD[kpr]['cel'][pre].soma[0]))
def insertchans ():
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
      
def setchans (mun=3, pnafjr=0.0, gnamult=1.0, gcabar=None, gcavfac=1.0, tyli=['TC', 'RE', 'PY', 'IN']):
  it2= it2l[mun]
  ms = h.MechanismStandard(it2, 1)
  print "Using %s channels"%it2
  gcab = gcabar if gcabar else 3e-3
  for k in ['TC', 'RE']:
    vals=thalDict[k]
    for ce in vals['cel']:
      ce.soma[0].gnabar_hh2nafjr = pnafjr *  gnamult * vals['gnabar'] # what is this??
      ce.soma[0].gnabar_hh2  =  (1-pnafjr) * gnamult * vals['gnabar']
  for ce in thalDict['RE']['cel']: # just set the RE one for now; corrD=3.777 for surface correction (Cav32RE3cc.hoc:105:257)
    sec=ce.soma[0]
    for v in thalDict['RE']['T'].values(): sec.__setattr__(v, 0.0) # turn all off
    sec.__setattr__(thalDict['RE']['T'][it2], gcab*gcavfac)

def zeroselfs ():
  selfconns = [nc for nc in h.List('NetCon') if nc.precell()==nc.postcell()]
  for nc in selfconns:
    for x in range(int(nc.wcnt())):
      nc.weight[x]=0.0

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

def allsetup ():
  global thalDict
  thalDict = mkcells() # creates dict used for cell lists and all other lists
  mksyns(thalDict)
  insertchans() # special Na chan, Ca chans
  recv()  # record vol
  setchans() # type and density of channels
  assignSyns() # sets weights
  # zeroselfs() # remove self connections
  setstims()

allsetup()

'''
COMMENT: testing sequence when opened from interpreter
import knox as kx
reload(kx)
td=tD=thalDict = kx.mkcells()
kx.thalDict=td # set up the global
kx.mksyns(td)
kx.setup()
kx.recv()
kx.setchans() # used to be setparams()
kx.assignSyns()
kx.zeroselfs() # remove self connections
kx.setstims()
import graph as g
g.mkfig() # 1 time only
g.TCraster(kx.thalDict)
'''
