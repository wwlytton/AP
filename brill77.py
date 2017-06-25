# execfile('test.py')
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt

h.load_file('stdrun.hoc')
h.tstop = 6

h.load_file('brill77/cable.hoc')  # make(50, 1000) is called at bottom of file; 50 nodes with 1e3 internode interval
stim=h.IClamp(0.5,sec=h.node[0])
nodl = [x for x in h.allsec() if 'node' in str(x)]
myel = [x for x in h.allsec() if 'myel' in str(x)]
stim.delay, stim.dur, stim.amp = 0, 0.1, 10

def mkfig (): 
  global fig,axi
  fig, axi = plt.subplots(1, 1)
mkfig()

def gr ():
  g=h.Graph()
  g.size(0, h.tstop, -80, 50)
  g.addvar("node0", h.node[0](0.5)._ref_v,1,2)
  g.addvar("node1", h.node[1](0.5)._ref_v,3,2)
  g.addvar("node25", h.node[25](0.5)._ref_v,4,2)
  g.addvar("node49",h.node[49](0.5)._ref_v,2,2)
  h.graphList[0].append(g)

def plot ():
  axi.clear()
  xval = np.linspace(0, h.tstop, len(nrec[0]))
  for x in nrec: plt.plot(xval,x)

def recv (thresh=35):
  global nrec
  spkt, spkid = h.Vector(len(nodl)+10), h.Vector(len(nodl)+10)
  ncl = [h.NetCon(sec(0.5)._ref_v, None, sec=sec) for sec in nodl]
  for nc in ncl: nc.threshold=thresh
  nrec = [h.Vector(h.tstop/h.dt+10) for x in range(len(nodl))]
  for i,nc in enumerate(ncl): nc.record(spkt,spkid, i)  # netcon.record(tvec, idvec, id)
  for v,n in zip(nrec,nodl): v.record(n(0.5)._ref_v)

def speed ():
  global spv, Ltot, dist
  Ltot = sum([x.L for x in h.allsec()])
  ndist = nodl[0].L + myel[0].L # 1003.183
  spv = ndist/np.diff(spkt)/1e3  # somehow alternative values

recv()
h.run()  
axi.clear()
plot()

