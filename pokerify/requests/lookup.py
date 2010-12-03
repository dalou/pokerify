"""
Lookup:

Voir ses cartes
"""

def apply( ca, ro, pl ):
	cards = pl.getCards()
	if cards:
		pl.emit( 'lookup', pl, cards )
		return pl.getEvents()
	return False
