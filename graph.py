'''
USAGE:
'''

def mkfig ():
  global fig,axi
  fig, axi = plt.subplots(6, 1)

tvec=h.Vector(len(d[0][1])).indgen(h.dt)

def replot (w=2, col='b'):
  for ax in axi: ax.clear()
  for ax in axi: ax.set_ylim(-120,50) 
  for ax, d1 in zip(axi, d): ax.plot(tvec, d1[1], linewidth=w, color=col)
