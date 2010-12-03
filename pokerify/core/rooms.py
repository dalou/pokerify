# -*- coding: utf8 -*-

import sys, os, datetime, random, time, types
from pokerify.core import players, cards

class Room( ):
	
	def __init__(self, casino, rid, name='', seat_max=7, 
				stack_min = 10000, stack_max = 50000, 
				blinds=[ 100, 200 ], 
				tokens=[ 100, 200, 500, 1000, 5000 ] ):
	
		self.casino =				casino
		self.rid = 					rid
		self.state =				1
		self.tokens =				tokens
		self.name =					name
		self.deck =					[]
		self.seats = 				{}
		self.cards = 				{}
		self.bets = 				{}
		self.dealer =				0
		self.current =				0
		self.players =				{}
		self.blinds =				blinds
		self.delay =                20
		self.created_at =			time.time()
		self.updated_at =			time.time()
		self.timeout =				False
		for i in range(1, seat_max): self.seats[ i ] = None
		for i in range(1, seat_max): self.cards[ i ] = []
		self.cards[ -1 ] = []
		self.cards[ -2 ] = []
		for i in self.seats: self.bets[ i ] = []
		
	def ping( self, command, args={} ):
		args['rid'] = self.rid
		self.casino.ping( command, args )
		
	def setDeck( self, deck ): 
		self.deck = deck
		return True
		
	def public( self, *args ): 
		for p in self.getPlayers(): p.events.append( list(args) )
		return True

	def isState(self, state): return self.state in state if type(state) == types.ListType else self.state is state
	def setState(self, state): 
		self.state = state
		self.update() and self.public( 'turn', self.state )
		return True	

	def setBlinds(self, blinds): 
		self.blinds = blinds
		return True
			
	def getEmptySeat( self ):
		for i, seat in self.seats.items():
			if not seat: return i
		return None

	# Players get and set
	def getPlayerBySeat( self, seat ): return self.seats.get( (abs(seat-1) % len(self.seats))+1, None )
	def getPlayers( self, state=None ): return filter( lambda p: p.isState( state ), self.players.values() ) if state else self.players.values()
	def setPlayer( self, player ): 
		self.players[ player.pid ] = player
		#self.emit( 'addplayer', player, player.name, player.stack )

	def getPlayer( self, pid, request=None ): 
		player = self.players.get( pid, None ) 
		if not player and request:
			player = players.getPlayerFromRequest( pid, self, request )
			if player: self.setPlayer( player )
		return player
		
	def getCurrent(self): return self.current
	def setCurrent(self, current): 
		self.current = current
		if self.current: self.current.update()
		return self.public( 'current', self.current )
		
	def getDealer( self ): return self.dealer
	def setDealer( self, dealer ): 
		self.dealer = dealer
		return self.public( 'dealer', self.dealer )
		
	def reset( self ):
		self.deck = []
		for i in self.cards: self.cards[ i ] = []
		for i in self.bets: self.bets[ i ] = []
		return self.public( 'reset' )

	def betCeil(self):
		ceil = 0
		for bets in self.bets.values(): 
			total = 0
			for bet in bets:
				for value, count in bet.items(): 
					total += count * value
				if total > ceil: ceil = total
		return ceil
	
	def showCard( self ):
		card = self.deck.pop()
		self.cards[ -1 ].append( card )
		return self.public( 'showcard', card )
		
	def giveCard( self, seat, card ): 
		self.cards[ seat.seat ].append( card )
		return self.public( 'givecard', seat )
		
	def burnCard( self ): 
		self.cards[ -2 ].append( self.deck.pop() )
		return self.public( 'burncard' )
	
	def refresh(self):
		if self.isTimeOut(): 
			self.resume( )
			self.update()
		return True
					
	def update(self): 
		self.updated_at = time.time()
		self.timeout = False
		return True
	def setTimeOut( self, delay=None ): 
		self.delay = delay
		return True
	def forceTimeOut( self, boolean=False ): 
		self.timeout = boolean 
		return True
	def isTimeOut( self ): return self.timeout or time.time() - self.updated_at > self.delay
				
