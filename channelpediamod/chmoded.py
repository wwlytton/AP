#!/usr/bin/python
import subprocess32 as subp
import pickle as pkl
import re
chanlist,cdi,nadi,kdi = pkl.load(open('channels.pkl')) # read back in with load()

for k,v in cdi.iteritems():
  for mf in v[1]: 
    fi = '%s.mod'%mf
    gr = subp.check_output(['grep', '-n', 'SUFFIX', fi]).split()
    if (len(gr)!=3): raise(Exception('grep SUFFIX on %s returned %s'%(fi,gr)))
    lnum, suff = int(re.findall('\d+',gr[0])[0])-1, gr[2] # line# now 0 offset statt 1
    fpi, fpo = map(open, [fi, '%s%s.mod'%(suff,mf)], ['r','w'])
    li=fpi.readlines()
    li[lnum] = re.sub('SUFFIX (.+_.+)','SUFFIX \\1_%s'%mf,li[lnum])
    fpo.writelines(li)
    fpi.close(); fpo.close()
