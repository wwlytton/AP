from netpyne import specs
npar = specs.NetParams()

npar.popParams.axA = {'cellType': 'axA', 'cellModel': 'ax', 'numCells': 1}
npar.cellParams['PYRrule'] = {'conds':{'cellType': 'axA', 'cellModel': 'ax'},
   'secs': {'axon': {'geom': {'diam': 1, 'L': 5000, 'Ra': 123.0, 'nseg': 1000}, 
                     'ions': {'k': {'e': -77.0}, 'na': {'e': 50.0}},
                     'mechs':{'ina2005': {'gnabar': 0.3}, 'ik2005': {'gkfbar': 0.3}, 'pas': {'g': 0.0001, 'e': -70.0}}}}}

npar.stimSourceParams.stim = {'type': 'IClamp', 'delay': 0, 'dur': 0.5, 'amp': 0.2}
npar.stimTargetParams.stimaxon = {'source': 'stim', 'conds': {'popLabel': 'axA'}, 'sec': 'axon', 'loc': 0.0}

