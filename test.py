import sys
import itertools as itr
params, data = None, None

fig, ax = plt.subplots(1, 1)  17mar08a\gref
# df4.query('gnabar==0.12 & temp==6.3 & rall==200').plot('percnajr','V0max',label="abc",ax=ax)

def eq (a,b): return np.isclose(a,b)

def mkqstr (l):
  'Create a query string from a list of tuples with (name, value)'
  st=''
  for x in l: st+="%s==%g&"%(x[0],x[1])
  return st.strip('[ &]')

def ae ():
 ax.clear()
 for tup in [zip(labs,x) for x in itr.product(*[v for x,v in vals.iteritems()])]:
   st=mkqstr(tup)
   res=df4.query(st)
   print st,len(res),'; ',
   if len(res)>2: res.plot('percnajr','V0max',label=st,ax=ax)

def read ():
    global params, data
    sys.path.append('/usr/site/nrniv/local/python/netpyne/examples/batchCell')
    from utils import readBatchData
    params, data = readBatchData('data/', 'baxA', loadAll=1, saveAll=0, vars=None, maxCombs=None) 

def loadall (): 
  global params, data
  filename = 'data/baxA/baxA_allData.json'
  with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
  params, data = dataLoad['params'], dataLoad['data']

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
