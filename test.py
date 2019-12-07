# elpy doesn't want to load a def that's right at top of file

def plot (clf=True): 
  global da, tt
  if clf: plt.clf()
  da=sim.simData; tt=np.array(da['t'])
  [plt.plot(tt,v['cell_0']) for k,v in da.items() if 'V_axon' in k]

def plot1 (ke, clf=True, dat=None): 
  ''' plot from dat1 loaded up from loadall() '''
  global da, tt
  if not dat: dat=dat1
  if clf: plt.clf()
  da=dat[ke]; tt=np.array(da['t'])
  [plt.plot(tt,v['cell_0']) for k,v in da.items() if 'V_axon' in k]

def plotlast (dat=None): 
  ''' plot last spk from each'''
  if not dat: dat=dat1
  plt.clf()
  for k,v in dat.items():
    da=v['V_axon_1.00']['cell_0']
    if max(da) > -20: plt.plot(tt,v['V_axon_1.00']['cell_0'])

# Batch run using lp() routine in init.py
def loadall (files = 'data/19dec06_*.json'): 
  import glob
  global dat1, f1
  f1, dat1 = {x[-7:-5]:x for x in glob.glob(files)}, {}
  for k,v in f1.items(): 
    with open(v, 'r') as fo: dat1[k]=json.load(fo)['simData'] # also has 'netpyne_changeset', 'netpyne_version'
