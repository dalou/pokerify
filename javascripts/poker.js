//$.ie6 = $.browser.msie && parseInt(jQuery.browser.version) <= 6 && !window["XMLHttpRequest"];



$(function() {
	Room.init();	
	$('body').delegate('div.me div.cards', 'mousedown', function() {
		command( '/room/'+window.rid+'/lookup');
		return false;
	})
	
		/*var tokens = [100, 200, 500, 1000, 2000, 5000]
		for( var i in tokens)
			$('body').append( $('<div class="place" style="width: 30px;position: absolute; left: '+( i*30) +'; top: 400px;"></div>').html( CHIPS.balanced_stack( 
				[ [tokens[i], 1], [tokens[i], 2], [tokens[i], 3], [tokens[i], 4], [tokens[i], 5], [tokens[i], 6], [tokens[i], 7], [tokens[i], 8], [tokens[i], 9], [tokens[i], 10] ], 
				25 * (1.6-1) * -0.5, 
				25 * (1.6-1) * 0.5
			)[0] ) )
			
		//i += 1
		html = $('<div style="position: absolute; left: '+( i*60) +'; top: 400px;"></div>')
		
		for( var j in window.hights)
			html.append( $(card2img( window.hights[ j ] )).css({ float: 'left' }) )
			
		$('body').append( html )*/
});
$.fn.rotate = function(a) {
	return this.css({ 
		'-o-transform': 'rotate(' + a + 'deg)',
		'-moz-transform': 'rotate(' + a + 'deg)',
		'-webkit-transform': 'rotate(' + a + 'deg)'
	});
}
$.fn.cardToggle = function( value, w ) {
	//this.each()
	w = this.width();
	this.stop(true).animate({ width: 0, marginLeft: w/2 }, 150, function() {
		$(this).attr('src', '/images/cards/new/'+(value ? value:'xx')+'.png')
		$(this).animate({ width: w, marginLeft: 0 }, 150);
	})
}
$.fn.moveCard = function( x1, y1, a1, x2, y2, a2, effect) {
	this.css({ 
		rotate: a1+"deg", 
		position: 'absolute', left: x1, top: y1 
	}).animate({ rotate: a2+"deg", left: x2, top: y2 }, 750, effect);
}

function card2bg(card) { return '<div name="'+card+'" style="float:left; width:15px; height:29px; background: url(/images/cards/new/'+card+'.png)" ></div>'}
function card2img(card) { return '<img class="card" name="'+card+'" src="/images/cards/png/'+card+'.png" />';}
function card2img2(card) { return '<img name="'+card+'" src="/images/cards/'+card+'" />';}

function card2selector(card) { return 'div[name='+card+']'}
function lookupCard(cards) {
	$(document).one('mouseup', function() { $('#lookup').animate({ bottom:-140 }); })
	html = '';
	for(var i in cards) html += card2img(cards[i])
	$('#lookup').html(html).animate({ bottom:50 })
}
function action(self) {
	$.ajax({ url: $(self).attr('href'), dataType: 'html', success: resume_action });
	//$('#meta').append( $('<div>'+$(self).attr('href')+'</div>').css({ background: 'green', color: 'white', padding: '5px'}) )
}
function command(url) {
	$.ajax({ url: url, dataType: 'json', success: resume_action });
}
function resume() { 
	$.ajax({ 
		url: "/room/"+window.rid+(Room.enter ? '/resume/':'/enter/'), 
		dataType: 'json', 
		success: resume_action
	});
}


function resume_action(data) {

	//try { 

		Room.ping( data )
	/*}
	catch(e) {
		console.log('fail on ' + data[0])
		console.log(e)
	}*/
	jQuery.fx.off = false;
	Room.enter = true

}

window._resume = false;

_room = null;		
window.hights = 	[427,305,183,122,413,295,177,118,371,265,159,106,301,215,129,86,287,205,123,82,259,185,111,74,217,155,93,62,203,145,87,58,161,115,69,46,133,95,57,38,119,85,51,34,91,65,39,26,77,55,33,22,427,305,183,122]
window.cardsstr = 	['As','Ah','Ad','Ac','Ks','Kh','Kd','Kc','Qs','Qh','Qd','Qc','Js','Jh','Jd','Jc','Ts','Th','Td','Tc','9s','9h','9d','9c','8s','8h','8d','8c','7s','7h','7d','7c','6s','6h','6d','6c','5s','5h','5d','5c','4s','4h','4d','4c','3s','3h','3d','3c','2s','2h','2d','2c']



jQuery.fx.off = false;

// 0 : ROOM_SEATS
function c0( data ) { 	
	for( var i in data[1] ) $('<div class="place empty"></div>')
		.seat( data[1][i] )
		.appendTo( Room.table )
		
}

// 1 : PLAYER_CURRENT
function c1( data ) {
	Room.seat( data[1], function( seat, i ) {
		$('#current_button').animate({ 
			left: seat.x * (Room.distance - 20),  
			top: seat.y * (Room.distance - 20),
		});
	});
}

// 2 : PLAYER_DEALER
function c2( data ) {
	Room.seat( data[1], function( seat, i ) {
		$('#dealer_button').animate({ 
			left: seat.x * (Room.distance - 50),  
			top: seat.y * (Room.distance - 50),
		});
	});
	
}

// 3 : PLAYER_STATE
function c3( data ) { 
	Room.seat( data[1], function( seat, i ) {
		seat.state.html( Room.PLAYER_STATES[ data[2] - 1 ] );
	});
}


// 4 : PLAYER_BET
function c4( data ) { 
	Room.seat( data[1], function( seat, i ) {
		stack = CHIPS.balanced_stack( 
			data[2],
			20 * (seat.ex-1) * seat.tx, 
			20 * (seat.ex-1) * seat.ty  
		)
		seat.bets.html( stack[0] ) //[0] )
		for( var i in data[2] ) {
			var jchips = seat.stack.find('.chip_'+data[2][i][0] )
			jchips.slice( jchips.length - data[2][i][1], jchips.length ).remove()
		}
		
	});
	/*for( var i in data[2] ) 
	{
		var jchips = seat.stack.find('.chip_'+data[2][i][0] )
		jchips.slice( jchips.length - data[2][i][1], jchips.length ).appendTo( seat.bets ).animate({ 
			left: seat.x * 100 +  Math.random()*25, 
			top: seat.y * 100 + Math.random()*25  
		}, 750, 'easeOutCirc' )
	}*/
}	
  	
// 5 : ROOM_STATE
function c5( data ) {
	if ( data[1] == 1 ) {
		Room.cards.html('')
		//Room.bets.html('')
	}
	Room.state.html( Room.ROOM_STATES[ data[1] - 1 ] );		
}

function c6( data ) { 
}

// 7 : PLAYER_CARD
function c7( data ) {
	Room.seat( data[1], function( seat, i ) {
		seat.cards.append( CARDS.card( 
			data[2], 
			seat.x * (Room.distance-70), 
			seat.y * (Room.distance-70), 
			0 ).css( '-webkit-transform', '  rotate('+(seat.angle-90)+'deg)  skew('+(-Math.abs(seat.angle-90))+'deg) ' )
			// scaleX('+( 1 - Math.abs(seat.cos) * 0.4)+')
		)
	});
}

// 8 : PLAYER_CARDS
function c8( data ) {
	
}


function c9( data ) {
	

}

// 10 : ROOM_SHOWCARD
function c10( data ) {
	//console.log(data[1])
	Room.cards.append( CARDS.card( data[1], Room.cards.find('.card').length * 35, 10, 0 ).css(
		'-webkit-transform', 'perspective(800) skewY(45deg)'
		
	 ))
}

// 11 : ROOM_BURNCARD
function c11( data ) {
	//Room.burned.append( CARDS.card( 0 ), 0, 100, 95 )
}

// 12 : PLAYER_FOLD
function c12( data ) { 
	
}

// 13 : PLAYER_STACK
function c13( data ) { 
	Room.seat( data[1], function( seat, i ) {
		stack = CHIPS.balanced_stack( 
			data[2], 
			25 * (seat.ex-1) * seat.tx, 
			25 * (seat.ex-1) * seat.ty 
		)
		seat.stack.html( stack[0] ).css({ left: seat.x * 200-stack[1], top: seat.y * 200-stack[2] }) 
	});
}




// 17 : OWNER
function c17( data ) { 
	Room.seat( data[1], function( seat, i, jseat ) {
		$('.me').removeClass('me')
		jseat.addClass('me')
	});
	
}

Room = {
	enter: false,
	rotation : -60,
	angle : 240,
	places : 7,
	ovality : 0.7,
	seats : {},
	distance: 200,
	me: null,
	init : function( ) {

		Room.table = $('#table');
		Room.cards = $('#cards');
		Room.deck = $('#deck');
		Room.burned = $('#burned');
		Room.state = $('#room .state');
		
		var html = ''
		for(var i in window.TOKENS_RANK) {
			html += '<div><img src="/images/chips/'+window.TOKENS_COLOR[i]+'.png" />: '+TOKENS_RANK[i]+'</div>'
		}
		Room.tokens = $(html).appendTo('#request_raise div')
	},	
	
	PLAYER_STATES : ['Empty', 'Up', 'Waiting', 'Ready', 'Fold', 'Call', 'Check', 'Raise', 'All-in'],	
	ROOM_STATES : ['New game', 'Serving', 'Preflop', 'Flop', 'Turn', 'River', 'End'],

	seat : function( i, fn ) { 
		var seat = $('#place'+i);
		if( seat.length ) fn( seat[0], i, seat );
		return seat
	},
	ping : function( data, j ) {
		
		j = 0
		for(var i in data) { 
			//setTimeout( function() { Room.fn[ data[ j ][0] ]( data[ j ] ); }, j );
			window[ 'c'+data[ i ][0] ]( data[ i ] );
			j ++
		}
	} 
}




$.fn.seat = function(  data, self, dom ) {
		
	self = this
	dom = this[0]
	this.css({ width:3, height:3, background: "red" });
	dom.i = data[0];
	dom.cos = data[1]/100;
	dom.sin = data[2]/100;
	
	dom.ex = 1.7; // x coefficient for the ellipse
	dom.ey = 1; // y coefficient for the ellipse	
	dom.x = dom.cos * dom.ex //* 200 
	dom.y = dom.sin * dom.ey //* 200 
	dom.tx = dom.sin * dom.ex
	dom.ty = dom.cos * dom.ey
	
	dom.angle = Math.atan2( dom.y, dom.x )*180 / Math.PI
	self.attr('id', 'place' + dom.i )
	
	
	
	dom.stackamount = $('<div class="stackamount"></div>').css({
		
	}).appendTo( self );
	
	dom.stack = $('<div class="stack"></div>').css({ left: dom.x * 200, top: dom.y * 200  }).appendTo( self )
	.mouseover(function(amount) {
		amount = 0;
		dom.stack.find('img').each(function(i) {
			amount += parseInt(this.title);
		})
		dom.stackamount.html(amount + '$').stop().animate({ opacity: 1})
		return false;
	}).mousemove(function(e) {
		dom.stackamount.css({ 
			left: e.clientX +20-dom.x, 
			top: e.clientY -20-dom.y- document.documentElement.scrollTop
		})
		return false;
	}).mouseout(function() {
		dom.stackamount.stop().animate({ opacity: 0})
		return false;
	})
	
	dom.card_w = 40;
	dom.card_h = 65;
	
	self.css( '-webkit-transform', 'scale('+( 1 + dom.sin  * 0.3)+')' );
	self.css('z-index', 99999 - dom.sin )
	
	dom.cards = $('<div class="cards"></div>').appendTo( self )//self.seat.find('.cards .card');
	dom.name = $('<div class="name"></div>').css({ left: dom.x * 160, top: dom.y * 180 }).appendTo( self );
	dom.state = $('<div class="state"></div>').css({ left: dom.x * 170, top: dom.y * 170  }).appendTo( self );
	//self.timer = $('<div class="timer"></div>').css({ left: self.x * 170, top: self.y * 170  }).appendTo( self );
	dom.timer = $('<div class="mark" style="position: absolute; z-index:9999999; width:5px; height:5px; background:red;"></div>')
		.css({ left: dom.x * Room.distance, top : dom.y * Room.distance }).appendTo( self ).html( dom.i );
	dom.bets = $('<div class="bets"></div>').appendTo( self );
	
	return self;
}

$.fn.rotation = function( a ) {
	return this.css({ rotate : a,
		'-o-transform': 'rotate(' + a + 'deg)',
		'-moz-transform': 'rotate(' + a + 'deg)',
		'-webkit-transform': 'rotate(' + a + 'deg)',
	})
}

function rotation2css(a) {
	return '-o-transform: rotate(' + a + 'deg);\
		-moz-transform: rotate(' + a + 'deg);\
		-webkit-transform: rotate(' + a + 'deg);'
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















