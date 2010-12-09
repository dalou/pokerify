# -*- coding: utf8 -*-
import time, random, types

T_DELAY = 20

colors = 	[7,5,3,2]
flushs = 	[16807,3125,243,32]
#            A  Q  K  J  T  9  8  7  6  5  4  3  2
ranks = 	[61,59,53,43,41,37,31,29,23,19,17,13,11,61]
hights = 	[427,305,183,122,413,295,177,118,371,265,159,106,301,215,129,86,287,205,123,82,259,185,111,74,217,155,93,62,203,145,87,58,161,115,69,46,133,95,57,38,119,85,51,34,91,65,39,26,77,55,33,22,427,305,183,122]
straights = [336286961,203977337,107174533,58642669,31367009,14535931,6678671,2800733,1062347,2817529]
fours = 	[13845841,12117361,7890481,3418801,2825761,1874161,923521,707281,279841,130321,83521,28561,14641]
threes = 	[226981,205379,148877,79507,68921,50653,29791,24389,12167,6859,4913,2197,1331]
pairs =		[3721,3481,2809,1849,1681,1369,961,841,529,361,289,169,121]

cardsstr = 	['As','Ah','Ad','Ac','Ks','Kh','Kd','Kc','Qs','Qh','Qd','Qc','Js','Jh','Jd','Jc','Ts','Th','Td','Tc','9s','9h','9d','9c','8s','8h','8d','8c','7s','7h','7d','7c','6s','6h','6d','6c','5s','5h','5d','5c','4s','4h','4d','4c','3s','3h','3d','3c','2s','2h','2d','2c']


class Card():
	
	def __repr__( self ): return str( self.prime )
	def __init__( self, prime, visible=False ):
	   self.prime = prime
	   self.visible = visible
	  
	def visible( self, visible ):
		self.visible = visible

def deck52(): 
	cards = [] 
	for prime in hights: cards.append( Card( prime ) )
	return cards

def shuffle( cards ):
	random.shuffle(cards)
	random.shuffle(cards)
	random.shuffle(cards)
	return True
	


def move( cards1, cards2, count=1 ):
	for i in xrange( count ): cards2.append( cards1.pop() )

def search( hand, serie, cards, out=-1, add=1):
	rank_i = 0
	for rank in serie:
		if hand % (rank * add) == 0 and out != rank_i: return rank_i
		rank_i += 1
	return -1
		
def card2str(cards):
	nc = []
	for card in cards: nc.append( cardsstr[ hights.index(card) ] )
	return nc

def str2card(cards):
	nc = []
	for card in cards: nc.append( hights[ cardsstr.index(card) ] )
	return nc
	
def resolve_hand( cards ):

	hand = 1
	for card in cards: hand = hand * card

	# STRAIGHT FLUSH
	fl = search( hand, flushs, cards ) #looking for a flush	
	if fl > -1:
		st = search( hand, straights, cards, add=flushs[fl] ) #looking for a straight
		if st > -1: 
			return 'Straight Flush', 1000-st, hights[ fl+st*(2+fl) : fl+st*(2+fl)+17: 4 ]
	
	# FOUR OF A KIND
	fo = search( hand, fours, cards ) #looking for a four of kind
	if fo > -1: return 'Four of a kind', 900-fo, hights[fo*4:(fo*4)+4:1]
	
	# FULL
	th = search( hand, threes, cards ) #looking for a three
	if th > -1:
		pa = search( hand, pairs, cards, out=th ) #looking for a pair
		if pa > -1: return 'Full',800-th, hights[th*4:(th*4)+3:1] + hights[pa*4:(pa*4)+2:1]
	
	# FLUSH
	if fl > -1: 
		hand_left = filter(lambda c: hand // flushs[fl] % c != 0, cards)
		def reverse_numeric(x, y):
			return hights.index(x) - hights.index(y)
		hand_left.sort( cmp=reverse_numeric )
		return 'Flush', 700-fl, hand_left #hights[fl*4:(fl*4)+4:1]
	
	# STRAIGHT
	st = search( hand, straights, cards ) #looking for a straight
	if st > -1:
		hand_left = filter(lambda c: hand // straights[st] % c != 0, cards)
		#rank_left = ranks[ st:st+5:1 ]
		def reverse_numeric(x, y):
			return hights.index(x) - hights.index(y)

		print hand_left
		hand_left.sort( cmp=reverse_numeric )
		print hand_left

		return 'Straight', 600-st, hand_left
	
	# THREE
	if th > -1: return 'Three of a kind', 500-th, hights[th*4:(th*4)+3:1]
	
	# DOUBLE PAIRS
	pa = search( hand, pairs, cards ) #looking for a pair
	if pa > -1: 
		p2 = search( hand, pairs, cards, out=pa ) #looking for a second pair
		if p2 > -1: return '2 pairs', 400-pa, hights[pa*4:(pa*4)+2:1] + hights[p2*4:(p2*4)+2:1]

	# PAIR
	if pa > -1: return 'pairs', 300-pa, hights[pa*4:(pa*4)+2:1]
	
	# HIGHT
	hi = search( hand, ranks, cards ) #looking for a hight
	hand_left = filter(lambda c: hand // ranks[ hi ] % c != 0, cards)
	return 'hight:', 200-hi, [ hand_left[0] ]











def test( count=1000 ):
	cards = ['As','Ah','Ad','Ac','Ks','Kh','Kd','Kc','Qs','Qh','Qd','Qc','Js','Jh','Jd','Jc','Ts','Th','Td','Tc','9s','9h','9d','9c','8s','8h','8d','8c','7s','7h','7d','7c','6s','6h','6d','6c','5s','5h','5d','5c','4s','4h','4d','4c','3s','3h','3d','3c','2s','2h','2d','2c']
	cards_test = []
	for x in xrange( count ):
		random.shuffle(cards)
		cards_test.append( cards[:7:1] )
	cards_test.append(['5s','4d','7d','8d','3h','3s','3d']);
	print cards_test
	times = time.time()
	for card in cards_test:
		serie, score, hand = resolve_hand( str2card(card) ) 
		print 'in (%s) i found %s (%s)' % (card, serie, card2str(hand))# if score >= 900 else ''
	print ' in %s seconds' % str(time.time() - times)
#test(0)

