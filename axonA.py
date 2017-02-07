'''
import axonA
ax=axonA.AxonA()
reload(axonA) # can edit and reload
'''

from neuron import h

axonL = 1000
axonDiam =  10

# passive properties 
axonCap =  1.01280903702 
somaCap =  1.78829677463 
rall = 35.4 # default value

class AxonA ():
  "Simplest axon"
  def __init__(self,x=0,y=0,z=0,ID=0):
    self.x,self.y,self.z=x,y,z
    self.ID=ID
    self.all_sec = []
    self.add_comp('axon')
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
    # self.axon.connect(self.soma, 0.0, 0.0)

  def set_geom (self):
    self.axon.L = axonL; self.axon.diam = axonDiam;
    # self.soma.L = somaL; self.soma.diam = somaDiam

  def activeoff (self):
    for sec in self.all_sec: sec.gbar_naf=sec.gbar_kdr=sec.gbar_nafjr=0.0

  def set_axong (self):
    axon = self.axon
    axon.gbar_kdr  = gbar_kdr * kdr_gbar_axonm
    axon.gbar_naf = gbar_naf * naf_gbar_axonm
    axon.gbar_kdr = gbar_kdr * kdr_gbar_axonm
    axon.gbar_nafjr = gbar_nafjr * nafjr_gbar_axonm

  def set_calprops (self,sec):
    sec.gcalbar_cal = cal_gcalbar 
    sec.gcanbar_can = can_gcanbar 
    sec.gpeak_kBK = kBK_gpeak
    sec.caVhmin_kBK = -46.08 + kBK_caVhminShift
    sec.depth_cadad = cadad_depth
    sec.taur_cadad = cadad_taur   

  def set_somag (self):
    sec = self.soma
    sec.gbar_ih = gbar_h # Ih
    self.set_calprops(sec)
    sec.gbar_kdr  = gbar_kdr 
    sec.gbar_naf = gbar_naf * naf_gbar_somam

  def set_bdendg (self): 
    sec = self.Bdend
    sec.gbar_ih = gbar_h # Ih
    self.set_calprops(sec)
    sec.gbar_naf = gbar_naf * naf_gbar_dendm

  def set_apicg (self):
    h.distance(0,0.5,sec=self.soma) # middle of soma is origin for distance
    self.nexusdist = nexusdist = 300.0
    self.h_gbar_tuftm = h_gbar_tuftm = h_gbar_tuft / gbar_h
    self.h_lambda = h_lambda = nexusdist / log(h_gbar_tuftm)

  # set properties
  def set_props (self):
    self.set_geom()
    # cm - can differ across locations
    self.axon.cm = axonCap
    # self.soma.cm = somaCap
    # g_pas == 1.0/rm - can differ across locations
    # self.axon.g_pas = 1.0/axonRM
    # self.soma.g_pas = 1.0/somaRM
    for sec in []:
      sec.ek = p_ek # K+ current reversal potential (mV)
      sec.ena = p_ena # Na+ current reversal potential (mV)
      sec.Ra = rall; sec.e_pas = Vrest # passive      
      sec.gbar_naf    = gbar_naf # Na      
      sec.gbar_kdr    = gbar_kdr # KDR
      sec.vhalfn_kdr = kdr_vhalfn # KDR kinetics 
      sec.gbar_nafjr    = gbar_nafjr # K-A
      sec.vhalfn_nafjr = nafjr_vhalfn # K-A kinetics
      sec.vhalfl_nafjr = nafjr_vhalfl
      sec.tq_nafjr = nafjr_tq
    # self.set_somag()

  def insert_conductances (self):
    for sec in self.all_sec:
      sec.insert('k_ion')
      sec.insert('na_ion')
      sec.insert('pas') # passive
      sec.insert('hh') # 
      sec.insert('nafjr') # altered naf
    for sec in []:  # could add other sections here
      sec.insert('ih') # h-current      
      sec.insert('ca_ion') # calcium channels
      sec.insert('cal') # cal_mig.mod
      sec.insert('can') # can_mig.mod
      sec.insert('cadad') # cadad.mod - calcium decay 
      sec.insert('kBK') # kBK.mod - ca and v dependent k channel

#
def prmstr (p,s,fctr=2.0,shift=5.0):
  if p == 0.0:
    print s,'=',str(p-shift),str(p+shift),str(p),'True'
  elif p < 0.0:
    print s, '=',str(p*fctr),str(p/fctr),str(p),'True'
  else:
    print s, ' = ' , str(p/fctr), str(p*fctr), str(p), 'True'
