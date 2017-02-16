""" cfg.py """
from netpyne import specs
D = specs.Dict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 1.0*1e3 
# cfg.dt = 0.05
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 44.3}
cfg.verbose = 1
cfg.cvode_active = False
cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.0, 'var': 'v'}}
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.2, 'var': 'v'}}
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.4, 'var': 'v'}}
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.6, 'var': 'v'}}
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.8, 'var': 'v'}}
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 1.0, 'var': 'v'}} # don't want to get too close to the end
cfg.recordStims = False  
cfg.recordStep = 0.1 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
# cfg.analysis.plotTraces = D({'include': ['axA'], 'oneFigPer': 'cell', 'saveFig': True, 
#                              'showFig': True, 'figSize': (10,8), 'timeRange': [0,cfg.duration]})

# Parameters
cfg.percnajr, cfg.rall, cfg.gnabar = 0.1, 5.18, 0.2

# Current inputs 
cfg.addstim = 1
cfg.stim = D({'popu': 'axA', 'sec': 'axon', 'loc': 0.0, 'start': 0, 'dur': 5, 'amp': 2.0}) # avoid word pop since that's a builtin method
