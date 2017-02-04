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
for x in soma: x.ena=50

def ae ():
  for x,v in zip(np.linspace(0,1,len(vvec)),vvec):
    v.record(soma(x)._ref_v) 
    nc=h.NetCon(soma(x)._ref_v, None, sec=soma)
    ncl.append(nc)
    nc.threshold=-20
    nc.record(svec,ivec)

def af (g):
  h.printf("Velocity: %0.2f m/s;  ",1/(svec.o(2).max()-svec.o(0).max()))
  h.printf("1st vs 2nd half: ")
  ["%0.2f m/s "%(0.5/(svec.o(i+1).max()-svec.o(i).max()))]
  h.printf(" (ena=%d mV)\n",ena)
  for i in range(2): vvec.o(i).line(g,dt,i+1,4)
  g.size(0,5,-70,50)

ae() 
h.run() 

gg = [h.Graph() for i in range(2)]
af(gg[0])
ena=5
h.run() 
af(gg[1])
