from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
fig, axi = None, None
datestr = os.popen('datestring').read()

h.load_file('Fspikewave.oc')
def mksecls (): 
  global TCsl, REsl, PYsl, INsl
  TCsl, REsl, PYsl, INsl = [h.SectionList() for i in range(4)]
  for i in range(int(h.nthalamiccells)):
    TCsl.append(h.IN[i]) 
    REsl.append(h.IN[i])
    PYsl.append(h.IN[i])
    INsl.append(h.IN[i]) 

def setup ():
  for ty in mksecls:
    for ce in ty:
      ce.soma[0].insert('hh2nafjr')
      ce.soma[0].gnabar_hh2nafjr = 0.0

def setparams (pnafjr=0.0, gnabar=0.1, cli='REsl'):
  for ce in cli:
    ce.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
    ce.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar

mksecls()
setup()
setparams()

