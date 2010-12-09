import random
from pokerify.core import players, cards, rooms, money

#DELAYS
DELAY_FAST = 0
DELAY_NORMAL = 1.00
DELAY_MEDIUM = 2#6.00
DELAY_LARGE = 2#46.00
DELAY_PLAYER = 50#10.00

PLAYER, ROOM = xrange(2)

#SIGNALS
RESET, CURRENT, DEALER, PLAYER_STATE, BET, ROOM_STATE, PLAYER_SEAT, PLAYER_CARD, SHOWCARD, \
PSHOWCARD, BURNCARD, PBURNCARD, STACK, WIN, RESULT, LOOKUP = xrange(16)

def signals2json():pass
	

#ROOM STATES
NOSTATE, NEW, SERVING, PREFLOP, FLOP, TURN, RIVER, END = xrange(8)
INTURN = [PREFLOP, FLOP, RIVER, TURN]

#PLAYER STATES
NOSTATE, IDLE, UP, WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN = xrange(10)

INGAME = [UP, WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN]
SIT = [WAITING, READY, FOLD, CALL, CHECK, RAISE, ALLIN]
HAS_PLAYED = [FOLD, CALL, CHECK, RAISE, ALLIN]
HAS_BET = [CALL, CHECK, RAISE, ALLIN]
CAN_BET = [READY, CALL, CHECK, RAISE]

class Player( players.Player ):
	
	bets = []
	
	def event_setState( self, state ): self.addEvent( False, PLAYER_STATE, self, state )
	def event_addCard( self, card ): self.addEvent( False, PLAYER_CARD, self, card )
	def event_popCard( self, card ): pass
	def event_popCards( self, cards ): pass
	def event_setSeat( self, seat ): self.addEvent( False, PLAYER_SEAT, self, seat )
	def event_addChips( self, chips ): pass
	def event_popChips( self, chips ): pass
	
	def bet( self, amount=None, chips=None ):
		chips = self.chips.popAmount( amount )
		self.bets.append( chips )
		
	def play( self ):
		i = int(random.random()*100)
		#if i >= 95: p.ping( 'allin' )
		#elif i >= 65: p.ping( 'raiseby', { 'amount': 1000 })
		if i >= 90: self.command_fold( )
		elif i >= 50: self.command_call( )
		else: self.command_check( )
		
	def command_sitdown( self ):
		if self.setSeat( ) and self.setState( WAITING ): return self.room.command_resume( self )
		return False

	def command_situp( self, ca, pl ):	
		if self.setState( UP ): return self.room.command_resume( self )
		return False
	
	def command_lookup( self, ca, pl ):
		cards = self.getCards()
		if cards:
			#self.public( 'lookup', pl )
			#self.private( 'lookup', pl, cards )
			return self.pong()
		return False		
	
	def command_fold( self ):	
		if self.isState( READY ) and self.room.isState( INTURN ):
			cards = self.popCards()
			self.setState( FOLD )	
			#self.addEvent( PLAYER, player )
			return self.room.command_resume( self )					
		return False
		
	def command_check( self ):	
		if self.isState( READY ) and self.room.isState( INTURN ) and self.betstotal == self.room.betsceil \
		  and self.setState( CHECK ): return self.room.resume( self )
		return False
	
	def command_call( self ):	
		if self.isState( READY ) and self.room.isState( INTURN ) and self.betstotal < self.room.betsceil \
		  and self.bet( self.room.betsceil - self.betstotal ) and self.setState( CALL ): return self.room.resume( self )
		return False
		
	def command_raise( self ):
		if self.isState( READY ) and self.room.isState( INTURN ) and self.room.bet( ro.betsceil*2 ) \
		  and self.setState( RAISE ): return self.room.resume( self )
		return False
		
	def command_allin( self ):	
		if self.isState( READY ) and self.room.isState( INTURN ) and self.bet( amount=self.chips.amount ) \
		  and self.setState( ALLIN ): return self.room.resume( self )		
		return False

class Room( rooms.Room ):	
	
	def event_setState( self, state ): self.addEvent( False, ROOM_STATE, state )
	def event_setDeck( self, deck ): pass
	def event_addPlayer( self, player ): pass
	
	def __init__( self, *args, **kwargs ):
		rooms.Room.__init__( self, *args, **kwargs )
		self.reset()
		
	def reset( self ): 
		self.burned = []
		self.betstotal = 0
		self.betsceil = 0
		self.cards = []
		self.current = 0
		self.dealer = 0
		self.blinds = [100, 200]
		return True
		
	def setCurrent( self, current ):
		self.current = current
		return True
		
	def setDealer( self, dealer ):
		self.dealer = dealer
		return True
	
		
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
		
	
	
		
	def command_enter( self, player=None ):
		
		player.addEvent( True, ROOM, [ RESET, [] ] )
		"""self.events = { 
			'reset' : 1,
			'state' : self.state,
			'current': self.current,
			'dealer' : self.dealer,
			'players' : {},
			'owner' : pl,
			'cards' : self.cards
		}
		for p in self.getPlayers( ): 
			if p.seat:
				self.events['players'][ p ] = {
					'bets' : p.getBets(),
					'chips' : p.chips,
					'cards' : p.getCards(),
				}"""
		#for card in self.room.cards[-1]: self.events['cards'].append( card ) #pong.showcard( pl, card )
		
		return self.command_resume( player )
		
	def command_addfake( self, player ):		
		self.getPlayer( 2, { 'name':"Kane", 'stack': 20000, 'fake':True } )
		self.getPlayer( 3, { 'name':"Undertaker", 'stack': 5000, 'fake':True } )
		self.getPlayer( 4, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
		self.getPlayer( 5, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
		self.getPlayer( 6, { 'name':"The miz", 'stack': 120000, 'fake':True } )
		self.getPlayer( 7, { 'name':"Cena", 'stack': 10000, 'fake':True } )

		for p in self.getPlayers(): p.command_sitdown( )
		
	def command_resume( self, player ):
		
		if not self.isTimeOut(): return False
		
		if self.isState( NEW ): 
		
			if len( self.getPlayers( state=WAITING ) ) > 1:

				for p in self.getPlayers( state=WAITING ): p.setTimeOut( DELAY_PLAYER ) 
	
				self.reset() 
				self.setDeck( cards.deck52() ) 
				cards.shuffle( self.deck ) 
				self.setDealer( self.dealer.next( 1, state=WAITING ) if self.dealer else self.getPlayer( seat=1 ) )
				
				for count, blind in enumerate( self.blinds ): 
					self.dealer.next( count + 1, state=WAITING ).bet( blind )		
								
				self.setCurrent( self.dealer.next( len( self.blinds ) + 1, state=WAITING ) ) 
				self.setTimeOut( DELAY_NORMAL ) 
				self.setState( SERVING )
		
		elif self.isState( SERVING ): 
		
			if self.current: 
				self.current.addCard( self.deck.pop() ) 
				self.current.setState( READY if len( self.current.cards ) >= 2 else self.current.state ) 
				self.setCurrent( self.current.next( 1, state=WAITING ) ) 
				self.setTimeOut( DELAY_FAST )
			else: 
				self.setCurrent( self.dealer.next( 3, state=READY ) ) 
				self.setTimeOut( DELAY_MEDIUM ) 
				self.setState( PREFLOP )
		
		
		elif self.isState( INTURN ): 
		
			if self.current:
				#p.executeRequest( )
				if self.current.fake: self.current.play(  )				
				if self.current.isTimeOut(): 
					self.current.foldCards()
					self.current.setState( UP )
				
				if not self.current.isState( READY ): self.current = self.current.next( 1, state=READY )
				self.setTimeOut( DELAY_NORMAL )
				
			else:
				if len( self.getPlayers( state=HAS_BET ) ) <= 1: 
					
					self.setState( END )
				else:
					for player in self.getPlayers( state=CAN_BET ): player.setState( READY )
						
					self.current = self.dealer.next( 3, state=READY ) 
					self.setTimeOut( DELAY_MEDIUM )
				
					if self.isState( PREFLOP ): self.burnCard() and self.showCard() and self.showCard() and self.showCard() and self.setState( FLOP )
					elif self.isState( FLOP ): self.burnCard() and self.showCard() and self.setState( TURN )
					elif self.isState( TURN ): self.burnCard() and self.showCard() and self.setState( RIVER )
					elif self.isState( RIVER ): self.setState( END )
		
		
		elif self.isState( END ): 
			
			winners = [[0, 0, 0, 0]]
			for p in self.getPlayers( state=HAS_BET ): 

				serie, score, hand5 = cards.resolve_hand( p.getCards() + self.cards[ -1 ] )
				#print '%s : %s %s %s' % (p.player().name(), serie, score, hand5)
				if ( len(winners) and winners[0][2] < score ) or ( not len(winners) ):
					winners = [[ p, serie, score, cards.card2str(hand5) ]]
				print '%s with %s' % ( serie, cards.card2str(hand5) )
			
				#temp
				#p.addStack( 4000 )
			
			if winners[0][0]: 

				winners[0][0].addStack( self.betstotal )
				self.public( 'winner', winners[0][0], winners[0][1], winners[0][2], winners[0][3] )
				
			
			#print 'winner is : %s' % self._winners[0]
			
			for p in self.getPlayers( state=HAS_PLAYED ):
				if p.chips.amount <= 0:
					p.setState( UP )
			
			self.setTimeOut( DELAY_LARGE )
			self.setState( NEW )
		
		
		if player: return player.pong()
		 

					
			
		
		
				
