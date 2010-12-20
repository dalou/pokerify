# -*- coding: utf8 -*-

import random, time, types, math
from bisect import bisect
from pokerify.core import cards, money, pong

T_DELAY = 200000




class Player(  ):

	def __repr__( self ): return str(self.seat)	
	def __init__( self, pid, room, name='', level=0, stack=10000, fake=False, jokers={}):

		self.pid = 					pid
		
		self.room = 				room
		self.name =					name
		self.state =				1
		self.level =				level

		self.seat =					0
		self.fake =					fake
		self.data =					0
		self.request =				None
			
		self.delay =				T_DELAY
		self.created_at =			time.time()
		self.updated_at =			time.time()
		self.timeout =				False
		
		self.events =				[]
		self.jokers = 				jokers
		self.chips =				money.Chips( stack, self.room.tokens )
		self.cards =				[]
		self.bets =					[]
		self.betsamount =			0
		
		
# EVENT SYSTEM

	def addEvent( self, *args ):
		if not self.fake:
			for arg in args: self.events.append( arg )
		return True

	def pong( self ):		
		if not self.fake: 			
			events = list( self.events )
			self.events = []
			return events
		return False
		
# CARD SYSTEM

	# PERFECT SYSTEM
	def event_addCard( self, card ): pass
	def addCard( self, card ):
		self.cards.append( card )
		self.event_addCard( card )
		return True
	#def getCard( self, id ): return self.cards.get
	
	# PERFECT SYSTEM
	def event_popCard( self, card ): pass
	def popCard( self, id=None ): 
		if not id: 
			card = self.cards.pop( )
			self.event_popCard( card )
			return card	
		return True	
		
	# PERFECT SYSTEM
	def event_popCards( self, cards ): pass
	def popCards( self ): 
		cards = list( self.cards )
		self.cards = []
		self.event_popCards( cards )
		return cards

	# PERFECT SYSTEM
	def next( self, count=1, state=None ):		
		seats = []
		players = self.room.getPlayers( state=state )
		if not len( players ): return 0
		for player in players: seats.append( player.seat )		
		sseats = sorted(seats)
		seat = sseats[ ( bisect( sseats, self.seat ) - 1 + count ) % len( players ) ]		
		return players[ seats.index( seat ) ]    
	def prev( self, count=1, state=None ): return self.next( count=-count, state=state )
	
	#def executeRequest( self ): return self.request[0]( self.request[1] ) if self.request else None
	
	# PERFECT SYSTEM
	def isState( self, state): return self.state in state if type(state) == types.ListType else self.state is state
	
	# PERFECT SYSTEM
	def event_setState( self, state ): pass
	def setState( self, state ): 
		if state == self.state: return True
		self.state = state
		self.event_setState( state )
		return self.update()# and self.room.forceTimeOut( True )
	
	# PERFECT SYSTEM	
	def event_setSeat( self, seat ): pass
	def setSeat( self, seat=None ):		
		if self.seat: 
			if not seat or seat == self.seat: return False
			else: seat = self.seat
		if not seat: 
			places = range( 1, self.room.places )			
			for player in self.room.players:
				if player.seat: places.remove( player.seat )
			if len(places): seat = places[0]
		if seat: 			
			self.seat = seat
			self.event_setSeat( self.seat )
			return True
		
		return False
			
	# PERFECT SYSTEM
	def event_addChips( self, chips ): pass
	def addChips(self, amount=None, chips=None ):
		if chips: self.chips.addChips( chips )
		elif amount: self.chips.addAmount( amount )
		self.event_addChips( self.chips )
		return True
	
	# PERFECT SYSTEM
	def event_popChips( self, chips ): pass
	def popChips( self, amount=None, chips=None ):		
		if chips: chips = self.chips.popChips( chips )			
		elif amount and amount > 0: chips = self.chips.popAmount( amount )
		self.event_popChips( chips )
		return chips
		
	def event_addBet( self, chips ): pass
	def addBet( self, amount=None, chips=None ):
		chips = self.chips.popAmount( amount )
		self.bets.append( chips )
		self.betsamount += chips.amount
		self.room.betsamount += chips.amount
		if self.betsamount > self.room.betsceil: self.room.betsceil = self.betsamount
		if len( self.bets ) >= self.room.betscount:  self.room.betscount = len( self.bets )
		self.event_addBet( chips )
		return chips
	
# TIMEOUT SYSTEM

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
	def isTimeOut( self ): return self.timeout or time.time() - self.updated_at > self.delay
		

	"""self.betstotal += chips.amount
	self.room.betstotal += chips.amount
	if self.room.betsceil < chips.amount: self.room.betsceil = chips.amount
	
	self.room.bets[ self.seat ].append( chips )
	if self.room.betscount < len(self.room.bets[ self.seat ]): self.room.betscount = len(self.room.bets[ self.seat ])

	return self.public( { 'players' : { self : { 'bet' : chips } } } )"""
    
    
    
# BETING SYSTEM

	
				
	# model : chips = { 1000: 4, 200: 2 }
	"""def betChips( self, chips ):
		
		chips = money.popChipsToChips( chips, self.chips )
		self.room.bets[ self.seat ].append( chips )
		return self.public( 'bet', self, chips )"""
	
	"""def getBets( self  ): return self.room.bets.get( self.seat,  [] )

	

		
	"""

    
	
	





		
		
 
