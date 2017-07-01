'''
USAGE:
'''
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl

tvec=[]

def mkfig ():
  global fig,axi
  fig, axi = plt.subplots(6, 1)

def replot (d, w=2, col='b'):
  global tvec
  if len(tvec)!=len(d[0][1]): tvec=h.Vector(len(d[0][1])).indgen(h.dt)
  for ax in axi: ax.clear()
  for ax in axi: ax.set_ylim(-120,50) 
  for ax, d1 in zip(axi, d): 
    ax.plot(tvec, d1[1], linewidth=w, color=col)
    ax.set_axis_off()
  plt.vlines(600, 0, 50)
  plt.hlines(0, 550, 600)

