window._resume = false;
window.ROOM_STATES = ['New game', 'Serving', 'Preflop', 'Flop', 'Turn', 'River', 'End']
window.PLACE_STATES = ['Empty', 'Up', 'Waiting', 'Ready', 'Fold', 'Call', 'Check', 'Raise', 'All-in']
_room = null;		
window.hights = 	[427,305,183,122,413,295,177,118,371,265,159,106,301,215,129,86,287,205,123,82,259,185,111,74,217,155,93,62,203,145,87,58,161,115,69,46,133,95,57,38,119,85,51,34,91,65,39,26,77,55,33,22,427,305,183,122]
window.cardsstr = 	['As','Ah','Ad','Ac','Ks','Kh','Kd','Kc','Qs','Qh','Qd','Qc','Js','Jh','Jd','Jc','Ts','Th','Td','Tc','9s','9h','9d','9c','8s','8h','8d','8c','7s','7h','7d','7c','6s','6h','6d','6c','5s','5h','5d','5c','4s','4h','4d','4c','3s','3h','3d','3c','2s','2h','2d','2c']
window.SEAT_ANGLES = [90, 45, 0, 0, -45, -90, -135, -180]


jQuery.fx.off = false;

Room = {
	enter: false,
	rotation : -60,
	angle : 240,
	places : 7,
	ovality : 0.7,
	seats : {},
	me: null,
	init : function( ) {

		Room.table = $('#table');
		Room.cards = $('#cards');
		Room.deck = $('#deck');
		Room.state = $('#room .state');	
		
		console.log( Room.places )
		
		for(var i=1; i<= Room.places; i++) Room.seats[ i ] =  $('<div class="place empty">'+i+'</div>').seat( i ).appendTo( Room.table );

		var html = ''
		for(var i in window.TOKENS_RANK) {
			html += '<div><img src="/images/chips/'+window.TOKENS_COLOR[i]+'.png" />: '+TOKENS_RANK[i]+'</div>'
		}
		Room.tokens = $(html).appendTo('#request_raise div')
	},
	
	state : function( data ) { Room.state.html( window.ROOM_STATES[data-1] ); },
	players : function( data ) 
	{ 		
		for( var i in data ) 
		{
			
			for( var j in data[ i ] ) Room.players_fn[ j ]( Room.seats[ i ], data[ i ][ j ] );
		}
	},
	
	players_fn : {
		state : function( seat, data ) { seat.state.html( window.ROOM_STATES[data-1] ); },
	},
	
	chips : function( data, seat ) { 

		seat = this.getseat( data[1] )//.stack( data[2] ); 
		//seat.chips = stack;
		seat.stack.html( CHIPS.html_stack_dirty( data[2], seat.pos ) )
		
		//seat.name.html( CHIPS.chips_to_amount( data[2] ) )
	},
	getseat : function( seat ) { return Room.seats[ seat ]; },
	
	current : function( data ) {
		$('.current').removeClass('current');
		try {
			if( data[1] != 0 )
				Room.getseat( data ).addClass('current').timer.html('<img src="/images/timer.gif"/>') 
		} catch(e) {}
	},
		
	ping : function( data ) {
		
		for(var i in data) {
			Room[ i ]( data[ i ] );
		}
	} 
}




$.fn.seat = function(  i, self ) {
		
	self = this;
	self.i = i;
	self.attr('id', 'place'+i )
	
	self.stackamount = $('<div class="stackamount"></div>').css({
		
	}).appendTo( self );
	
	self.stack = $('<div class="stack"></div>').appendTo( self )
	.mouseover(function(amount) {
		amount = 0;
		self.stack.find('img').each(function(i) {
			amount += parseInt(this.title);
		})
		self.stackamount.html(amount + '$').stop().animate({ opacity: 1})
		return false;
	}).mousemove(function(e) {
		self.stackamount.css({ 
			left: e.clientX +20-self.pos.dx, 
			top: e.clientY -20-self.pos.dy- document.documentElement.scrollTop
		})
		return false;
	}).mouseout(function() {
		self.stackamount.stop().animate({ opacity: 0})
		return false;
	})
	
	self.card_w = 40;
	self.card_h = 65;
	
	var a = Room.rotation + ( i-1 ) * ( Room.angle / ( Room.places ) ) 
	var ar = a * Math.PI/180
	
	self.pos = { 
		ax: Math.cos( ar ), ay: Math.sin( ar ),// * self.room.ovality, 				
		a: a, radian: ar, dx: 200, dy: 200 
	}
	
	self.cards = $('<div class="cards"></div>').appendTo( self )//self.seat.find('.cards .card');
	self.name = $('<div class="name"></div>').css({ left: self.pos.ax * 160, top: self.pos.ay * 180 }).appendTo( self );
	self.state = $('<div class="state"></div>').css({ left: self.pos.ax * 170, top: self.pos.ay * 170 }).appendTo( self );
	self.timer = $('<div class="timer"></div>').css({ left: self.pos.ax * 170, top: self.pos.ay * 170 - 100 }).appendTo( self );
	self.bets = $('<div class="bets"></div>').appendTo( self );
	
	return self;
}

function rotation2css(a) {
	return '-o-transform: rotate(' + a + 'deg);\
		-moz-transform: rotate(' + a + 'deg);\
		-webkit-transform: rotate(' + a + 'deg);'
}


com_dealer = function( data ) {
	$('.dealer').removeClass('dealer');
	try{ this.getseat( data[1] ).seat.addClass('dealer'); } catch(e) {}
}
com_turn = function( data ) { this.state.html(window.ROOM_STATES[data[1]-1]); }
com_state = function( data, seat ) { 
	//this.getseat( data[1] ).setstate( data[2] ); 
	seat = this.getseat( data[1] )
	seat.state.html( window.PLACE_STATES[ data[2]-1 ] )
	seat.removeClass('fold call raise allin check').addClass( window.PLACE_STATES[data[2]-1] )
}
com_givecard = function( data, seat, card ) {
	CARDS.deck_to_seat( data[2], this.getseat( data[1] ) ) 
},
com_burncard = function( data ) {  }
com_chips = function( data, seat ) { 

	seat = this.getseat( data[1] )//.stack( data[2] ); 
	//seat.chips = stack;
	seat.stack.html( CHIPS.html_stack_dirty( data[2], seat.pos ) )
	
	//seat.name.html( CHIPS.chips_to_amount( data[2] ) )
}
com_bets = function( data ) { 
	seat = this.getseat( data[1] )//.stack( data[2] ); 
	//seat.chips = stack;
	for(var i in data[2]) {
		CHIPS.seat_to_bets( data[2][i], seat ) 
	}
}
com_bet = function( data ) { 

	CHIPS.seat_to_bets( data[2], this.getseat( data[1] ) ) 
}
com_foldcard = function( data ) { 
	this.getseat( data[1] ).foldcard( data[2] ); 
}
com_foldcards = function( data, seat ) { 
	
	seat = this.getseat( data[1] )
	CARDS.seat_to_deck( seat.cards, seat )

	
}
com_showcard = function( data ) { this.cards.append( card2img( data[1] ) ); }
com_owner = function( data ) {
	$('.me').removeClass('me');
	try {
	this.me = this.getseat( data[1] );
	this.me.addClass('me');

	} catch(e) {}
}
com_reset = function( data ) {
	this.cards.html('');
	for( var i in this.seats )
		this.seats[i].cards.empty();
		this.seats[i].bets.empty();
		this.seats[i].removeClass('winner')
}
com_lookup = function( data, w, h, seat ) { self = this;	
	
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


