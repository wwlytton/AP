from netpyne import sim

from cfg import cfg
cfg, netParams = sim.readCmdLineArgs()	
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
sim.analyze()
