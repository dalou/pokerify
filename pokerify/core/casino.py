# -*- coding: utf8 -*-

import datetime, sys, os, traceback
from pokerify.core import servers, ping
from urlparse import parse_qs

class Casino( servers.Server ):
	
	rooms = {}
	rooms_index = 1
	
	def ping( self, command, args={} ):
		
		try:
			
			#event = __import__('pokerify.requests.%s' % command, globals(), locals(), [ 'apply' ], -1)
			reload( ping )
			command = 'command_%s' % command
			
			room = self.getRoom( args.get('rid') )
			player = room.getPlayer( args.get('pid'), args ) if room else None
			if room and hasattr( room, command ): 
				event = getattr( room, command )				
				if event( self, player ): player.pong()
			elif  hasattr( ping, command ): 
				event = getattr( ping, command )
				return event( self, room, player )
				
		except Exception as inst:			
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print '\033[32;1m', command, args, '\033[0;91m', ':', '', traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=10, file=sys.stdout), '\033[0;0m'
			return []
	
	def getRoom( self, rid ): 
		if not rid: return None
		return self.rooms.get( int(rid), None )
		
	def addRoom( self ): 
		from pokerify.rules import texasholdem
		reload(texasholdem)
		self.rooms[ self.rooms_index ] = texasholdem.Room( self, self.rooms_index )
		self.rooms_index += 1
		
	def __init__( self, addr ):
		self.addRoom( )
		servers.Server.__init__( self, addr )
		
def get( data, addr ): return servers.send( data, addr )
	
	
