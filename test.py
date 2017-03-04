import sys
params, data = None, None
def read ():
    global params, data
    sys.path.append('/usr/site/nrniv/local/python/netpyne/examples/batchCell')
    from utils import readBatchData
    params, data = readBatchData('data/', 'baxA', loadAll=0, saveAll=0, vars=None, maxCombs=None) 

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
