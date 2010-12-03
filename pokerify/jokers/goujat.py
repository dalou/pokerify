# -*- coding: utf8 -*-
import random
"""
Goujat :

lvl1: voir un main au pif, on se sait pas a qui elle est
lvl2: voir un main au pif, on sait a qui elle est
??? : // un sort par options

Suivant les niveaux, savoir le nombre de coeur, trefle, pic couleur etc """

name = 'goujat'
title = 'Goujat!'

def apply( ru, ro, pl, re ):	

	if ro.isState( ru.INTURN ):
		players = ro.getPlayers( state=ru.CAN_BET )
		random.shuffle( players )
		try: players.remove( pl )
		except ValueError: pass
		try:
			cards = players[0].getCards()
			if cards:
				return pl.emit( 'lookup', players[0], cards )
		except ValueError: pass
	return False
