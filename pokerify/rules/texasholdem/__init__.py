import random, math
from pokerify.core import players, cards, rooms, money

#DELAYS
DELAY_FAST = 0.4
DELAY_NORMAL = 2.00
DELAY_MEDIUM = 2#6.00
DELAY_LARGE = 2#46.00
DELAY_PLAYER = 50#10.00


#EVENTS
ROOM_SEATS, PLAYER_CURRENT, PLAYER_DEALER, PLAYER_STATE, PLAYER_BET, ROOM_STATE, \
PLAYER_SIT, PLAYER_CARD, PLAYER_CARDS, ROOM_SHOWCARDS, ROOM_SHOWCARD, \
ROOM_BURNCARD, PLAYER_FOLD, PLAYER_STACK, WIN, RESULT, LOOKUP, OWNER = xrange(18)
		
#ROOM STATES
NOSTATE, NEW, SERVING, PREFLOP, FLOP, TURN, RIVER, END = xrange(8)
INTURN = [PREFLOP, FLOP, RIVER, TURN]

#PLAYER STATES
NOSTATE, IDLE, UP, WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN = xrange(10)

ONSEAT = [UP, WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN]
SIT = [WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN]
PLAYING = [FOLD, CALL, CHECK, RAISE, ALLIN]
ALIVE = [READY, CALL, CHECK, RAISE, ALLIN]
BET = [CALL, RAISE, ALLIN]
CAN_BET = [READY, CALL, RAISE]

class Player( players.Player ):
	
	def event_setState( self, state ): self.room.addEvent( [ PLAYER_STATE, self, state ] )
	def event_addBet( self, chips ): 
		self.room.addEvent( [ PLAYER_BET, self, chips ] )
		self.room.addEvent( [ PLAYER_STACK, self, self.chips ] )
		
	def play( self ):
		i = int(random.random()*100)
		if i >= 95: self.command_allin( )
		elif i >= 85: self.command_raise( )
		elif i >= 70: self.command_fold( )
		elif i >= 30: self.command_call( )
		else: self.command_check( )
		
	def command_sitdown( self ):
		if self.setSeat( ):
			self.setState( WAITING )
			return self.room.command_resume( self )
		return False

	def command_situp( self ):
		if self.setState( UP ): return self.room.command_resume( self )
		return False
	
	def command_lookup( self ):
		cards = self.getCards()
		if cards:
			#self.public( 'lookup', pl )
			#self.private( 'lookup', pl, cards )
			return self.pong()
		return False		
	
	def command_fold( self ):	
		if self.isState( [ READY, CHECK, CALL, RAISE ] ) and self.room.isState( INTURN ):
			cards = self.popCards()
			self.setState( FOLD )
			self.room.setCurrent( self.next( 1, state=[ READY, CALL, RAISE ] ) )
			return self.room.command_resume( self )
		return False
		
	def command_check( self ):	
		if self.isState( [ READY, CHECK, CALL, RAISE ] ) and self.room.isState( INTURN ) and self.betsamount == self.room.betsceil:
			self.setState( CHECK )
			self.room.setCurrent( self.next( 1, state=[ READY, CHECK, CALL, RAISE ] ) )			
			return self.room.command_resume( self )
		return False
	
	def command_call( self ):	
		if self.isState( [ READY, CHECK, CALL, RAISE ] ) and self.room.isState( INTURN ) and self.betsamount < self.room.betsceil:
			chips = self.addBet( self.room.betsceil - self.betsamount )
			self.setState( CALL )
			self.room.setCurrent( self.next( 1, state=[ READY, CHECK, CALL, RAISE ] ) )
			return self.room.command_resume( self )
			
		return False
		
	def command_raise( self, amount=0 ):
		if self.isState( [ READY, CHECK, CALL, RAISE ] ) and self.room.isState( INTURN ): 
			chips = self.addBet( self.room.betsceil*2 )
			self.setState( RAISE )
			self.room.setCurrent( self.next( 1, state=[ READY, CHECK, CALL, RAISE ] ) )
			return self.room.command_resume( self )
		return False
		
	def command_allin( self ):	
		if self.isState( [ READY, CHECK, CALL, RAISE ] ) and self.room.isState( INTURN ): 
			chips = self.addBet( amount=self.chips.amount )
			self.setState( ALLIN )
			self.room.setCurrent( self.next( 1, state=[ READY, CHECK, CALL, RAISE ] ) )
			return self.room.command_resume( self )		
		return False

class Room( rooms.Room ):	
	
	def event_setState( self, state ): self.addEvent( [ ROOM_STATE, state ] )
	def event_addCard( self, card ): self.addEvent( [ ROOM_SHOWCARD, card ] )
	def event_setCurrent( self, current ): self.addEvent( [ PLAYER_CURRENT, current ] )
	def event_setDealer( self, dealer ): self.addEvent( [ PLAYER_DEALER, dealer ] )
	
	def __init__( self, *args, **kwargs ):
		rooms.Room.__init__( self, *args, **kwargs )
		self.reset()
		
	def reset( self ): 
		self.burned = []
		self.betsamount = 0
		self.betsceil = 0
		self.cards = []
		self.bets = []
		self.current = 0
		self.dealer = 0
		self.blinds = [100, 200]
		self.deck = []

		for player in self.players: 
			player.cards = []
			player.bets = []
			player.betsamount = 0
	
		
	def createPlayerFromRequest( self, pid, request ):
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
			player = Player( pid, self, 
				jokers=jokers,
				name=name,
				stack=stack,
				fake=fake
			)
			return player
		return None
		
	def command_enter( self, player ):
		player.events = []
		
		player.addEvent( 
			[ ROOM_SEATS, self.seat_positions ],
			[ ROOM_STATE, self.state ],
			[ PLAYER_CURRENT, self.current ],
			[ PLAYER_DEALER, self.dealer ], 
			[ OWNER, player ],
		)
		for p in self.getPlayers( state=[ WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN ] ):
			player.addEvent(
				[ PLAYER_STATE, p, p.state ],
				[ PLAYER_STACK, p, p.chips ]
			) 
			for c in p.cards: player.addEvent( [ PLAYER_CARD, p, c ] )
			for b in p.bets: player.addEvent( [ PLAYER_BET, p, b ] )
				
		for card in self.cards: player.addEvent( [ ROOM_SHOWCARD, card ] )
			

		return self.command_resume( player )
		
	def command_addfake( self, player ):		
		self.getPlayer( 2, { 'name':"Kane", 'stack': 20000, 'fake':True } )
		self.getPlayer( 3, { 'name':"Undertaker", 'stack': 5000, 'fake':True } )
		self.getPlayer( 4, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
		self.getPlayer( 5, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
		self.getPlayer( 6, { 'name':"The miz", 'stack': 120000, 'fake':True } )
		self.getPlayer( 7, { 'name':"Cena", 'stack': 10000, 'fake':True } )
		self.getPlayer( 8, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
		self.getPlayer( 9, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
		self.getPlayer( 10, { 'name':"The miz", 'stack': 120000, 'fake':True } )
		self.getPlayer( 11, { 'name':"Cena", 'stack': 10000, 'fake':True } )
		self.getPlayer( 12, { 'name':"The miz", 'stack': 120000, 'fake':True } )
		self.getPlayer( 13, { 'name':"Cena", 'stack': 10000, 'fake':True } )
		self.getPlayer(14, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
		for p in self.getPlayers(): 
			if p.fake : p.command_sitdown( )
		
		 
		
	def command_resume( self, player ):
		
		if self.isTimeOut(): 
		
			if self.isState( NEW ): 
				
				sitplayers = self.getPlayers( state=[ WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN ] )
			
				if len( sitplayers ) > 1:
	
					for p in sitplayers: 
						p.setState( WAITING )
						p.setTimeOut( DELAY_PLAYER ) 
		
					self.reset() 
					self.setDeck( cards.deck52() ) 
					cards.shuffle( self.deck ) 
					self.setDealer( self.dealer.next( 1, state=WAITING ) if self.dealer else self.getPlayer( seat=1 ) )
					
					for count, blind in enumerate( self.blinds ):  self.dealer.next( count + 1, state=WAITING ).addBet( amount=blind )
									
					self.setCurrent( self.dealer.next( len( self.blinds ) + 1, state=WAITING ) )
					self.addEvent( [ PLAYER_CURRENT, self.current ] )
					self.setTimeOut( DELAY_NORMAL ) 
					self.setState( SERVING )
			
			elif self.isState( SERVING ): 
				if self.current: 
									
					card = self.deck.pop()
					self.current.addCard( card )
					self.addEvent( [ PLAYER_CARD, self.current, card ] )
					
					if len( self.current.cards ) >= 2 : self.current.setState( READY ) 
					
					self.setCurrent( self.current.next( 1, state=WAITING ) )
					self.setTimeOut( DELAY_FAST )
				else: 
					self.setCurrent( self.dealer.next( 3, state=READY ) )
					self.setTimeOut( DELAY_MEDIUM ) 
					self.setState( PREFLOP )
					self.betscount = 0
			
			
			elif self.isState( INTURN ): 
			
				alives = self.getPlayers( state=[ READY, CALL, CHECK, RAISE, ALLIN ] )
				
				if self.current and len( self.current.bets ) < 2 and len( alives ) > 1:
										
					#p.executeRequest( )
					
					if self.current.isTimeOut(): 
						self.current.popCards()
						self.current.setState( UP )
					else:
						if self.current.fake: self.current.play(  )

					self.setTimeOut( DELAY_NORMAL )
					
				else:
					
					
					can_bet = self.getPlayers( state=[ READY, CALL, CHECK, RAISE ] )
					
					print 'FIN DU TOUR', self.state, self.betscount, len( can_bet )
										
					if len( alives ) <= 1: self.setState( END )
					else:
						
						for p in can_bet: 
							for b in p.bets:
								self.bets.append( p.bets.pop() )
							p.setState( READY )
						
						self.betscount = 0
						self.setCurrent( self.dealer.next( 3, state=READY ) )
						self.setTimeOut( DELAY_MEDIUM )
					
						if self.isState( PREFLOP ): 
							self.burned.append( self.deck.pop().setVisible( False ) ) #Burn 1 card
							self.addEvent( [ ROOM_BURNCARD ] )
							for i in xrange(3): self.addCard( self.deck.pop().setVisible( True ) ) #Show 3 cards
							self.setState( FLOP )							
							
						elif self.isState( FLOP ): 
							self.burned.append( self.deck.pop().setVisible( False ) ) #Burn 1 card
							self.addEvent( [ ROOM_BURNCARD ] )
							self.addCard( self.deck.pop().setVisible( True ) ) #Show 1 card
							self.setState( TURN )
							
						elif self.isState( TURN ): 
							self.burned.append( self.deck.pop().setVisible( False ) ) #Burn 1 card
							self.addEvent( [ ROOM_BURNCARD ] )
							self.addCard( self.deck.pop().setVisible( True ) ) #Show 1 card
							self.setState( RIVER )
							
						elif self.isState( RIVER ):
							self.setState( END )
							
			
			
			elif self.isState( END ): 
				print 'END'
				winners = [[0, 0, 0, 0]]
				for p in self.getPlayers( state=BET ): 
	
					serie, score, hand5 = cards.resolve_hand( p.cards + self.cards )
					#print '%s : %s %s %s' % (p.player().name(), serie, score, hand5)
					if ( len(winners) and winners[0][2] < score ) or ( not len(winners) ):
						winners = [[ p, serie, score, hand5 ]]
				
					#temp
					#p.addStack( 4000 )
				
				if winners[0][0]: 
	
					winners[0][0].addChips( amount = self.betsamount )
					#self.public( 'winner', winners[0][0], winners[0][1], winners[0][2], winners[0][3] )
					
				
				#print 'winner is : %s' % self._winners[0]
				
				for p in self.getPlayers( state=PLAYING ):
					if p.chips.amount <= 0:
						p.setState( UP )
				
				self.setTimeOut( DELAY_LARGE )
				self.setState( NEW )
		
		
		return player.pong()
		 

					
			
		
		
				
