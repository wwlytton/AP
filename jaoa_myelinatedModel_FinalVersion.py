import os
from neuron import h, gui
from matplotlib import pyplot
import numpy as np
import scipy.signal as sig

aL = 30e3
gL = 1e-4

displens = list() # internodal distances
vels = list() # velocity

#for disp_len in np.arange(99.0, 2000.0, 50.0):	#	Loop for Myelin study
for chan_scale in np.arange(1., 50.0, 5.0):		#	Loop for Channels study
    # demy_len = disp_len + 7.0
    disp_len = 1999.0 #	Constant for the Myelin length in the study of channels increase after demyelination
    #savename = 'figs'+os.sep+'axonLen%d_interNodal%05d.png' % (int(aL),int(disp_len),)		#	Filename for Myelin study
    savename = 'figs'+os.sep+'axonLen%d_chan_Scale%05d.png' % (int(aL),int(chan_scale),)	#	Filename for Channels study
    print "Now calculating %s" % (savename,)

    '''
    Here is created a Neuron with   a soma and an axon component
    somaMotor is a sphere
    axonMotor is a cylinder with    length of 1 meter (10^6 microns)
                                    segments of 2 microns each
                                    each myelin sheet has a length of 48 microns
                                    each ranvier node has a length of 02 microns
    
                                CMT             Control
    propagation velocity: 20.4 +/- 4.7 m/s    48 m/s
    internodal length:    73.9 +/- 27 micron  94.5 +/- 28.6 micron
    nr nodes:             ~ 117               ~ 176
    '''
    # Creating the Soma structure
    somaMotor = h.Section(name='somaMotor')
    somaMotor.L = somaMotor.diam = 34.0 # microns (34 microns), arbitrary value

    # Creating the Axon structure
    axonMotor = h.Section(name='axonMotor')
    axonMotor.L = aL # microns
    axonMotor.diam = 10. #microns # Tackmann 1976
    segmentSize = 1 # microns

    # print "Axon length / segment size: %f" % (axonMotor.L/segmentSize,)

    axonMotor.nseg = int(int(axonMotor.L) / int(segmentSize))

    # Connecting the Soma and Axon
    axonMotor.connect(somaMotor(1))

    # Inserting active Hodgkin-Huxley current in the soma
    somaMotor.insert('hh')
    somaMotor.gnabar_hh = 0.12  # Sodium conductance in S/cm2
    somaMotor.gkbar_hh = 0.036  # Potassium conductance in S/cm2
    somaMotor.gl_hh = 0.0003    # Leak conductance in S/cm2
    somaMotor.el_hh = -65 # -54.3    # Reversal potential in mV
    somaMotor.Ra = 10 # Axial resistance in Ohms
    somaMotor.cm = 10

    # Adding active HH channels in the Axon of the passive Neuron
    axonMotor.insert('hh')
    axonMotor.gnabar_hh     = 1e-5   # Sodium conductance in S/cm2
    axonMotor.gkbar_hh  	= 1e-5   # Potassium conductance in S/cm2
    axonMotor.gl_hh         = 1e-7   # Leak conductance in S/cm2
    axonMotor.cm = 1e-5
    axonMotor.Ra = 10 # Axial resistance

    const_gbar = 1e3

    for segIndex in range(1, axonMotor.nseg):
        segIndexNorm = float(segIndex)/float(axonMotor.nseg)
        
        if segIndex % disp_len == 0:                     # Ranvier Node membrane properties
            # print "segIndex: %f" % (segIndex,)
            axonMotor(segIndexNorm).hh.gnabar = 0.12*const_gbar/10
            axonMotor(segIndexNorm).hh.gkbar = 0.036*const_gbar/10
            axonMotor(segIndexNorm).hh.gl = gL
            axonMotor(segIndexNorm).cm = 10.

        else:                                           # Myelin Sheath membrane properties

            axonMotor(segIndexNorm).hh.gnabar   = 1e-5   # Sodium conductance in S/cm2
            axonMotor(segIndexNorm).hh.gkbar    = 1e-5 # Potassium conductance in S/cm2
            axonMotor(segIndexNorm).hh.gl       = 1e-7   # Leak conductance in S/cm2
            axonMotor(segIndexNorm).cm = 1e-5           # capacitance in microfarads

#	First Stage Degradation
# 	Damage on the middle of the myelin
    for segIndex in range(1, axonMotor.nseg):
        segIndexNorm_ = float(segIndex+(disp_len/2))/float(axonMotor.nseg)
        print segIndexNorm_
        if segIndex % disp_len == 0:                     # Demyelinated axon properties
            maxRange = 100
            for x in xrange(1,maxRange):
                xIndexNorm_ = float(segIndex+(disp_len/2)-int(maxRange/2)+x)/float(axonMotor.nseg)
                if segIndexNorm_+xIndexNorm_<1:
                    print x
                    # print "segIndex: %f" % (segIndex,)
                    axonMotor(segIndexNorm_+xIndexNorm_).hh.gnabar = 0.012*chan_scale#	1e-9 	(constant for Myelin study // 0.012*chan_scale for channels study)
                    axonMotor(segIndexNorm_+xIndexNorm_).hh.gkbar = 0.0036*chan_scale#	1e-9 	(constant for Myelin study // 0.0036*chan_scale for channels study)
                    axonMotor(segIndexNorm_+xIndexNorm_).hh.gl = gL#*1e-9 						(constant for Myelin study // gL for channels study)
                    axonMotor(segIndexNorm_+xIndexNorm_).cm = 1.
# #	Second Stage Degradation
# # Damage on the first quarter
#     for segIndex in range(1, axonMotor.nseg):
#         segIndexNorm_ = float(segIndex+(disp_len/4))/float(axonMotor.nseg)
#         print segIndexNorm_
#         if segIndex % disp_len == 0:                     # Demyelinated axon properties
#             maxRange = 100
#             for x in xrange(1,maxRange):
#                 xIndexNorm_ = float(segIndex+(disp_len/4)-int(maxRange/2)+x)/float(axonMotor.nseg)
#                 if segIndexNorm_+xIndexNorm_<1:
#                     print x
#                     # print "segIndex: %f" % (segIndex,)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gnabar = 0.012*chan_scale#1e-9 	(constant for Myelin study // 0.012*chan_scale for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gkbar = 0.0036*chan_scale#1e-9 	(constant for Myelin study // 0.0036*chan_scale for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gl = gL#*1e-9 					(constant for Myelin study // gL for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).cm = 1.
# # Damage on the second quarter
#     for segIndex in range(1, axonMotor.nseg):
#         segIndexNorm_ = float(segIndex+(disp_len*3/4))/float(axonMotor.nseg)
#         print segIndexNorm_
#         if segIndex % disp_len == 0:                     # Demyelinated axon properties
#             maxRange = 100
#             for x in xrange(1,maxRange):
#                 xIndexNorm_ = float(segIndex+(disp_len*3/4)-int(maxRange/2)+x)/float(axonMotor.nseg)
#                 if segIndexNorm_+xIndexNorm_<1:
#                     print x
#                     # print "segIndex: %f" % (segIndex,)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gnabar = 0.012*chan_scale#1e-9 	(constant for Myelin study // 0.012*chan_scale for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gkbar = 0.0036*chan_scale#1e-9 	(constant for Myelin study // 0.0036*chan_scale for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).hh.gl = gL#*1e-9 					(constant for Myelin study // gL for channels study)
#                     axonMotor(segIndexNorm_+xIndexNorm_).cm = 1.

    ''' 
        We tried current clamp, but it worked as same as the Alpha Synapse
    '''
    # Insert Alpha Synapse
    syn = h.AlphaSynapse(somaMotor(1.0))
    syn.e = 0  # equilibrium potential in mV
    # syn.onset = 20  # turn on after this time in ms
    syn.gmax = 1e6  # set conductance in uS
    syn.tau = 1e-2 # set time constant 

    # Set up plot
    t_vec = h.Vector()  # record time
    t_vec.record(h._ref_t)

    v_vec_soma = h.Vector() # record soma
    v_vec_soma.record(somaMotor(0.5)._ref_v)

    # Setting up the recordings
    probe_rate = 0.01
    axon_locs = np.arange(probe_rate,1,probe_rate)  # set axon recording times
    v_vec_axon=[]
    for loc in axon_locs:
        v_vec_axon.append(h.Vector())
        v_vec_axon[-1].record(axonMotor(loc)._ref_v)
        
    ## run simulation (passive propagation in axon)
    # h.topology()
    h.tstop = 4
    h.run()

    #pyplot format
    pyplot.figure(figsize = (8,4))
    pyplot.plot(t_vec, v_vec_soma, label = 'sM')  # plot soma
    for i,v_vec in enumerate(v_vec_axon):  # plot axon
        pyplot.plot(t_vec, v_vec, label = 'aM '+str(axon_locs[i]))
        vpksix = sig.argrelmax(np.array([vi for vi in v_vec]), order=int(300*aL*probe_rate))[0].astype(int) # get pks
        tvp = [t_vec[tk] for tk in vpksix]
        vvp = [v_vec[vk] for vk in vpksix]
        Vvel = (float(axon_locs[-1]/tvp[-1])) # we don't consider the situation where the spike doesn't make it
        # print "axon_locs[-1]: %f , tvp[-1]: %f" % (axon_locs[-1],tvp[-1])
    pyplot.plot(tvp, vvp, 'rx')
    # pyplot.legend()
    VvelF = (Vvel*aL)*1e-3 # meters/sec
    displens.append(disp_len)
    vels.append(VvelF)
    print "Velocity: %.5e m/sec" % (VvelF,)
    title_text = 'Myelinated Axon: Axon Length: %d microns\nVelocity: %.5e m/sec\ninterNode: %.3e' % (aL,VvelF,disp_len)
    pyplot.title(title_text, size=8)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')
    pyplot.savefig(savename)
    pyplot.close('all')

pyplot.figure(figsize=(8,4))
pyplot.plot(displens, vels)
pyplot.title("Velocity vs Internodal spacing")
pyplot.xlabel('Internodal spacing')
pyplot.ylabel('Velocity (m/sec)')
#pyplot.savefig('figs'+os.sep+'vel_internode.png')
pyplot.show()