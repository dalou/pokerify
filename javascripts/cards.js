CARDS = {
	seat_to_deck : function( cards, seat ) {
		cards.animate({ 
			rotate: (Math.random()*360-180)+"deg", 
			left: -100, 
			top: -100
		}, 750, 'easeOutCirc' );
	},
	card: function( card, x, y, a  ) {
		return $( card2img( card ) ).css({ 
			//rotate: (Math.random()*360-180)+"deg", 
			position: 'absolute', 
			left: -100, 
			top: -100
		}).animate({ 
			//rotate: a+"deg", 
			left: x, // + cards.length, 
			top: y// + cards.length 
		}, 750, 'easeOutCirc' );
	},
	cards: function( cards, x, y  ) {
		
	}
}
