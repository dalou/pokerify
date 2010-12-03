# -*- coding: utf8 -*-

import random, time, types
from pokerify.core import cards, money, pong

T_DELAY = 200000

def getPlayerFromRequest( pid, room, request ):
	jokers = {}
	try:		
		_jokers = eval(request.get( 'jokers' ))
		for joker in _jokers:
			print joker
			#jokers[ joker ] = 
	except: pass
	
	name = request.get('name')
	stack = request.get('stack')
	fake = request.get('fake')
	
	if name:
		player = Player( pid, room, 
			jokers=jokers,
			name=name,
			stack=stack,
			fake=fake
		)
		return player
	return None

class Player(  ):
   
	def __init__(self, pid, room, name='', level=0, stack=10000, fake=False, jokers={}):

		self.pid = 					pid
		self.room = 				room
		self.name =					name
		self.state =				1
		self.level =				level
		self.stack =				float(stack)
		
		self.seat =					0
		self.fake =					fake
		self.data =					0
		self.request =				None		
		self.delay =				T_DELAY
		self.created_at =			time.time()
		self.updated_at =			time.time()
		self.timeout =				False
		#self.sig_i =				0
		#self.rsig_i =				0
		self.events =				[]
		self.jokers = 				jokers
		self.chips =				money.stack2Chips( stack, self.room.tokens )
		#print stack, count, chips[ value ]
		total = 0
		for v,c in self.chips.items(): total += c*v
		print self.chips, self.name, self.stack , total

		
		

# EVENT SYSTEM

	def ping( self, command, args={} ):
		args['rid'] = self.room.rid
		args['pid'] = self.pid
		self.room.ping( command, args )		
	def __repr__( self ): return str(self.seat)	
	def private( self, *args ): 
		self.events.append( list(args) )
		return True
	def public( self, *args ): return self.room.public( *args )  

	def resetEvents( self ):
		self.events = []
	def pong( self ):
		events = list(self.events)
		self.events = []
		return events
		
	def resume( self ):
		self.events = []
		self.private( 'reset' )
		self.private( 'turn', self.room.state )
		self.private( 'dealer', self.room.dealer )
		self.private( 'current', self.room.current )
		for p in self.room.getPlayers( ): 
			if p.seat:
				self.private( 'bets', p, p.getBets() )
				self.private( 'chips', p, p.chips )
		self.private( 'owner', self )
		for card in self.room.cards[-1]: self.private( 'showcard', card ) #pong.showcard( pl, card )
		

	

		
# CARD SYSTEM
	
	def getCards( self ): return self.room.cards.get( self.seat, [] )	
	def foldCard( self, card=None ):
		cards = self.getCards()
		if cards:
			popcard = cards.pop( card.index( card ) ) if card else cards.pop()
			self.public( 'foldcard', self, popcard )
			return popcard
		return card		
	def foldCards( self ):
		cards = self.getCards()
		cards = []
		self.public( 'foldcards', self )
		return True
		

	

		
# STATE SYSTEM
		
	def isCurrent( self ): return self.room.current and self.seat == self.room.current.seat
	def isDealer( self ): return self.room.dealer and self.seat == self.room.dealer.seat
	def next( self, count=1, state=None ): #r.dealer.next( count + 1, lambda p : p.isState( WAITING )
		for i in self.room.seats:
			p = self.room.getPlayerBySeat( self.seat+count )
			count += 1
			if p and ( p.isState( state ) or state == None ): return p
		return 0		
	def prev( self, count=1, state=None ): return self.next( count=-count, state=state )
	#def executeRequest( self ): return self.request[0]( self.request[1] ) if self.request else None
	def isState( self, state): return self.state in state if type(state) == types.ListType else self.state is state
	def setState( self, state ): 
		self.state = state
		self.request = None
		return self.update() and self.room.forceTimeOut( True ) and self.public( 'state', self, self.state )
	
	# TODO : refact		
	def setSeat( self, seat=None ):
		if self.seat: seat = self.seat
		if not seat: seat = self.room.getEmptySeat()
		if seat: 
			self.room.seats[ seat ] = self
			self.seat = seat
			self.private( 'owner', self )
			return True#pong.state( self.room, self, self.seat )
		return False
			


		
    
    
    
    
# BETING SYSTEM

	
				
	# model : chips = { 1000: 4, 200: 2 }
	def betChips( self, chips ):
		for value, count in chips.items():
			if count > 0 and value in self.chips and self.chips[ value ] >= count:
				self.chips[ value ] -= count
			else : return False
		self.room.bets[ self.seat ].append( chips )
		return self.public( 'bet', self, chips )
	def getBets( self  ): return self.room.bets[ self.seat ]

	def bet( self, amount ):
		return True
		if amount > 0:
			total = 0
			for value, count in self.chips.items():
				total += count *  value
				if total % amount == 0: return self.betChips( { value: total / amount } )
		return False
		
	def betSum( self ): 
		count = 0
		bets = self.room.bets.get( self.seat,  [] )
		for chips in bets: 
			for value, count in chips.items():
				count += count * value
		return count
			
	def addStack(self, chips=None, amount=None):
		if chips:
			for value, count in self.chips.items():
				self.chips[ value ] += count
		elif amount:
			
		# TODO connect with django to update stack
		self.stack += stack
		return self.room.emit( 'p_stack', self, self.stack )

    
	
	




# TIMEOUT SYSTEM

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
		
		
 
