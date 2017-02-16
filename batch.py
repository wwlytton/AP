""" 
mpiexec -np 4 nrniv -python -mpi batch.py 
"""
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
	b = createBatch({'percnajr'        : np.linspace(0.0,1.0,9), 
                         'rall'            : [34.5, 100, 200],
                         ('hParams', 'celsius') : [6.3, 23, 37]})
	runBatch(b, 'baxA')

# Main code
if __name__ == '__main__':
	batchaxA() 
