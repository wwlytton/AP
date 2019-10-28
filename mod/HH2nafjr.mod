TITLE Hippocampal HH channels
: Fast Na+ modified from Traub, for Hippocampal Pyramidal cells, in: : Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991
: range variable vtraub adjust threshold
: Written by Alain Destexhe, Salk Institute, Aug 1992
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX hh2nafjr
	USEION na READ ena WRITE ina
	RANGE gnabar 
	RANGE m_inf, tau_m
        GLOBAL vtraub, emut, perc
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

PARAMETER {
	gnabar	= .003 	(mho/cm2)
	vtraub	= -63	(mV)
        emut = 40 (mV)
        perc = 0.0 : % current flowing thru mutated channel
	ena	(mV)
	celsius (degC)
	v       (mV)
}

STATE {	m h }

ASSIGNED {
	ina	(mA/cm2)
	m_inf
	tau_m
	tadj
}


BREAKPOINT {
	SOLVE states
	ina = gnabar * m*m*m*h * ((1-perc)*(v - ena) + perc*(v-emut))
}


PROCEDURE states() {	: exact when v held constant
	evaluate_fct(v)
        m' = (m_inf - m) / tau_m        
}

UNITSOFF
INITIAL {
	m = 0
	tadj = 3.0 ^ ((celsius-36)/ 10 )
}

PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2
	v2 = v - vtraub : convert to traub convention
	a = 0.32 * (13-v2) / ( exp((13-v2)/4) - 1)
	b = 0.28 * (v2-40) / ( exp((v2-40)/5) - 1)
	tau_m = 1 / (a + b) / tadj
	m_inf = a / (a + b)
}

UNITSON
