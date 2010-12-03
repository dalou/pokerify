# -*- coding: utf8 -*-
from pokerify.rules.texasholdem import *

""" S'assoir a la table."""

name = 'raise'
title = """Surencherir"""
resume = ""

def apply( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.foldCards() and pl.setState( FOLD ):
			ro.refresh( )
			return pl.getEvents()
				
	return False
