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

def setparams (it2=it2l[0], pnafjr=0.0, gnabar=0.1):
  h.soma[0].gnabar_hh2nafjr = pnafjr *gnabar
  h.soma[0].gnabar_hh2  =  (1-pnafjr)*gnabar
  h('soma.gcabar_%s = %g'%(it2, 4.5e-5)) #  h.soma[0](0.5).it2WT.gcabar
  h('dend1[0].gcabar_%s = %g'%(it2, h.corrD*4.5e-5))
  h('dend1[1].gcabar_%s = %g'%(it2, h.corrD*6.8e-4))

def rf (vals=np.linspace(0, 1.0, 6), name='', svfig=False, svdata=True):
  if svdata: fp = open('data/%s%sCav32.pkl'%(datestr,name), 'w')
  for x in vals:
    print x, 
    setparams(pnafjr=x)
    h.run()
    if svfig: plotv('gif/%s%s_pnafjr%d.png'%(datestr,name,x*100), '%d%% mutated Naf'%(x*100))
    if svdata: pkl.dump((x*100, nrec), fp)
  if svdata: fp.close()

setup()
setparams()
