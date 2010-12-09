
CHIPS = {
	COLORS: {
		5000 : 'black', 1000 : 'red', 500 : 'yellow', 
		200 : 'blue',  100 : 'white'
	},
	chipsToPot: function( chips, seat ) {
		for( var value in chips ) 
		{
			var chips = from.find('.chip_'+value )
			chips.slice( chips.length - chips[ value ], chips.length ).appendTo( to ).animate({ 
				left: seat.pos.ax * 100 +  Math.random()*25, 
				top: seat.pos.ay * 100 + Math.random()*25  
			}, 750, 'easeOutCirc' )
		}
	},
	
	chipsToBets: function( chips, seat ) {
		for( var value in chips ) 
		{
			var jchips = seat.stack.find('.chip_'+value )
			jchips.slice( jchips.length - chips[ value ], jchips.length ).appendTo( seat.bets ).animate({ 
				left: seat.pos.ax * 100 +  Math.random()*25, 
				top: seat.pos.ay * 100 + Math.random()*25  
			}, 750, 'easeOutCirc' )
		}
	},
	chipsToamount: function( c ) { var a = 0; for(var v in c) a += v * c[ v ]; return a; },
	
	html_stack_dirty: function( chips, pos) {
		var r = '';
		var i = 0;
		for( v in chips ) {
			
			for(var j=0; j< chips[v]; j++) {
		
				var left = pos.dx * pos.ax + ( Math.random()*(40+chips[v]) - (20+chips[v]) )				
				var top = pos.dy * pos.ay + ( Math.random()*(40+chips[v]) - (20+chips[v]) - i ) 		
				r += '<img title="'+v+'" style="z-index:'+( Math.random()*chips[v] + i )+'; left:'+left+'px; top: '+top+'px;" \
					class="chip chip_'+v+'" src="/images/chips/'+CHIPS.COLORS[ v ]+'.png" />'
			}
			i++;
		}
		return r
	},
	html_stack_sorted1: function( chips, pos ) {
		
		var vs = []; 
		for( v in chips ) vs.push( v );
		vs.sort( function(a, b){ return (a-b); } )
		var i = 0
		var r = '';
		var dm = 0;
		
		for(var v in vs) 
		{
			var h=0
			var d=0
			var count = chips[ vs[v] ]
			var m= Math.ceil( (count/2)+ (Math.random()*4) )
			for(var j=1; j<= count; j++) { 
				//if(  count > 12 && j % m == 0  ) { h=0; d+= 1; dm+= d; }	
				var left = i * pos.ay + d * pos.ax + pos.dx * pos.ax				
				var top = -i * pos.ax + d * pos.ay + pos.dy * pos.ay				
				r += '<img title="'+vs[v]+'" style="z-index:'+( parseInt(top) + 9999)+'; left:'+left+'px; top: '+top+'px; margin-top:'+(-2*h + d)+'px;" \
					class="chip chip_'+vs[v]+'" src="/images/chips/'+CHIPS.COLORS[ vs[v] ]+'.png" />'
				h++;
			}
			i++;
		}
		return r
	}
}

