
CHIPS = {
	COLORS: {
		5000 : 'black', 2000 : 'green', 1000 : 'red', 500 : 'yellow', 
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
	html_stack_sorted1: function( chips, px, py, dx, dy ) {
		if( !dy ) dy = dx;
		/*var i = 0
		var r = '';
		var dm = 0;
		var w=0
		var h=0*/
		
		var w = 0
		var h = 0
		var r = '';
		var x = 0;
		var y = 0;
		var z = 0;
		
		var pos = []
		
		for(var i in chips) 
		{
			var v = chips[i][0]
			var c = chips[i][1]
			for(var j=1; j<= c+1; j++) { 
				
				pos.push([v, c, x*px + dx*px, -y*py + dy*py, z])
				
				var left = y + dx*px
				var top = x + dy*py
				
				r += '<img title="'+v+'" style="z-index:'+( parseInt(top) + 9999)+'; left:'+left+'px; top: '+top+'px; margin-top:'+(-z)+'px;" \
					class="chip chip_'+v+'" src="/images/chips/'+CHIPS.COLORS[ v ]+'.png" />'
				
				z += 2
				if( j == c/2 ) {
					x += 20
					w += 20
					z = 0
				}				
			}
			if(i % 3 == 0) { 
				x = 0; 
				z = 0;
				y += 20;
				h += 20
			}
			z = 0
			x += 20
			w += 20
		}
		return [r, w, h]
	},
	
balanced_stack : 
	// elliptic table
function( chips, step_x, step_y ) 
{
	var html = ''	
	var left = 0
	var top = 0
	for(var i in chips) 
	{
		var step = ( chips[i][1]- 1 ) * 3.5 + 18 
		html += '<div 	style=" background: url(/images/chips/'+CHIPS.COLORS[ chips[i][0] ]+'.png) left top no-repeat; \
								z-index:'+( parseInt(top) + 9999)+'; \
								left:'+left+'px; top: '+(top - step)+'px;" \
						class="chip chip_'+ chips[i][0] +'"><div style="padding-top: '+ (step ) +'px; background: url(/images/chips/bottom.png) left bottom no-repeat;"></div></div>'
		left += step_x
		top += -step_y
	}
	return [ html, left/2, top/2 ]
}
}


	
