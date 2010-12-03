# -*- coding: utf8 -*-

#PING
from pokerify.rules.texasholdem import *
from pokerify.core import pong

def getrooms( ca, ro, pl ):
	results = []
	for room in ca.rooms.values():
		results.append({
			'nb_players' : len(room.getPlayers( )),
			'id' : room.rid,
			'state' : room.state
		})
	return results

def addroom( ca, ro, pl  ):
	ca.addRoom()
	return False

def enter( ca, ro, pl ):
	pl.resume()
	return pl.pong()
	
def addfake( ca, ro, pl  ):	
	
	ro.getPlayer( 2, { 'name':"Kane", 'stack': 20000, 'fake':True } )
	ro.getPlayer( 3, { 'name':"Undertaker", 'stack': 5000, 'fake':True } )
	ro.getPlayer( 4, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
	ro.getPlayer( 5, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
	ro.getPlayer( 6, { 'name':"The miz", 'stack': 120000, 'fake':True } )
	ro.getPlayer( 7, { 'name':"Cena", 'stack': 10000, 'fake':True } )
	ro.refresh( )
	
	for p in ro.players.values(): sitdown( ca, ro, p )
	
def sitdown( ca, ro, pl ):
	if pl.setSeat( ) and pl.setState( WAITING ) and ro.refresh( ): return pl.pong()
	return False

def resume( ca, ro, pl ):
	if ro and pl and ro.refresh( ): return pl.pong()
	return False
	
def call( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.betSum() < ro.betCeil() and pl.bet( ro.betCeil() ) and pl.setState( CALL ):
			ro.refresh( )
			return pl.pong()
	return False
	
def check( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.betSum() == ro.betCeil() and pl.setState( CHECK ):
			ro.refresh( )
			return pl.pong()	
	return False
	
def fold( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.foldCards() and pl.setState( FOLD ):
			ro.refresh( )
			return pl.pong()
				
	return False
	
def raiseby( ca, ro, pl ):
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.bet( ro.betCeil()*2 ) and pl.setState( RAISE ):
			ro.refresh( )
			return pl.pong()
	return False
	
def allin( ca, ro, pl ):	
	if pl.isState( READY ) and ro.isState( INTURN ):
		if pl.bet( pl.stack ) and pl.setState( ALLIN ):
			ro.refresh( )
			return pl.pong()
			
			
		
	return False
