# -*- coding: utf8 -*-

import sys, os, datetime, random, time, types, math
from pokerify.core import players, cards, money

class Room( ):
	
	def __init__(self, casino, rid, name='', seat_max=15, 
				stack_min = 10000, stack_max = 50000, 
				blinds=[ 100, 200 ], 
				tokens=[ 100, 200, 500, 1000, 5000 ],
				rotation = 20, #-60,
				angle = 360 #180
	):  
	
		self.casino =				casino
		self.rid = 					rid
		self.state =				1
		self.tokens =				tokens
		self.name =					name
		self.places =				seat_max 
		
		self.current =				0
		self.dealer = 				0
		
		self.deck =					[]
		self.cards = 				[]
		self.bets = 				[]
		self.betsamount =			0
		self.betsceil =				0
		self.betscount =			0
		
		self.players =				[]
				
		self.delay =                1
		
		self.created_at =			time.time()
		self.updated_at =			time.time()
		self.timeout =				False
		
		#GRAPHICS
		self.rotation =             rotation
		self.angle =                angle
		
		self.seat_positions = []
		for i in xrange( 1, self.places+1 ):
			angle = self.rotation + ( i-1 ) * ( self.angle / ( self.places ) ) 
			radian = angle * math.pi/180
			self.seat_positions.append( [i, int(math.cos( radian )*100), int(math.sin( radian )*100) ] )
		
	def addEvent( self, *args ):
		for player in self.players: player.addEvent( *args )
		return True
	
	# PERFECT SYSTEM	
	def event_setDeck( self, deck ): pass
	def setDeck( self, deck ): 
		self.deck = deck
		self.event_setDeck( self.deck )
		return True

	# PERFECT SYSTEM
	def isState(self, state): return self.state in state if type(state) == types.ListType else self.state is state
	
	# PERFECT SYSTEM
	def event_setState( self, state ): pass
	def setState(self, state): 
		self.state = state
		self.update()
		self.event_setState( self.state )	
		return True
	
	# PERFECT SYSTEM
	def getPlayers( self, state=None ): return filter( lambda player: player.isState( state ), self.players ) if state else self.players

	# PERFECT SYSTEM
	def event_addPlayer( self, player ): pass
	def addPlayer( self, player ): 
		self.players.append( player )
		self.event_addPlayer( player )
		return True
		
	# PERFECT SYSTEM
	def event_setDealer( self, player ): pass
	def setDealer( self, player ): 
		self.dealer = player
		self.event_setDealer( player )
		return True
		
	# PERFECT SYSTEM
	def event_setCurrent( self, player ): pass
	def setCurrent( self, player ): 
		self.current = player
		self.event_setCurrent( player )
		return True
		
	# PERFECT SYSTEM
	def event_addCard( self, card ): pass
	def addCard( self, card ): 
		self.cards.append( card )
		self.event_addCard( card )
		return True
	
	# PERFECT SYSTEM
	def getPlayer( self, pid=None, request=None, seat=None ): 
		if pid:
			for player in self.players:
				if player.pid == pid: return player
		elif seat:
			for player in self.players:
				if player.seat == seat: return player
		if request and pid:
			player = self.createPlayerFromRequest( pid, request )
			if player: 
				self.addPlayer( player )
				return player
		return 0
	
	def createPlayerFromRequest( self, pid, request ):
		return None

	# PERFECT SYSTEM				
	def update(self): 
		self.updated_at = time.time()
		self.timeout = False
		return True
	
	# PERFECT SYSTEM
	def setTimeOut( self, delay=None ): 
		self.delay = delay
		return True
	
	# PERFECT SYSTEM
	def forceTimeOut( self, boolean=False ): 
		self.timeout = boolean 
		return True
	
	# PERFECT SYSTEM
	def isTimeOut( self ): 
		if self.timeout or time.time() - self.updated_at > self.delay:
			self.update()
			return True
		return False
	
	

				
