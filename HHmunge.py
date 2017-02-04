from neuron import h
vvec = [h.Vector() for i in range(3)]
svec, ivec = h.Vector(), h.Vector()
ncl =  []

soma=h.Section()
soma.nseg=100
soma.L=1e3
soma.diam=10
soma.insert('hh')
soma.gnabar_hh, soma.gkbar_hh, soma.gl_hh, soma.el_hh = 0.12, 0.036, 3e-4, -54.3  # set for all segments with underscore notation

stim=h.IClamp()
stim.loc(0.0,sec=soma)
stim.amp=2
stim.dur=5
ena=50
for x in soma: x.ena=ena

def ae ():
  for x,v,i in zip(np.linspace(0,1,len(vvec)),vvec,range(len(vvec))):
    v.record(soma(x)._ref_v) 
    nc=h.NetCon(soma(x)._ref_v, None, sec=soma)
    ncl.append(nc)
    nc.threshold=-20
    nc.record(svec,ivec,i+1)

def af (g):
  h.printf("Velocity: %0.2f m/s;  ",1/(svec[-1] - svec[0]))
  h.printf("Instant speeds: ")
  print ["%0.2f m/s "%x for x in np.diff(svec)]
  h.printf(" (ena=%d mV)\n",ena)
  for v in vvec: v.line(g, h.dt, i+1, 4)
  g.size(0,5,-70,50)

ae() 
h.run() 

gg = [h.Graph() for i in range(2)]
af(gg[0])
ena=5
h.run() 
af(gg[1])
