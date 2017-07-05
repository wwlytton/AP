'''
USAGE:
'''
from neuron import h
import os, sys, json
import numpy as np
import pylab as plt
import pickle as pkl

tvec=[]
colors = ['k','b','r','g','c','m','y']

def mkfig (rows=1, cols=1):
  global fig, axi, axit
  fig, axi = plt.subplots(rows, cols, squeeze=False) # squeeze to always get an array of axes even for 1x1
  axit = zip(*axi) # transpose
  return (fig, axi, axit)

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
    if column==0: ax.text(0, 0, '%d%%'%d1[0],fontsize=14, ha='right', va='top')
  plt.vlines(600, 0, 50)
  plt.hlines(0, 550, 600)

def TCraster (di, **kwargs):
  ax=axi[0][0]
  ax.clear()
  keys = ['RE', 'TC', 'PY', 'IN']
  for i,c,k in zip(range(4), colors, keys):
    v=di[k]
    ax.scatter(v['spkt'],v['spkid'].c().add(i*110), linewidth=0, s=4, color=c) # spkt, spkid belongs to the cell types
    ax.text(1e3, i*120+50, k , color=c, fontsize=14, ha='left', va='top')
  ax.set_axis_off()    
  ax.set_xlim(175,1000)
  plt.hlines(-20, 950, 1000, linewidth=4)
