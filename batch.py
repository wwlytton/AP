"""  """
from netpyne.batch import Batch
import numpy as np

def createBatch(params):
	b = Batch()
	for k,v in params.iteritems():
		b.params.append({'label': k, 'values': v})
	return b

def runBatch(b, label):
	b.batchLabel = label
	b.saveFolder = 'data/'+b.batchLabel
	b.method = 'grid'
	b.runCfg = {'type': 'mpi', 'script': 'init.py', 'skip': True}
	b.run() # run batch

def batchNa():
	b = createBatch({'dendNa': [0.025, 0.03],
                         ('IClamp1', 'amp'): [0.1, 0.5]})
	runBatch(b, 'batchNa')

# Main code
if __name__ == '__main__':
	batchNa() 
