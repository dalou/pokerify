""" Le biceps : 

bruler sa propre carte, mais avoir un bonus

lvl1: 100% ;
lvl2: 100% + choisir sa carte;
lvl3: 120%..."""

def apply( ca, ro, pl ):	

	if ro: ro.refresh( )
	if pl: return pl.getEvents()
	return False
