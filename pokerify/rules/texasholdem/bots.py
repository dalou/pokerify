import random

def play( room, casino, p ):
	i = int(random.random()*100)
	#if i >= 95: p.ping( 'allin' )
	#elif i >= 65: p.ping( 'raiseby', { 'amount': 1000 })
	if i >= 90: p.ping( 'fold' )
	elif i >= 50: p.ping( 'call' )
	else: p.ping( 'check' )
	#else : p.ping( 'fold' )