CARDS = {
	seat_to_deck : function( cards, seat ) {
		cards.animate({ 
			rotate: (Math.random()*360-180)+"deg", 
			left: -100, 
			top: -100
		}, 750, 'easeOutCirc' );
	},
	deck_to_seat : function( cards, seat ) {
		var card = $( card2img( cards ) )
		seat.find('.cards').append( card )
		var cards = seat.find('.cards .card');
		card.css({ 
			rotate: (Math.random()*360-180)+"deg", 
			position: 'absolute', 
			left: -100, 
			top: -100
		}).animate({ 
			rotate: seat.pos.a-90+"deg", 
			left: seat.pos.ax*150, // + cards.length, 
			top: seat.pos.ay*150// + cards.length 
		}, 750, 'easeOutCirc' );
	}
}
