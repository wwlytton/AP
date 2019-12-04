from netpyne import specs
	
npar = specs.NetParams()   # object of class NetParams to store the network parameters
npar.popParams.axA = {'cellType': 'axA', 'cellModel': 'ax', 'numCells': 1}
npar.cellParams['PYRrule'] = {'conds':{'cellType': 'axA', 'cellModel': 'ax'},
   'secs': {'axon': {'geom': {'diam': 1, 'L': 2000, 'Ra': 123.0, 'nseg': 1000}, 
                     'ions': {'k': {'e': -77.0}, 'na': {'e': 50.0}},
                     'mechs':{'ina2005': {'gnatbar': 0.3}, 'ik2005': {'gkfbar': 0.3}, 'pas': {'g': 0.0001, 'e': -70.0}}}}}

# cellRule=npar.importCellParams(label='axA', conds={'cellType': 'axA'}, fileName='axonA.py', cellName='AxonA', cellArgs={'percnajr':0.5, 'rall':34.5, 'gnabar':0.12})
# axr.secs.axon.ions.na.e = cfg.percnajr
# axr.secs.axon.mechs.hh.gnabar = cfg.gnabar

# cfg.stim = Dict({'popu': 'axA', 'sec': 'axon', 'loc': 0.0, 'start': 0, 'dur': 2, 'amp': 0.2}) # avoid word pop since that's a builtin method
npar.stimSourceParams.stim = {'type': 'IClamp', 'delay': 0, 'dur': 0.5, 'amp': 0.2}
npar.stimTargetParams.stimaxon = {'source': 'stim', 'conds': {'popLabel': 'axA'}, 'sec': 'axon', 'loc': 0.0}
