'''
import axonA
ax=axonA.AxonA()
reload(axonA) # can edit and reload
'''
from neuron import h
axonL = 1000
axonDiam =  10

class AxonA ():
  "Simplest axon"
  def __init__(self,x=0,y=0,z=0,ID=0,percnajr=0,rall=35.4): # proportion j.r. na channel
    self.x,self.y,self.z,self.ID=x,y,z,ID
    self.percnajr,self.rall=percnajr,rall
    self.all_sec = []
    self.set_morphology()
    self.insert_conductances()
    self.set_props()
    self.calc_area()

  def add_comp(self, name):
    self.__dict__[name] = h.Section(name=name)#,cell=self)
    self.all_sec.append(self.__dict__[name])

  def calc_area(self):
    self.total_area = 0
    self.n = 0
    for sect in self.all_sec:
      self.total_area += h.area(0.5,sec=sect)
      self.n+=1

  def set_morphology(self):
    self.add_comp('axon')
    self.set_geom()

  def set_geom (self):
    self.axon.L = axonL
    self.axon.diam = axonDiam;

  def activeoff (self):
    for sec in self.all_sec: sec.gbar_naf=sec.gbar_kdr=sec.gbar_nafjr=0.0

  # set properties
  def set_props (self):
    self.set_geom()
    for sec in self.all_sec:
      print "AAAA",self.x,self.rall
      # sec.Ra = rall;
      # leave other hh stuff at default values

  def insert_conductances (self):
    for sec in self.all_sec:
      sec.insert('k_ion')
      sec.insert('na_ion')
      sec.insert('hh') # 
      sec.insert('nafjr') # altered naf
