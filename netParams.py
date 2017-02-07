from netpyne import specs
from cfg import cfg
netParams = specs.NetParams()   # object of class NetParams to store the network parameters
# PT cell params (6-comp)
cellRule = netParams.importCellParams(label='axA', conds={'cellType': 'axA', 'cellModel': 'HH_reduced'}, fileName='axonA.py', cellName='AxonA')

def setena (en=50):
  global ena
  ena=en
  for x in axon.axon: x.ena=ena

ena = cfg.ena
setena()

netParams.popParams['axA'] = {'cellModel': 'HH_reduced', 'cellType': 'axA', 'numCells': 1}

if cfg.addIClamp:	
  for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
    ic = getattr(cfg, iclabel, None)  # get dict with params
    netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'delay': ic['start'], 'dur': ic['dur'], 'amp': ic['amp']}
    netParams.stimTargetParams[iclabel+'_'+ic['pop']] = {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}
