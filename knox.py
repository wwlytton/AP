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
  thalDict = {'TC': (TCsl, TCsl[0].soma[0].gnabar_hh2), 
              'RE': (TCsl, REsl[0].soma[0].gnabar_hh2),
              'PY': (TCsl, PYsl[0].soma[0].gnabar_hh2),
              'IN': (INsl, TCsl[0].soma[0].gnabar_hh2)}

def setup ():
  for ty in [TCsl, REsl, PYsl, INsl]:
    for ce in ty:
      ce.soma[0].insert('hh2nafjr')
      ce.soma[0].gnabar_hh2nafjr = 0.0

def setparams (pnafjr=0.0, gnabar=0.1, cli=REsl):
  for ce in cli:
    ce.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
    ce.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar

mksecls()
setup()
setparams()
