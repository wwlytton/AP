'''
USAGE:
'''

def setparams (pnafjr=0.0, gnabar=1.2):
  soma.gnabar_nafjr =  pnafjr*gnabar
  soma.gnabar_hh = (1-pnafjr)*gnabar

soma=h.Section(name='soma')
soma.insert('hh')
soma.insert('nafjr')
soma(0.5).nafjr.gnabar
soma.gnabar_nafjr=0
stim = h.IClamp(soma(0.5))
stim.dur, stim.delay, stim.amp = 10, 2, 0
h.tstop=10
fig, axi = plt.subplots(1, 1)
axi.clear()
tvec=h.Vector()
vecl=[h.Vector()]
tvec.record(h._ref_t)
vecl[0].record(soma(0.5)._ref_v)

# sim runs
setparams(0.0)
h.run()
plt.plot(tvec,vecl[0],color='red',linewidth=5)
setparams(1.0)
plt.plot(tvec,vecl[0],color='blue',linewidth=5)
