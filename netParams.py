from netpyne import specs
from netpyne.specs import Dict, ODict
from cfg import cfg

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
axr=netParams.importCellParams(label='axA', conds={'cellType': 'axA'}, fileName='axonA.py', cellName='AxonA', cellArgs={'percnajr':cfg.percnajr, 'rall':cfg.rall, 'gnabar':cfg.gnabar})
netParams.popParams.axA = Dict({'cellType': 'axA', 'numCells': 1})

ic = cfg.stim
netParams.stimSourceParams.stim = Dict({'type': 'IClamp', 'delay': 0, 'dur': ic['dur'], 'amp': ic['amp']})
netParams.stimTargetParams.stimaxon = Dict({'source': 'stim', 'conds': {'popLabel': ic['popu']}, 'sec': ic['sec'], 'loc': ic['loc']})

