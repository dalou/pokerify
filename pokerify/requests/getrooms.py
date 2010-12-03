""" Le biceps : 

bruler sa propre carte, mais avoir un bonus

lvl1: 100% ;
lvl2: 100% + choisir sa carte;
lvl3: 120%..."""


def apply( ca, ro, pl ):
	results = []
	for room in ca.rooms.values():
		results.append({
			'nb_players' : len(room.getPlayers( )),
			'id' : room.rid,
			'state' : room.state
		})
	return results

