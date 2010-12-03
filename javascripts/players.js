function Seat() { }
Seat.prototype.init = function( room, i ) {
	
	this.i = i;
	this.room = room;
	this.seat = $('#place'+i);
	
	this.card_w = 40;
	this.card_h = 65;
	
	this.a = (i-1) * (180 / (this.room.places_count-1))
	this.ar = (this.a / 180) * Math.PI
	
	this.arx = -Math.cos(this.ar);
	this.ary = Math.sin(this.ar);
	this.x = this.arx * this.room.r + this.room.cx;
	this.y = this.ary * this.room.r + this.room.cy;
	this.dcx = -this.x + this.room.cx;
	this.dcy = -this.y + this.room.cy;
	
	this.seat.css({ left: this.x, top: this.y*this.room.oy });
	this.cards = this.seat.find('.cards .card');
	this.name = this.seat.find('.name').css({ left: this.arx*60, top: this.ary*80 });
	this.state = this.seat.find('.state').css({ left: this.arx*60, top: this.ary*80 + 20 });
	this.stack = this.seat.find('.stack').css({ width: 5, height: 5, background: 'green',/*'-webkit-transform': "rotate("+(-this.a-90)+"deg)",*/ left: this.arx*100, top: this.ary*100 });
	this.bets = this.seat.find('.bets').css({ left: this.arx, top: this.ary });
}
Seat.prototype.setstate = function( state ) {
	this.seat.removeClass('fold call raise allin check').addClass( window.PLACE_STATES[state-1] )
}
Seat.prototype.setcard = function( card ) {
		
}

// Test : _room.getseat( 1 ).betchips( { 500: 3, 200 : 4, 100 : 6 } ) 
Seat.prototype.betchips = function( chips ) {
	CHIPS.move_to_bets( chips, this )
}
Seat.prototype.foldcards = function( cards ) {
	CARDS.move_to_deck( this.cards )
}
function rotation2css(a) {
	return '-o-transform: rotate(' + a + 'deg);\
		-moz-transform: rotate(' + a + 'deg);\
		-webkit-transform: rotate(' + a + 'deg);'
}
Seat.prototype.setstack = function( stack ) {
	this.chips = stack;
	this.stack.html( CHIPS.html_stack_sorted1( stack, this ) )
	this.name.html( CHIPS.amount( stack ) )
}
