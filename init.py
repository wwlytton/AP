from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()	
sim.createSimulateAnalyze(simConfig = cfg, netParams = netParams)
sim.saveData()
