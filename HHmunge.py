from neuron import h
ncl,vvec,svec,g=[[]]*4
for i in range(2): g.append(h.Graph()) 
vvec = [h.Vector() for i in range(3)]
svec, ivec = h.Vector(), h.Vector()

soma=h.Section()
soma.nseg=100
soma.L=1e3
soma.diam=10
soma.insert('hh')
soma.gnabar_hh, soma.gkbar_hh, soma.gl_hh, soma.el_hh = 0.12, 0.036, 3e-4, -54.3  # set for all segments with underscore notation

stim=h.IClamp()
stim.loc(0.0)
stim.amp=2
stim.dur=5
for x in soma: x.ena=50

for v,x in zip(
[v.record(soma(x)._ref_v) 
    ncl.append(h.NetCon(&v(x),nil)) 
    ncl.o(i).threshold=-20
    ncl.o(i).record(svec.o(i)) 

def af () : local i,j
  j=$1
  printf("Velocity: %0.2f m/s;  ",1/(svec.o(2).max()-svec.o(0).max()))
  printf("1st vs 2nd half: ")
  for i=0,1 printf("%0.2f m/s ",0.5/(svec.o(i+1).max()-svec.o(i).max()))
  printf(" (ena=%d mV)\n",ena)
  for i=0,2 vvec.o(i).line(g[j],dt,i+1,4)
  g[j].size(0,5,-70,50)

ae() 
run() 
af(0)

ena=5
run() 
af(1)


