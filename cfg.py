from netpyne import specs
from netpyne.specs import Dict, ODict

simConfig = cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 10
# cfg.dt = 0.05
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 37}
cfg.verbose = 1
cfg.cvode_active = False
cfg.printRunTime = 1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordCells = [0]
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

# Parameters
cfg.percnajr, cfg.rall, cfg.gnabar = 90.0, 101, 0.5

# Current inputs 
cfg.addstim = 1
cfg.stim = Dict({'popu': 'axA', 'sec': 'axon', 'loc': 0.0, 'start': 0, 'dur': 2, 'amp': 0.2}) # avoid word pop since that's a builtin method
