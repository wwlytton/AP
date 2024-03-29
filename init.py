from netpyne import sim
from neuron import h
import wlutils as wl
import numpy as np
from netpyne import sim
from simConfig import cfg
from netParams import npar
sim.create(npar, cfg)
ax = sim.net.cells[0].secs.axon.hObj
def lp ():
    for perc in np.linspace(0.0, 0.8, 9): # now is percent block
        h.gnablock_ina2005 = perc # h.perc_ina2005
        sim.runSim()
        sim.gatherData()
        sim.saveData(include = ['simData'], filename = 'data/19dec06blkA_%02d'%(100*perc))

lp()
