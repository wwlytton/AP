''' USAGE example
ModelDB#
/u/billl/articles/jnsci25:4844.pdf
Iuliia Vitko, Yucai Chen, Juan M. Arias, Yen Shen, Xi-Ru Wu and Edward Perez-Reyes (2005)
Functional Characterization and Neuronal Modeling of the Effects of Childhood Absence Epilepsy Variants of CACNA1H, a T-Type Calcium Channel. J Neurosci 25:4844-4855
in simulations of the network, only REs were altered

import Cav32 as cv
print cv.it2l # the list of items
cv.setparams(it2=cv.it2l[0], pnafjr=0.0) # WT control
h.run()
cv.setparams(it2=cv.it2l[1], pnafjr=0.0) # test one of the cav mutants without compensation
cv.setparams(it2=cv.it2l[1], pnafjr=0.7) # test one of the cav mutants with 1/2 naf mutant
cv.setparams(it2=cv.it2l[2], pnafjr=0.0) # test one of the cav mutants without compensation
cv.setparams(it2=cv.it2l[2], pnafjr=0.5) # test one of the cav mutants with 1/2 naf mutant
'''

from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()
it2l = ['it2WT', 'it2C456S', 'it2R788C']

# just work with 3 compartment cell for now re3_cc, also re1 and re80, and reD (dissociated cell)
# have different demos in Cav32_WT (wild type); Cav32_R788C; Cav32_C456S
h.load_file('Cav32RE3cc.hoc')

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

def setparams (mun=0, pnafjr=0.0, gnabar=0.1, gnafac=1.0, gcavfac=1.0):
  '''Set mutant # mun, pnafjr proportion, na channel total density'''
  it2=it2l[mun]
  h.soma[0].gnabar_hh2nafjr = pnafjr *gnabar*gnafac
  h.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar*gnafac
  h('soma.gcabar_%s = %g'%(it2, 4.5e-5*gcavfac)) #  h.soma[0](0.5).it2WT.gcabar
  h('dend1[0].gcabar_%s = %g'%(it2, h.corrD*4.5e-5*gcavfac))
  h('dend1[1].gcabar_%s = %g'%(it2, h.corrD*6.8e-4*gcavfac))

# recording and run
def recv (thresh=-5):
  global vvec
  vvec = h.Vector(h.tstop/h.dt+10)
  vvec.record(h.soma[0](0.5)._ref_v)

def rf (vals=np.linspace(0, 1.0, 6), name='', mun=0, svfig=False, svdata=True):
  if svdata: 
    filestem = '%s%s%s'%(datestr,name,it2l[mun])
    fp = open('data/%s.pkl'%(filestem), 'w')
  for x in vals:
    print x, 
    setparams(pnafjr=x, mun=mun)
    h.run()
    if svfig: plotv('gif/%s_pnafjr%d.png'%(filestem,x*100), '%d%% mutated Naf'%(x*100))
    if svdata: pkl.dump((x*100, vvec), fp)
  if svdata: fp.close()
  return 'data/%s.pkl'%(filestem)

setup()
setparams()
