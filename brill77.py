# execfile('test.py')
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

def setup ():
  global myel,nodl,stim
  h.load_file('brill77/cable.hoc')  # make(50, 1000) is called at bottom of file; 50 nodes with 1e3 internode interval
  h.tstop = 10
  myel = [x for x in h.allsec() if 'myel' in str(x)]
  nodl = [x for x in h.allsec() if 'node' in str(x)]
  stim=h.IClamp(0.5,sec=h.node[0])
  stim.delay, stim.dur, stim.amp = 0, 0.1, 5
  for n in nodl: 
    n.insert('nafjr')
    n(0.5).nafjr.gnabar=0.0

def setparams (pnafjr=0.0, gnabar=1.2):
  for n in nodl:
    n(0.5).nafjr.gnabar = pnafjr*gnabar
    n(0.5).hh.gnabar = (1-pnafjr)*gnabar

def mkfig (): 
  global fig,axi
  fig, axi = plt.subplots(1, 1)

def gr ():
  g=h.Graph()
  g.size(0, h.tstop, -80, 50)
  g.addvar("node0", h.node[0](0.5)._ref_v,1,2)
  g.addvar("node1", h.node[1](0.5)._ref_v,3,2)
  g.addvar("node25", h.node[25](0.5)._ref_v,4,2)
  g.addvar("node49",h.node[49](0.5)._ref_v,2,2)
  h.graphList[0].append(g)

def plotv (name='', label=''):
  if fig is None: mkfig()
  axi.clear()
  xval = np.linspace(0, h.tstop, len(nrec[0]))
  for x in nrec: plt.plot(xval,x)
  if label: plt.title(label, fontdict={'family':'sansserif','color':'black','weight': 'bold','size': 36})
  if name: plt.savefig(name)
    
def recv (thresh=35):
  global nrec
  spkt, spkid = h.Vector(len(nodl)+10), h.Vector(len(nodl)+10)
  ncl = [h.NetCon(sec(0.5)._ref_v, None, sec=sec) for sec in nodl]
  for nc in ncl: nc.threshold=thresh
  nrec = [h.Vector(h.tstop/h.dt+10) for x in range(len(nodl))]
  for i,nc in enumerate(ncl): nc.record(spkt,spkid, i)  # netcon.record(tvec, idvec, id)
  for v,n in zip(nrec,nodl): v.record(n(0.5)._ref_v)

def speed ():
  global spv, Ltot, dist, vel
  Ltot = sum([x.L for x in h.allsec()])
  ndist = nodl[0].L + myel[0].L # 1003.183
  spv = ndist/np.diff(spkt)/1e3  # somehow alternative values
  maxt = [vec.max_ind()*h.dt for vec in nrec]
  vel = ndist/np.diff(maxt)/1e3

def rf (name='', svfig=True, svdata=True):
  if svdata: fp = open('data/%s%s.pkl'%(datestr,name), 'w')
  for x in np.linspace(0,1.0,6):
    print x, 
    setparams(pnafjr=x)
    h.run()
    if svfig: plotv('gif/%s%s_pnafjr%d.png'%(datestr,name,x*100), '%d%% mutated Naf'%(x*100))
    if svdata: pkl.dump(nrec, fp)
  if svdata: fp.close()

def rdpklf (file=''):
  with open(file) as f:
    d.append(pkl.load(f)) 

setup()
setparams()
recv()
# mkfig()
def run ():
  h.run()  
  plotv()
