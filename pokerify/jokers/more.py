# -*- coding: utf8 -*-
import random, jokers
"""More (pic|trefle|noir|rouge):

x% de chance de plus qu'une carte noir/rouge sorte, ou pic trefle carreau """

name = 'more'
title = 'More'

class More( jokers.Joker ):
	

	def apply( ru, ro, pl, re ):	

		if ro.isState( ru.SERVING ):
			pl.activeCard( 'more' )
		return False

	def onGiveCard( ru, ro, pl ):
		pass
	
