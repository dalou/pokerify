CARDS = {
	seat_to_deck : function( cards, seat ) {
		cards.animate({ 
			rotate: (Math.random()*360-180)+"deg", left: seat.dcx, top: seat.dcy
		}, 750, 'easeOutCirc' );
	},
	deck_to_seat : function( cards, seat ) {
		var card = $( card2img( data[2] ) )
		seat.seat.find('.cards').append( card )
		seat.cards = seat.seat.find('.cards .card');
		card.css({ 
			rotate: (Math.random()*360-180)+"deg", 
			position: 'absolute', left: seat.dcx, top: seat.dcy
		}).animate({ 
			rotate: -seat.a-90+"deg", left: seat.arx*20*seat.cards.length, top: seat.ary*20*seat.cards.length 
		}, 750, 'easeOutCirc' );
	}
}
