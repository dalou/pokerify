

def apply( ca, ro, pl  ):	
	
	ro.getPlayer( 2, { 'name':"Kane", 'stack': 20000, 'fake':True } )
	ro.getPlayer( 3, { 'name':"Undertaker", 'stack': 5000, 'fake':True } )
	ro.getPlayer( 4, { 'name':"Jeriko", 'stack': 5000, 'fake':True } )
	ro.getPlayer( 5, { 'name':"Kofi kingston", 'stack': 2000, 'fake':True } )
	ro.getPlayer( 6, { 'name':"The miz", 'stack': 120000, 'fake':True } )
	ro.getPlayer( 7, { 'name':"Cena", 'stack': 10000, 'fake':True } )
	ro.refresh( )
	
	for p in ro.players.values(): p.command( 'sitdown' )
