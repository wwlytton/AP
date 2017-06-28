from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

h.load_file('Knox_Absence_model/Fspikewave.oc')

def setup ():
  h.trans=0 # this means don't read from SaveState
  if False:
    h.soma[0].insert('hh2nafjr')
    h.soma[0].gnabar_hh2nafjr = 0.0

def setparams (pnafjr=0.0, gnabar=0.1):
  if False:
    h.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
    h.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar

setup()
setparams()

