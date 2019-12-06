import wlutils as wl
import numpy as np
from netpyne import sim
from simConfig import cfg
from netParams import npar
sim.create(npar, cfg)
ax = sim.net.cells[0].secs.axon.hObj
for perc in np.linspace(0, 0.8, 0.1):
  h.perc_ina2005 = perc
  sim.runSim()
  sim.saveData(include = ['simData'], filename = '19dec06%d'%(100*perc))

