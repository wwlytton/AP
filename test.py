# elpy doesn't want to load a def that's right at top of file

def plot1 (ke): 
  ''' plot from dat1 loaded up from loadall() '''
  global da, tt
  plt.clf()
  da=dat1[ke]; tt=np.array(da['t'])
  [plt.plot(tt,v['cell_0']) for k,v in da.items() if 'V_axon' in k]

# Batch run using lp() routine in init.py
def loadall (files = 'data/19dec06_*.json'): 
  import glob
  global dat1, f1
  f1, dat1 = {x[-7:-5]:x for x in glob.glob(files)}, {}
  for k,v in f1.items(): 
    with open(v, 'r') as fo: dat1[k]=json.load(fo)['simData'] # also has 'netpyne_changeset', 'netpyne_version'
