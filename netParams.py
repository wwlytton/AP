from netpyne import specs
from cfg import cfg
netParams = specs.NetParams()   # object of class NetParams to store the network parameters
cellRule = netParams.importCellParams(label='axA', conds={'cellType': 'axA'}, fileName='axonA.py', cellName='AxonA')
netParams.popParams.axA = {'cellModel': 'HH_reduced', 'cellType': 'axA', 'numCells': 1}

cellRule.secs.axon.ions.na.e = cfg.enahh
cellRule.secs.axon.mechs.hh.gnabar = cfg.gnabarhh

ic = cfg.stim
netParams.stimSourceParams.stim = {'type': 'IClamp', 'delay': 0, 'dur': ic['dur'], 'amp': ic['amp']}
netParams.stimTargetParams.stimaxon = {'source': 'stim', 'conds': {'popLabel': ic['popu']}, 'sec': ic['sec'], 'loc': ic['loc']}
