import sys
import itertools as itr
import pandas as pd
params, data = None, None

# reading data section
def read ():
    global params, data
    sys.path.append('/usr/site/nrniv/local/python/netpyne/examples/batchCell')
    from utils import readBatchData
    params, data = readBatchData('data/', 'baxA', loadAll=1, saveAll=0, vars=None, maxCombs=None) 

def loadall (filename = 'data/baxA/baxA_allData.json'): 
  global params, data
  with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
  params, data = dataLoad['params'], dataLoad['data']

def loadpd (filename = 'data/baxA/df4.pd'):
  "need precise_float=True to get the correct numbers"
  return pd.read_json('data/baxA/df4.pd',precise_float=True)

# fig, ax = plt.subplots(1, 1)
# df4.query('gnabar==0.12 & temp==6.3 & rall==200').plot('percnajr','V0max',label="abc",ax=ax)
# df4[(df4.gnabar==0.12) & (df4.temp==6.3) & (df4.rall==200)].plot('percnajr','V0max',label="abc",ax=ax)

def mkqstr (l):
  'Create a query string from a list of tuples with (name, value)'
  st=''
  for x in l: st+="%s==%g&"%(x[0],x[1])
  return st.strip('[ &]')

def supfigs ():
  global res
  ax.clear()
  for tup in [zip(labs,x) for x in itr.product(*[v for x,v in vals.iteritems()])]:
    st=mkqstr(tup)
    res=df4.query(st)
    if len(res)>2: res.plot('percnajr','V0max',label=st,ax=ax,linewidth=6)

def plotf (dataDir='data/', batchLabel='baxA', params=params, data=data): # from plotfINa
    import utils
    utils.setPlotFormat(numColors = 8)
    Pvals = params[0]['values']
    Ivals = params[1]['values']
    Pvalsdic = {val: i for i,val in enumerate(Pvals)}
    Ivalsdic = {val: i for i,val in enumerate(Ivals)}
    rates = [[0 for x in range(len(Pvals))] for y in range(len(Ivals))] 
    for key, d in data.iteritems():
        rate = len(d['simData']['spkt'])
        Pindex = Pvalsdic[d['paramValues'][0]]
        Iindex = Ivalsdic[d['paramValues'][1]]
        rates[Iindex][Pindex] = rate
        print d['paramValues']
        print rate

    filename = '%s/%s/%s_fIcurve.json' % (dataFolder, batchLabel, batchLabel)
    with open(filename, 'w') as fileObj:
        json.dump(rates, fileObj)

    plt.figure()

    handles = plt.plot(rates, marker='o', markersize=10)
    plt.xlabel('Somatic current injection (nA)')
    plt.xticks(range(len(Ivals))[::2], Ivals[::2])
    plt.ylabel('Frequency (Hz)')
    plt.legend(handles, params[0]['values'], title = 'dend Na', loc=2)
    plt.savefig('%s/%s/%s_fIcurve.png' % (dataFolder, batchLabel, batchLabel))
    plt.show()
