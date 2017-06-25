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
h.load_file('stdrun.hoc')
h.tstop = 6

h.load_file('brill77/cable.hoc')  # make(50, 1000) is called at bottom of file
h.geom(9500) # set long internode interval
stim=h.IClamp(0.5,sec=h.node[0])
stim.delay, stim.dur, stim.amp = 0, 0.1, 10
h.run()


