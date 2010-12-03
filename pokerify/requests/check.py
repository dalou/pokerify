from pokerify.rules.texasholdem import *
""" Le biceps : 

bruler sa propre carte, mais avoir un bonus

lvl1: 100% ;
lvl2: 100% + choisir sa carte;
lvl3: 120%..."""

def apply( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.betSum() == ro.betCeil() and pl.setState( CHECK ):
			ro.refresh( )
			return pl.getEvents()	
	return False
