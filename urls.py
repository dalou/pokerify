from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from poker.player.models import Player
from poker.room.models import Room
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import simplejson
import os, imp, httplib, glob
import pokerify

urlpatterns = patterns('',

    url(r'favicon\.ico$', direct_to_template, {'template':'img/icons/favicon.ico', 'mimetype':'image/x-icon'}),
    url(r'robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}), 
    url(r'(?P<path>.+\.js)$', 'django.views.static.serve', {'document_root': settings.PROJECT_PATH}),
    url(r'(?P<path>.+\.(swf|png|gif|jpg))$', 'django.views.static.serve', {'document_root': settings.PROJECT_PATH}), 
    url(r'(?P<path>.+\.css)$', 'django.views.static.serve', {'document_root': settings.PROJECT_PATH}),    
    
    url(r'^room/(?P<aid>[a-z]+)?/?$', settings.PROJECT_NAME+'.urls.room'),
    url(r'^room/(?P<rid>[0-9]+)/(?P<aid>[a-z]+)?/?$', settings.PROJECT_NAME+'.urls.room'),
    url(r'^room/?$', settings.PROJECT_NAME+'.urls.room'), 
     

    url(r'^$', settings.PROJECT_NAME+'.urls.rooms'),
)

def room( request, rid=None, aid=None ):

	request.session['name'] = "Dalou"
	request.session['stack'] = "31550"		
	request.session['jokers'] = { 'biceps': [], 'goujat': [], 'more': ['c'] }

	if aid == 'add':
		pokerify.get( 'aid=addroom' )
		return HttpResponseRedirect('/room/')
	
	if aid == 'stop' and rid:
		pokerify.get( 'aid=stoproom&rid=%s' % rid )
		return HttpResponseRedirect('/room/')
		
	if rid:

		params = request.GET.copy()
	
		params['aid'] = aid
		params['rid'] = rid
		params['pid'] = request.session.session_key
		params['name'] = request.session['name']
		params['stack'] = request.session['stack']
		params['jokers'] = request.session['jokers']
		data = pokerify.get( params.urlencode() )

		if request.is_ajax():
			return HttpResponse( data, mimetype='application/json')
		else:
			n_p = xrange(7)
			jokers = getJokers( request )

	rooms = eval( pokerify.get( 'aid=getrooms' ) ) 
	return render_to_response('rooms.html', locals())
    

def getJokers( request ):
	jokers = []

	for joker in request.session['jokers']:
		if os.path.isfile( '/var/www/sites/poker/casino/jokers/%s.py' % joker ):
			
			#j = imp.load_source('', '/var/www/sites/poker/casino/jokers/%s.py' % joker)
			jokers.append( { 'name': joker, 'title': '' } )
	
	return jokers
	
			
	
    
