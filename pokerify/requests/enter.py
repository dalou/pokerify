from pokerify.rules import texasholdem

def apply( ca, ro, pl ): #ru, ro, pl, re ):
	
	pl.resetEvents()
	pl.emit( 'reset' )
	pl.emit( 'state', ro.state )
	pl.emit( 'current', ro.current )
	pl.emit( 'dealer', ro.dealer )
	for p in ro.getPlayers( state=texasholdem.INGAME ): pl.resume()
	pl.emit( 'setme', pl )
	for card in ro.cards[-1]: pl.emit( 'showcard', card )
	
	return pl.getEvents()
