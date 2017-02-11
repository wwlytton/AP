from neuron import h
import axonA
vvec = [h.Vector() for i in range(3)]
svec, ivec = h.Vector(), h.Vector()
ncl =  []

axon=axonA.AxonA()
axon.axon.nseg=100
axon.axon.gnabar_hh, axon.axon.gkbar_hh, axon.axon.gl_hh, axon.axon.el_hh = 0.12, 0.036, 3e-4, -54.3  # set for all segments with underscore notation

stim=h.IClamp()
stim.loc(0.0,sec=axon.axon)
stim.amp=2
stim.dur=5
ena=50
def setena (en=50):
  global ena
  ena=en
  for x in axon.axon: x.ena=ena

def ae ():
  for x,v,i in zip(np.linspace(0,1,len(vvec)),vvec,range(len(vvec))):
    v.record(axon.axon(x)._ref_v) 
    nc=h.NetCon(axon.axon(x)._ref_v, None, sec=axon.axon)
    ncl.append(nc)
    nc.threshold=-20
    nc.record(svec,ivec,i+1)

def af (g):
  if (len(svec)>1): 
    h.printf("Velocity: %0.2f m/s;  ",axon.axon.L/(svec[-1] - svec[0])*1e-3)
    h.printf("Instant speeds: ")
    print ["%0.2f m/s "%(axon.axon.L/(len(svec)-1)/x*1e-3) for x in np.diff(svec)]
  else:
    h.printf("only %d spikes: \n",len(svec))
    svec.printf()
  h.printf(" (ena=%d mV)\n",ena)
  for i,v in enumerate(vvec): v.line(g, h.dt, i+1, 4)
  g.size(0,5,-70,50)

def ge (): [g.erase_all() for g in gg]

'''
ae() 
h.run() 
gg = [h.Graph() for i in range(2)]
af(gg[0])
setena(5)
h.run() 
af(gg[1])
'''
