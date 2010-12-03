# -*- coding: utf8 -*-
""" S'assoir a la table."""

from pokerify.rules import texasholdem

name = 'situp'
title = """S'assoir à la room"""
resume = ""

def apply( ca, ro, pl ):
	
	if pl.setState( texasholdem.UP ) and ro.refresh( ) :
		return pl.getEvents()
	return False

