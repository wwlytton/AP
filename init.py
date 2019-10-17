from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()	
simConfig = cfg
sim.createSimulateAnalyze(simConfig = cfg, netParams = netParams)
