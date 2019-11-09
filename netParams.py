from netpyne import specs
try:
	from __main__ import cfg  # import SimConfig object with params from parent module
except:
	from cfg import cfg
	
netParams = specs.NetParams()   # object of class NetParams to store the network parameters
cellRule=netParams.importCellParams(label='axA', conds={'cellType': 'axA'}, fileName='axonA.py', cellName='AxonA', 
                               cellArgs={'percnajr':0.5, 'rall':34.5, 'gnabar':0.12})
netParams.popParams.axA = {'cellType': 'axA', cellModel: 'HH', 'numCells': 1}

axr.secs.axon.ions.na.e = cfg.percnajr
axr.secs.axon.mechs.hh.gnabar = cfg.gnabar

ic = cfg.stim
netParams.stimSourceParams.stim = {'type': 'IClamp', 'delay': 0, 'dur': ic['dur'], 'amp': ic['amp']}
netParams.stimTargetParams.stimaxon = {'source': 'stim', 'conds': {'popLabel': ic['popu']}, 'sec': ic['sec'], 'loc': ic['loc']}
