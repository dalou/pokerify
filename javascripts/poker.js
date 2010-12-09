//$.ie6 = $.browser.msie && parseInt(jQuery.browser.version) <= 6 && !window["XMLHttpRequest"];



























$(function() {
	Room.init();
	$('body').delegate('div.me div.cards', 'mousedown', function() {
		command( '/room/'+window.rid+'/lookup');
		return false;
	})
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
		$(this).attr('src', '/images/cards/'+(value ? value:'xx')+'.gif')
		$(this).animate({ width: w, marginLeft: 0 }, 150);
	})
}
$.fn.moveCard = function( x1, y1, a1, x2, y2, a2, effect) {
	this.css({ 
		rotate: a1+"deg", 
		position: 'absolute', left: x1, top: y1 
	}).animate({ rotate: a2+"deg", left: x2, top: y2 }, 750, effect);
}

function card2bg(card) { return '<div name="'+card+'" style="float:left; width:15px; height:29px; background: url(/images/cards/'+card+'.gif)" ></div>'}
function card2img(card) { return '<div class="card"><img name="'+(card ? card:'xx')+'" src="/images/cards/'+(card ? card+'.gif':'xx.png')+'" /></div>';}
function card2img2(card) { return '<img name="'+(card ? card:'xx')+'" src="/images/cards/'+(card ? card+'.gif':'xx.png')+'" />';}

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
function resume() { $.ajax({ url: "/room/"+window.rid+(Room.enter ? '/resume/':'/enter/'), dataType: 'json', success: resume_action })}
function resume_action(data) {

	if( data.length ) console.log( data )
	Room.ping( data )
	jQuery.fx.off = false;
	Room.enter = true
}
















