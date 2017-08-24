import subprocess32 as subp
import re
chanlist,cdi,nadi,kdi = pkl.load(open(fi)) # read back in with load()
dr = '/u/billl/nrniv/AP/channelpediamod/'

for k,v in chanlist:
  for mf in v[1]: 
    fi = dr+'%s.mod'%mf
    gr = subp.check_output(['grep', 'SUFFIX', fi]).split()
    if (len(gr)!=3): raise(Exception('grep SUFFIX on %s returned %s'%(fi,gr)))
    lnum, suff = int(re.findall('\d+',gr[0])[0])-1, gr[2] # line# now 0 offset statt 1
    fpi, fpo = map(open, [fi, dr+'%s%s.mod'%(suff,mf)], ['r','w'])
    li=fpi.readlines()
    lin=re.sub('SUFFIX (.+_.+)','SUFFIX \\1_%s'%mf,li[lnum])
    print lin
    map(close, [fpi, fpo])
    
