
CHIPS = {
	COLORS: {
		5000 : 'black', 1000 : 'red', 500 : 'yellow', 
		200 : 'blue',  100 : 'white'
	},
	seat_to_bets: function( cards, seat ) {
		for( var value in cards) {
			seat.stack.find('.chip_'+v).slice( -cards[ value ] )/*.animate({ 
				left: s.arx*-Math.random()*50+150, top: s.ary*-Math.random()*50+150
			}, 750, 'easeOutCirc' )*/.appendTo( seat.bets );
		}
	},
	chips_to_amount: function( c ) { var a = 0; for(var v in c) a += v * c[ v ]; return a; },
	html_stack_sorted1: function( c, s ) {
		
		var vs = []; 
		for( v in c ) vs.push( v );
		vs.sort( function(a, b){ return (a-b); } )
		var i = 0
		var r = '';
		var dm = 0;
		var dx = s.arx;
		var dy = s.ary;
		if (dy < 0.3) dy = 0.3
		for(var v in vs) 
		{
			var h=0
			var d=0
			var count = c[ vs[v] ]
			var m= Math.ceil( (count/2)+ (Math.random()*4) )
			for(var j=1; j<= count; j++) { 
				if(  count > 12 && j % m == 0  ) { h=0; d+= 1; dm+= d; }
				var left = i*dy*20 + d*dx*20
				var top = -i*dx*20 + d*dy*20
				r += '<img style="z-index:'+( parseInt(top) + 9999)+'; left:'+left+'px; top: '+top+'px; margin-top:'+(-2*h + d)+'px;" \
					class="chip chip_'+vs[v]+'" src="/images/chips/'+CHIPS.COLORS[ vs[v] ]+'.png" />'
				h++;
			}
			i++;
		}
		return r
	}
}

