from netpyne import specs
from netpyne.specs import Dict, ODict

cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 10
cfg.dt = 0.01
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 37}
cfg.verbose = 1
cfg.cvode_active = False
cfg.printRunTime = 1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordCells = [0]
nlocs=20
cfg.recordTraces = {'V_axon_%.2f'%x : {'sec': 'axon', 'loc': x, 'var': 'v'} for x in np.linspace(0, 1, nlocs+1)}
cfg.recordStims = False
cfg.recordStep = cfg.dt

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
