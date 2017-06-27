from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

h.load_file('Knox_Absence_model/Fspikewave.oc')
h.cvode_active(1)
h.trans=0 # this means don't read from SaveState
h.run()

'''
# need a Ca channel -- start with WT
seclist = h.SectionList()
seclist.wholetree()

def setup ():
  h.soma[0].insert('hh2nafjr')
  h.soma[0].gnabar_hh2nafjr = 0.0
  for sec in seclist: 
    for mech in it2l:
      sec.insert(mech)
      h('%s.gcabar_%s = 0.0'%(str(sec),mech))

def setparams (it2=it2l[0], pnafjr=0.0, gnabar=0.1):
  h.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
  h.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar
  h('soma.gcabar_%s = %g'%(it2, 4.5e-5)) #  h.soma[0](0.5).it2WT.gcabar
  h('dend1[0].gcabar_%s = %g'%(it2, h.corrD*4.5e-5))
  h('dend1[1].gcabar_%s = %g'%(it2, h.corrD*6.8e-4))

setup()
setparams()
'''
