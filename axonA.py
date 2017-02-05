class SPI6 ():
  "Simplified Corticospinal Cell Model"
  def __init__(self,x=0,y=0,z=0,ID=0):
    self.x,self.y,self.z=x,y,z
    self.ID=ID
    self.all_sec = []
    self.add_comp('soma')
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
    self.add_comp('Bdend')
    self.add_comp('Adend1')
    self.add_comp('Adend2')
    self.add_comp('Adend3')
    self.apic = [self.Adend1, self.Adend2, self.Adend3]
    self.basal = [self.Bdend]
    self.alldend = [self.Adend1, self.Adend2, self.Adend3, self.Bdend]
    self.set_geom()
    self.axon.connect(self.soma, 0.0, 0.0)
    self.Bdend.connect(self.soma,      0.5, 0.0) # soma 0.5 to Bdend 0
    self.Adend1.connect(self.soma,   1.0, 0.0)
    self.Adend2.connect(self.Adend1,   1.0, 0.0)
    self.Adend3.connect(self.Adend2,   1.0, 0.0)

  def set_geom (self):
    self.axon.L = axonL; self.axon.diam = axonDiam;
    self.soma.L = somaL; self.soma.diam = somaDiam
    for sec in self.apic: sec.L,sec.diam = apicL,apicDiam
    self.Bdend.L = bdendL; self.Bdend.diam = bdendDiam

  def activeoff (self):
    for sec in self.all_sec: sec.gbar_nax=sec.gbar_kdr=sec.gbar_kap=0.0

  def set_axong (self):
    axon = self.axon
    axon.gbar_kdmc  = gbar_kdmc * kdmc_gbar_axonm
    axon.gbar_nax = gbar_nax * nax_gbar_axonm
    axon.gbar_kdr = gbar_kdr * kdr_gbar_axonm
    axon.gbar_kap = gbar_kap * kap_gbar_axonm

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
    sec.gbar_kdmc  = gbar_kdmc 
    sec.gbar_nax = gbar_nax * nax_gbar_somam

  def set_bdendg (self): 
    sec = self.Bdend
    sec.gbar_ih = gbar_h # Ih
    self.set_calprops(sec)
    sec.gbar_nax = gbar_nax * nax_gbar_dendm

  def set_apicg (self):
    h.distance(0,0.5,sec=self.soma) # middle of soma is origin for distance
    self.nexusdist = nexusdist = 300.0
    self.h_gbar_tuftm = h_gbar_tuftm = h_gbar_tuft / gbar_h
    self.h_lambda = h_lambda = nexusdist / log(h_gbar_tuftm)
    for sec in self.apic:
      self.set_calprops(sec)
      for seg in sec:
        d = h.distance(seg.x,sec=sec)
        if d <= nexusdist: seg.gbar_ih = gbar_h * exp(d/h_lambda)
        else: seg.gbar_ih = h_gbar_tuft
      sec.gbar_nax = gbar_nax * nax_gbar_dendm
    self.apic[1].gcalbar_cal = cal_gcalbar * calginc # middle apical dend gets more iL

  # set properties
  def set_props (self):
    self.set_geom()
    # cm - can differ across locations
    self.axon.cm = axonCap
    self.soma.cm = somaCap
    self.Bdend.cm = bdendCap
    for sec in self.apic: sec.cm = apicCap
    # g_pas == 1.0/rm - can differ across locations
    self.axon.g_pas = 1.0/axonRM
    self.soma.g_pas = 1.0/somaRM
    self.Bdend.g_pas = 1.0/bdendRM
    for sec in self.apic: sec.g_pas = 1.0/apicRM
    for sec in self.all_sec:
      sec.ek = p_ek # K+ current reversal potential (mV)
      sec.ena = p_ena # Na+ current reversal potential (mV)
      sec.Ra = rall; sec.e_pas = Vrest # passive      
      sec.gbar_nax    = gbar_nax # Na      
      sec.gbar_kdr    = gbar_kdr # KDR
      sec.vhalfn_kdr = kdr_vhalfn # KDR kinetics 
      sec.gbar_kap    = gbar_kap # K-A
      sec.vhalfn_kap = kap_vhalfn # K-A kinetics
      sec.vhalfl_kap = kap_vhalfl
      sec.tq_kap = kap_tq
    self.set_somag()
    self.set_bdendg()
    self.set_apicg()
    self.set_axong()

  def insert_conductances (self):
    for sec in self.all_sec:
      sec.insert('k_ion')
      sec.insert('na_ion')
      sec.insert('pas') # passive
      sec.insert('nax') # Na current
      sec.insert('kdr') # K delayed rectifier current
      sec.insert('kap') # K-A current
    for sec in [self.Adend3, self.Adend2, self.Adend1, self.Bdend, self.soma]:
      sec.insert('ih') # h-current      
      sec.insert('ca_ion') # calcium channels
      sec.insert('cal') # cal_mig.mod
      sec.insert('can') # can_mig.mod
      sec.insert('cadad') # cadad.mod - calcium decay 
      sec.insert('kBK') # kBK.mod - ca and v dependent k channel
    for sec in [self.soma, self.axon]: sec.insert('kdmc')  # K-D current in soma & axon only

#
def prmstr (p,s,fctr=2.0,shift=5.0):
  if p == 0.0:
    print s,'=',str(p-shift),str(p+shift),str(p),'True'
  elif p < 0.0:
    print s, '=',str(p*fctr),str(p/fctr),str(p),'True'
  else:
    print s, ' = ' , str(p/fctr), str(p*fctr), str(p), 'True'
