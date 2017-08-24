chanlist,cdi,nadi,kdi = pkl.load(open(fi)) # read back in with load()

for k,v in chanlist:
  for mf in v[1]: 
    fi = '/u/billl/nrniv/AP/channelpediamod/' + '%s.mod'%mf
    try: open
