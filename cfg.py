""" cfg.py """
from netpyne import specs
D = specs.Dict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 1.0*1e3 
# cfg.dt = 0.05
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
# cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 1
cfg.cvode_active = False
cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'V_axon': {'sec': 'axon', 'loc': 0.5, 'var': 'v'}}
cfg.recordStims = False  
cfg.recordStep = 0.1 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = D({'include': ['axA'], 'oneFigPer': 'cell', 'saveFig': True, 
                             'showFig': True, 'figSize': (10,8), 'timeRange': [0,cfg.duration]})

# Parameters
cfg.percnajr, cfg.rall, cfg.gnabar = 0.5, 34.5, 0.12

# Current inputs 
cfg.addstim = 1
cfg.stim = D({'popu': 'axA', 'sec': 'axon', 'loc': 0.0, 'start': 0, 'dur': 5, 'amp': 2.0}) # avoid word pop since that's a builtin method
