from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl
h.load_file('stdrun.hoc')
fig, axi = None, None
datestr = os.popen('datestring').read()

# just work with 3 compartment cell for now re3_cc, also re1 and re80, and reD (dissociated cell)
# have different demos in Cav32_WT (wild type); Cav32_R788C; Cav32_C456S
h.xopen('Cav32RE3cc.hoc')

