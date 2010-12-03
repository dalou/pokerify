# -*- coding: utf8 -*-
""" S'assoir a la table."""

from pokerify.rules import texasholdem

name = 'sitdown'
title = """S'assoir à la room"""
resume = ""

def apply( ca, ro, pl ):
	
	if pl.setSeat( ) and pl.setState( texasholdem.WAITING ) and ro.refresh( ) :
		pl.emit('setme', pl.pid )
		return pl.getEvents()
	return False

