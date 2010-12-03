window._resume = false;
window.ROOM_STATES = ['New game', 'Serving', 'Preflop', 'Flop', 'Turn', 'River', 'End']
window.PLACE_STATES = ['Empty', 'Up', 'Waiting', 'Ready', 'Fold', 'Call', 'Check', 'Raise', 'All-in']
_room = null;		
window.hights = 	[427,305,183,122,413,295,177,118,371,265,159,106,301,215,129,86,287,205,123,82,259,185,111,74,217,155,93,62,203,145,87,58,161,115,69,46,133,95,57,38,119,85,51,34,91,65,39,26,77,55,33,22,427,305,183,122]
window.cardsstr = 	['As','Ah','Ad','Ac','Ks','Kh','Kd','Kc','Qs','Qh','Qd','Qc','Js','Jh','Jd','Jc','Ts','Th','Td','Tc','9s','9h','9d','9c','8s','8h','8d','8c','7s','7h','7d','7c','6s','6h','6d','6c','5s','5h','5d','5c','4s','4h','4d','4c','3s','3h','3d','3c','2s','2h','2d','2c']
window.SEAT_ANGLES = [90, 45, 0, 0, -45, -90, -135, -180]


jQuery.fx.off = false;



function Room() { this.init(); }
Room.prototype.init = function( self ) {
	self = this;
	
	this.enter = false;
	this.seats = {}
	this.me = null;
	this.table = $('#table');
	this.cards = $('#cards');
	this.deck = $('#deck');
	this.state = $('#room .state');
	this.cx = this.table.width()/2;
	this.cy = 1;
	this.r = 200
	this.oy = 0.7;
	this.places_count = this.table.find('.place').length
	this.table.find('.place').each( function( i ) {
		self.seats[ i+1 ] = new Seat;
		self.seats[ i+1 ].init( self, i+1 );
	});
	var html = ''
	for(var i in window.TOKENS_RANK) {
		html += '<div><img src="/images/token_'+window.TOKENS_COLOR[i]+'.png" />: '+TOKENS_RANK[i]+'</div>'
	}
	this.tokens = $(html).appendTo('#request_raise div')
}
Room.prototype.getseat = function( s ) { return this.seats[s]; }

Room.prototype.com_current = function( data ) {
	$('.current').removeClass('current');
	try{ this.getseat( data[1] ).seat.addClass('current'); } catch(e) {}
}
Room.prototype.com_p_seat = function( data ) {
	var seat = this.getseat( data[1] ) 
	seat.name.html( data[2] );
	seat.seat.removeClass('empty')
	seat.setstack( data[3] );
}
Room.prototype.com_dealer = function( data ) {
	$('.dealer').removeClass('dealer');
	try{ this.getseat( data[1] ).seat.addClass('dealer'); } catch(e) {}
}
Room.prototype.com_turn = function( data ) { this.state.html(window.ROOM_STATES[data[1]-1]); }
Room.prototype.com_state = function( data ) { this.getseat( data[1] ).setstate( data[2] ); }
Room.prototype.com_givecard = function( data, seat, card ) {
	CARDS.deck_to_seat( data[2], this.getseat( data[1] ) ) 
},
Room.prototype.com_burncard = function( data ) {  }
Room.prototype.com_chips = function( data, seat ) { 
	console.log( data[2] )
	seat = this.getseat( data[1] )//.stack( data[2] ); 
	//seat.chips = stack;
	seat.stack.html( CHIPS.html_stack_sorted1( data[2], seat ) )
	seat.name.html( CHIPS.chips_to_amount( data[2] ) )
}
Room.prototype.com_bets = function( data ) { 
}
Room.prototype.com_bet = function( data ) { 
	
	CHIPS.seat_to_bets( data[2], this.getseat( data[1] ) ) 
}
Room.prototype.com_foldcard = function( data ) { this.getseat( data[1] ).foldcard( data[2] ); }
Room.prototype.com_foldcards = function( data ) { this.getseat( data[1] ).foldcards( ); }
Room.prototype.com_showcard = function( data ) { this.cards.append( card2img( data[1] ) ); }
Room.prototype.com_owner = function( data ) {
	$('.me').removeClass('me');
	try {
	this.me = this.getseat( data[1] );
	this.me.seat.addClass('me');

	} catch(e) {}
}
Room.prototype.com_reset = function( data ) {
	this.cards.html('');
	for( var i in this.seats )
		this.seats[i].cards.remove();
		this.seats[i].seat.removeClass('winner')
}
Room.prototype.com_lookup = function( data, w, h, seat ) { self = this;	
	
	seat = this.getseat( data[1] )
	$(document).one('mouseup', function() { 
		console.log(seat.cards)
		seat.cards.each(function(i, w, h ) {

			$(this).stop().animate({ 
				left: seat.arx*seat.card_w,  
				top: seat.ary*seat.card_h,  
				height: 0, 
				marginTop: seat.card_h/2 
			}, 150, function() {
				$(this).html( this.old_html  )
				$(this).stop().animate({ left: 0, height: seat.card_h, marginTop: 0 }, 150);				
			})
		})
	})
	
	seat.cards.each(function(i, w, h ) {
		this.old_html = $(this).html();
		$(this).stop().animate({ 
			left: seat.arx*seat.card_w,  
			top: seat.ary*seat.card_h,
			height: 0, 
			marginTop: h/2 
		}, 150, function() {
			$(this).html( card2img2( data[2][i] ) )
			$(this).stop().animate({ left: 0, height: h, marginTop: 0 }, 150);
			
		})
	})
	
	
	
}


