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

def batchaxA():
	b = createBatch({'ena': [50, 5], ('stim', 'amp'): [2, 4]})
	runBatch(b, 'baxA')

# Main code
if __name__ == '__main__':
	batchaxA() 
