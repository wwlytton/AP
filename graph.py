'''
USAGE:
'''

tvec=None

def mkfig ():
  global fig,axi
  fig, axi = plt.subplots(6, 1)

def replot (d, w=2, col='b'):
  if not tvec: tvec=h.Vector(len(d[0][1])).indgen(h.dt)
  for ax in axi: ax.clear()
  for ax in axi: ax.set_ylim(-120,50) 
  for ax, d1 in zip(axi, d): ax.plot(tvec, d1[1], linewidth=w, color=col)
