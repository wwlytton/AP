: Equations modified by Traub, for Hippocampal Pyramidal cells, in: : Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991
: range variable vtraub adjust threshold
: Written by Alain Destexhe, Salk Institute, Aug 1992
: Modified Oct 96 for compatibility with Windows: trap low values of arguments

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX hh2k
	USEION k READ ek WRITE ik
	RANGE gkbar, vtraub
	RANGE n_inf, tau_n
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

PARAMETER {
	gnabar  = 0.0  (mho/cm2)
	gkbar   = .005  (mho/cm2)
	ek      (mV)
	celsius (degC)
	dt      (ms)
	v       (mV)
	vtraub = -63   (mV)
}

STATE {
	h n
}

ASSIGNED {
	ik      (mA/cm2)
	il      (mA/cm2)
	n_inf
	tau_n
	tadj
}


BREAKPOINT {
	SOLVE states
	ik  = gkbar * n*n*n*n * (v - ek)
}


DERIVATIVE states {   : exact Hodgkin-Huxley equations
       evaluate_fct(v)
       n' = (n_inf - n) / tau_n
}

UNITSOFF
INITIAL {
	tadj = 3.0 ^ ((celsius-36)/ 10 )
	h = 0
	n = 0
}

PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2
	v2 = v - vtraub : convert to traub convention
	a = 0.032 * vtrap(15-v2, 5)
	b = 0.5 * Exp((10-v2)/40)
	tau_n = 1 / (a + b) / tadj
	n_inf = a / (a + b)
}

FUNCTION vtrap(x,y) {
	if (fabs(x/y) < 1e-6) {
		vtrap = y*(1 - x/y/2)
	}else{
		vtrap = x/(Exp(x/y)-1)
	}
}

FUNCTION Exp(x) {
	if (x < -100) {
		Exp = 0
	}else{
		Exp = exp(x)
	}
} 
