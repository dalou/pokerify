import random, time, types
from pokerify.core import players, cards, rooms, money
from pokerify.rules.texasholdem import bots

#DELAYS
DELAY_FAST = 0
DELAY_NORMAL = 1.00
DELAY_MEDIUM = 2#6.00
DELAY_LARGE = 2#46.00
DELAY_PLAYER = 50#10.00

PLAYER, ROOM = xrange(2)

#SIGNALS
RESET, CURRENT, DEALER, PLAYER, BET, STATE, PSTATE, GIVECARD, SHOWCARD, \
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
	
	def event_setState( self, state ): self.addEvent( PLAYER, 1, state )
	
	def bet( self, amount=None, chips=None ):
		chips = self.chips.popAmount( amount )
		self.bets.append( chips )

class Room( rooms.Room ):	
	
	def event_setState( self, state ): self.addEvent( ROOM, 1, state )
	
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
		
	
	
		
	def command_enter( self, ca, pl ):
		
		pl.addEvent( True, ROOM, [ RESET, [] ] )
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
		
		return self.command_resume( ca, pl )
		
	def command_addfake( self, ca, pl  ):		
		self.getPlayer( 2, { 'name':"Kane", 'stack': 20000, 'fake':True } )
		self.getPlayer( 3, { 'name':"Undertaker", 'stack': 5000, 'fake':True } )
		self.getPlayer( 4, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
		self.getPlayer( 5, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
		self.getPlayer( 6, { 'name':"The miz", 'stack': 120000, 'fake':True } )
		self.getPlayer( 7, { 'name':"Cena", 'stack': 10000, 'fake':True } )

		for p in self.getPlayers(): self.command_sitdown( ca, p )
		
	def command_sitdown( self, ca, pl ):
		if pl.setSeat( ) and pl.setState( WAITING ): return self.command_resume( ca, pl )
		return False

	def command_situp( self, ca, pl ):	
		if pl.setState( UP ): return self.command_resume( ca, pl )
		return False
	
	def command_lookup( self, ca, pl ):
		cards = pl.getCards()
		if cards:
			pl.public( 'lookup', pl )
			pl.private( 'lookup', pl, cards )
			return pl.pong()
		return False		
	
	def command_fold( self, ca, player ):	
		if player.isState( READY ) and self.isState( INTURN ):
			cards = player.popCards()
			player.setState( FOLD )	
			player.addEvent([ [PLAYER, player], [] ])
			return self.command_resume( ca, player )					
		return False
		
	def command_check( self, ca, pl ):	
		if pl.isState( READY ) and self.isState( INTURN ) and pl.betstotal == self.betsceil \
		  and pl.setState( CHECK ): return self.resume(  ca, pl  )
		return False
	
	def command_call( self, ca, pl ):	
		if pl.isState( READY ) and self.isState( INTURN ) and pl.betstotal < self.betsceil \
		  and pl.bet( self.betsceil - pl.betstotal ) and pl.setState( CALL ): return self.resume( ca, pl )
		return False
		
	def command_raise( self, ca, pl ):
		if pl.isState( READY ) and self.isState( INTURN ) and self.bet( ro.betsceil*2 ) \
		  and pl.setState( RAISE ): return self.resume( ca, pl )
		return False
		
	def command_allin( self, ca, pl):	
		if pl.isState( READY ) and self.isState( INTURN ) and pl.bet( amount=pl.chips.amount ) \
		  and pl.setState( ALLIN ): return self.resume( ca, pl )		
		return False
		
	def command_resume( self, ca=None, pl=None ):
		
		if not self.isTimeOut(): return False
		
		if self.isState( NEW ): 
		
			if len( self.getPlayers( state=SIT ) ) > 1:

				for p in self.getPlayers( ): p.setTimeOut( DELAY_PLAYER ) and p.isState( SIT ) and p.setState( WAITING )
				self.reset() and self.setDeck( cards.deck52() ) and cards.shuffle( self.deck ) and self.setDealer( self.getPlayer( seat=1 ) if not self.dealer else self.dealer.next( 1, state=WAITING ) )
				
				for count, blind in enumerate( self.blinds ): self.dealer.next( count + 1, state=WAITING ).bet( blind )					
				self.setCurrent( self.dealer.next( len( self.blinds ) + 1, state=WAITING ) ) and self.setTimeOut( DELAY_NORMAL ) and self.setState( SERVING )
		
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
				if self.current.fake: bots.play( self, ca, self.current )				
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
		
		
		if pl: return pl.pong()
		 

					
			
		
		
				
