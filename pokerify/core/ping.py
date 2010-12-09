# -*- coding: utf8 -*-

#PING
from pokerify.core import pong

def command_getrooms( ca, ro, pl ):
	results = []
	for room in ca.rooms.values():
		results.append({
			'nb_players' : len(room.getPlayers( )),
			'id' : room.rid,
			'state' : room.state
		})
	return results

def command_addroom( ca, ro, pl  ):
	ca.addRoom()
	return False

def command_stoproom( ca, ro, pl  ):	
	del ca.rooms[ro.rid]
	return False


	

