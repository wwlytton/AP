'''
USAGE:
loaddll('/u/billl/nrniv/AP')
import basicHH as hh
from basicHH import stim, tvec, vecl, axi, setparams # so can reset stim and do plots
'''

from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

def setparams (pnafjr=0.0, gnabar=1.2):
  soma.gnabar_nafjr =  pnafjr*gnabar
  # soma.gnabar_hh = (1.0-pnafjr)*gnabar
  return 1.0

soma=h.Section(name='soma')
soma.insert('hh')
soma.insert('nafjr')
soma.gnabar_nafjr=0
stim = h.IClamp(soma(0.5))
stim.delay, stim.dur, stim.amp = 0, 1, 15
h.tstop=10
fig, axi = plt.subplots(1, 1)
tvec=h.Vector()
vecl=[h.Vector()]
tvec.record(h._ref_t)
vecl[0].record(soma(0.5)._ref_v)

# sim runs
axi.clear()
setparams(0.0)
h.run()
plt.plot(tvec,vecl[0],color='red',linewidth=5)
# setparams(1.0)
plt.plot(tvec,vecl[0],color='blue',linewidth=5)
