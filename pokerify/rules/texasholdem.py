import random, time, types
from pokerify.core import cards, rooms

#DELAYS
DELAY_NORMAL = 1.00
DELAY_MEDIUM = 2#6.00
DELAY_LARGE = 2#46.00
DELAY_PLAYER = 5555555#10.00

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

class TexasHoldem( rooms.Room ):
	
	#def __init__( self, *args, **kwargs ):
		#rooms.Room.__init__( self, *args, **kwargs )
		
	def resume( self ):
		
		if self.isState( NEW ): 
		
			if len( self.getPlayers( state=SIT ) ) > 1:

				for p in self.getPlayers( ): p.setTimeOut( DELAY_PLAYER ) and p.isState( SIT ) and p.setState( WAITING )
				self.reset() and self.setDeck( cards.deck52() ) and cards.shuffle( self.deck )
				if not self.getDealer(): self.setDealer( self.getPlayerBySeat( 1 ) )
				else: self.setDealer( self.getDealer().next( 1, state=WAITING ) )
				for count, blind in enumerate( self.blinds ): self.getDealer().next( count + 1, state=WAITING ).bet( blind )
				self.setCurrent( self.getDealer().next( len( self.blinds ) + 1, state=WAITING ) ) and self.setTimeOut( DELAY_NORMAL ) and self.setState( SERVING )
		
		elif self.isState( SERVING ): 
		
			p = self.getCurrent()
			if p:
				self.giveCard( p, self.deck.pop() )
				if len( p.getCards() ) >= 2: p.setState( READY )
				self.setCurrent( p.next( 1, state=WAITING ) ) and self.setTimeOut( DELAY_NORMAL )
			else:
				self.setCurrent( self.getDealer().next( 3, state=READY ) ) and self.setTimeOut( DELAY_MEDIUM ) and self.setState( PREFLOP )
		
		
		elif self.isState( INTURN ): 
		
			p = self.getCurrent()
			if p:
				#p.executeRequest( )
				if p.fake: 
					i = int(random.random()*100)
					if i >= 95: p.ping( 'allin' )
					elif i >= 65: p.ping( 'raiseby', { 'amount': 1000 })
					elif i >= 45: p.ping( 'call' )
					elif i >= 15: p.ping( 'check' )
					else : p.ping( 'fold' )
				
				if p.isTimeOut(): p.foldCards() and p.setState( UP )
				
				if not p.isState( READY ): self.setCurrent( p.next( 1, state=READY ) ) 
				self.setTimeOut( DELAY_NORMAL )
				
			else:
				if len( self.getPlayers( state=HAS_BET ) ) <= 1: 
					
					self.setState( END )
				else:
					for p in self.getPlayers( state=HAS_PLAYED ): 
						#p.bets_to_r()
						if not p.isState( ALLIN ): p.setState( READY )
						
					self.setCurrent( self.getDealer().next( 3, state=READY ) ) and self.setTimeOut( DELAY_MEDIUM )
				
					if self.isState( PREFLOP ): self.burnCard() and self.showCard() and self.showCard() and self.showCard() and self.setState( FLOP )
					elif self.isState( FLOP ): self.burnCard() and self.showCard() and self.setState( TURN )
					elif self.isState( TURN ): self.burnCard() and self.showCard() and self.setState( RIVER )
					elif self.isState( RIVER ): self.setState( END ) and self.emit( STATE, self.state )
		
		
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
				h = 0
				for p in self.getPlayers( state=HAS_BET ): 
					h += p.betSum()
				winners[0][0].addStack( h )
				self.emit( 'winner', winners[0][0], winners[0][1], winners[0][2], winners[0][3] )
				
			
			#print 'winner is : %s' % self._winners[0]
			
			for p in self.getPlayers( state=HAS_PLAYED ):
				if p.stack <= 0:
					p.setState( UP )
			
			self.setTimeOut( DELAY_LARGE )
			self.setState( NEW )
		
		
			
		 

					
			
		
		
				
