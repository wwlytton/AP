# execfile('test.py')
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt

h.load_file('stdrun.hoc')
h.tstop = 6

h.load_file('brill77/cable.hoc')  # make(50, 1000) is called at bottom of file; 50 nodes with 1e3 internode interval
stim=h.IClamp(0.5,sec=h.node[0])
stim.delay, stim.dur, stim.amp = 0, 0.1, 10

g=h.Graph()
g.size(0, h.tstop, -80, 50)
g.addvar("node0", h.node[0](0.5)._ref_v,1,2)
g.addvar("node1", h.node[1](0.5)._ref_v,3,2)
g.addvar("node25", h.node[25](0.5)._ref_v,4,2)
g.addvar("node49",h.node[49](0.5)._ref_v,2,2)
h.graphList[0].append(g)
h.run()


