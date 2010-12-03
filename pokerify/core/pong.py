# -*- coding: utf8 -*-

SIGNALS = []

def bets( target, seat ):
	for bet in seat.getBets(): return bet( target, seat, bet )
def cards( target, seat ):
	for card in seat.getCards(): return card( target, seat, card )
def bet( target, seat, bet ): return target.emit( 'bet', seat, bet )
def card( target, seat, card ): return target.emit( 'card', seat, card )
def chips( target, seat ): return target.emit( 'chips', seat, seat.chips )

#cards
def givecard( target, card=None ): return target.emit( 'givecard', card )
def showcard( target, card=None ): return target.emit( 'showcard', card )
def burncard( target, card=None ): return target.emit( 'burncard', card )
def foldcard( target, seat, card ): return target.emit( 'foldcard', seat, card )
def foldcards( target, seat ): return target.emit( 'foldcards', seat )

#states
def onwer( target, onwer ): return target.emit( 'onwer', onwer )
def dealer( target, dealer ): return target.emit( 'dealer', dealer )
def current( target, current ): return target.emit( 'current', current )
def reset( target ): return target.emit( 'reset' )
def turn( target, state ): return target.emit( 'turn', state )
def state( target, seat, state ): return target.emit( 'state', seat, state )
#def player( target, seat ): return target.emit( 'player', seat )

