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
    TCsl.append(h.IN[i].soma[0]) 
    REsl.append(h.IN[i].soma[0])
    PYsl.append(h.IN[i].soma[0])
    INsl.append(h.IN[i].soma[0]) 

def setup ():
  if False:
    h.soma[0].insert('hh2nafjr')
    h.soma[0].gnabar_hh2nafjr = 0.0

def setparams (pnafjr=0.0, gnabar=0.1):
  if False:
    h.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
    h.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar

mksecls()
setup()
setparams()

