# -*- coding: utf8 -*-
name = 'curieux'
title = 'Curieux'
""" Curieux:

Voir les cartes de ceux qui se sont couchés """

def apply( ru, ro, pl, re ):
	
	seat = re.getAttr('seat')
	ncard = re.getAttr('card')	
	
	player = ro.getPlayersBySeat( seat )
	cards = player.getCards()
	
	try: return cards[ cards ]
	except: return False



