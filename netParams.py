# from cfg import simConfig
from netpyne import specs
from cfg import cfg
	
netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams.axA = {'cellType': 'axA', 'cellModel': 'ax', 'numCells': 1}
netParams.cellParams['PYRrule'] = {'conds':{'cellType': 'axA', 'cellModel': 'ax'},
   'secs': {'axon': {'geom': {'diam': 5, 'L': 2000, 'Ra': 123.0}, 
                     'ions': {'k': {'e': -77.0}, 'na': {'e': 50.0}},
                     'mechs':{'ina2005': {'gnatbar': 0.3}, 'ik2005': {'gkbar': 0.3}, 'pas': {'g': 0.0001, 'e': -70.0}}}}}

# cellRule=netParams.importCellParams(label='axA', conds={'cellType': 'axA'}, fileName='axonA.py', cellName='AxonA', cellArgs={'percnajr':0.5, 'rall':34.5, 'gnabar':0.12})
# axr.secs.axon.ions.na.e = cfg.percnajr
# axr.secs.axon.mechs.hh.gnabar = cfg.gnabar

ic = cfg.stim
netParams.stimSourceParams.stim = {'type': 'IClamp', 'delay': 0, 'dur': ic['dur'], 'amp': ic['amp']}
netParams.stimTargetParams.stimaxon = {'source': 'stim', 'conds': {'popLabel': ic['popu']}, 'sec': ic['sec'], 'loc': ic['loc']}
