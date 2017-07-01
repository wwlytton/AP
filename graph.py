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
  global fig, axi, axit
  fig, axi = plt.subplots(6, 3)
  axit = zip(*axi) # transpose

def replot (d, w=2, column=0, color='b'):
  global tvec
  axi=axit[column]
  if len(tvec)!=len(d[0][1]): tvec=h.Vector(len(d[0][1])).indgen(h.dt)
  for ax in axi: ax.clear()
  for ax in axi: ax.set_ylim(-120,50) 
  for ax, d1 in zip(axi, d): 
    ax.plot(tvec, d1[1], linewidth=w, color=color)
    ax.set_axis_off()
    # https://matplotlib.org/users/text_props.html
    if column==0: ax.text(0, 0, '%d%%'%d1[0],fontsize=14, ha='center', va='top')
  plt.vlines(600, 0, 50)
  plt.hlines(0, 550, 600)

