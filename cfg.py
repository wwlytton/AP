""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 10
# cfg.dt = 0.05
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 6.3}
cfg.verbose = 1
cfg.cvode_active = False
cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'V_axon_0.0': {'sec': 'axon', 'loc': 0.0, 'var': 'v'},
                    'V_axon_0.2': {'sec': 'axon', 'loc': 0.2, 'var': 'v'},
                    'V_axon_0.4': {'sec': 'axon', 'loc': 0.4, 'var': 'v'},
                    'V_axon_0.6': {'sec': 'axon', 'loc': 0.6, 'var': 'v'},
                    'V_axon_0.8': {'sec': 'axon', 'loc': 0.8, 'var': 'v'},
                    'V_axon_1.0': {'sec': 'axon', 'loc': 1.0, 'var': 'v'}}
cfg.recordStims = False  
cfg.recordStep = 0.05 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = Dict({'include': ['axA'], 'oneFigPer': 'cell', 'saveFig': False, 
                             'showFig': False, 'figSize': (10,8), 'timeRange': [0,cfg.duration]})

# Parameters
cfg.percnajr, cfg.rall, cfg.gnabar = 90.0, 101, 0.5

# Current inputs 
cfg.addstim = 1
cfg.stim = Dict({'popu': 'axA', 'sec': 'axon', 'loc': 0.0, 'start': 0, 'dur': 5, 'amp': 2.0}) # avoid word pop since that's a builtin method
