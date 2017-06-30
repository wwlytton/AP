'''
USAGE:
import brill77 as br
h.run()
br.plotv()
br.rf() # to run a set of sims
'''

# execfile('test.py')
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

# simulation defs
def setup ():
  global myel,nodl,stim,distl
  h.load_file('brill77/cable.hoc')  # make(50, 1000) is called at bottom of file; 50 nodes with 1e3 internode interval
  h.tstop = 10
  myel = [x for x in h.allsec() if 'myel' in str(x)]
  nodl = [x for x in h.allsec() if 'node' in str(x)]
  h.distance(0,0.5,sec=h.node[0])
  distl = [h.distance(0.5,sec=sec) for sec in nodl]
  stim=h.IClamp(0.5,sec=h.node[0])
  stim.delay, stim.dur, stim.amp = 0, 0.1, 5
  for n in nodl: 
    n.insert('nafjr')
    n(0.5).nafjr.gnabar=0.0

def setparams (pnafjr=0.0, gnabar=1.2):
  for nod in nodl:
    for n in nod:
      n.nafjr.gnabar = pnafjr*gnabar
      n.hh.gnabar = (1-pnafjr)*gnabar

def hhit ():
  'make it more hh squid axon in terms of temp, Ra, diam'
  stim.amp=30000
  h.celsius=6.3
  diam = 500
  h('forall {Ra=34.5 cm=1}')
  for x in myel:
    x.L=3.183
    x.diam=diam
    x.nseg=1
  for x in nodl:
    x.L=1000
    x.diam=diam
    x.nseg=100
    
# graphics and data figs
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
  plt.xlim(0,h.tstop); plt.ylim(-80,50)
  if label: plt.title(label, fontdict={'family':'sansserif','color':'black','weight': 'bold','size': 36})
  if name: plt.savefig(name)
    
# recording
def recv (thresh=35):
  global nrec
  spkt, spkid = h.Vector(len(nodl)+10), h.Vector(len(nodl)+10)
  ncl = [h.NetCon(sec(0.5)._ref_v, None, sec=sec) for sec in nodl]
  for nc in ncl: nc.threshold=thresh
  nrec = [h.Vector(h.tstop/h.dt+10) for x in range(len(nodl))]
  for i,nc in enumerate(ncl): nc.record(spkt,spkid, i)  # netcon.record(tvec, idvec, id)
  for v,n in zip(nrec,nodl): v.record(n(0.5)._ref_v)

# calculate speed
def speed (tl, beg=2, end=-3): 
  'takes vector of times (length # of nodes); defaults beg 2 and end -3 to avoid edge effects'
  if len(tl)!=len(distl): raise Exception('time list wrong length; should be %d'%(len(distl)))
  return round((br.distl[end]-br.distl[beg])/(tl[end]-tl[beg])/1e3, 3)

def speed1 ():
  'speed1() reads from current sim'
  global spv, Ltot, dist, vel
  Ltot = sum([x.L for x in h.allsec()])
  ndist = nodl[0].L + myel[0].L # 1003.183
  spv = ndist/np.diff(spkt)/1e3  # somehow alternative values
  maxt = [vec.max_ind()*h.dt for vec in nrec]
  vel = ndist/np.diff(maxt)/1e3

def rf (vals=np.linspace(0, 1.0, 6), name='', svfig=True, svdata=True):
  if svdata: fp = open('data/%s%s.pkl'%(datestr,name), 'w')
  for x in vals:
    print x, 
    setparams(pnafjr=x)
    h.run()
    if svfig: plotv('gif/%s%s_pnafjr%d.png'%(datestr,name,x*100), '%d%% mutated Naf'%(x*100))
    if svdata: pkl.dump((x*100, nrec), fp)
  if svdata: fp.close()

setup()
setparams()
recv()
# mkfig()
def run ():
  h.run()  
  plotv()
