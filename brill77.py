# execfile('test.py')
import sys
sys.path.insert(1,'/usr/site/nrniv/local/python/netpyne')
import itertools as itr
import pandas as pd
import numpy as np
import pylab as plt
import json
fig, ax, params, data, pdi = None, None, None, None, None
from netpyne import specs, sim
from collections import OrderedDict

