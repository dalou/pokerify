import socket
import threading, time
from urlparse import parse_qs

class Server( ):
	def __init__( self, addr ):
		self.addr = addr
		self.times = []
		try:
			print "Server is running on %s:%s:" % addr
			self.listen()
		except KeyboardInterrupt:
			self.shutdown()
			sys.exit(0)
			print "Keyboard interrupt"
	
	#def get( self, name ): return self.attributes.get(name, [None])[0]
	
	def handle( self, client, addr ):
		while 1:
			
			t0 = time.time()
			
			try:
				message = client.recv(2024)
				if not message: break
			except: break

			params = parse_qs( message )
			args = {}
			for k in params.keys(): args[k] = params[k][0]

			command = args.get('aid')
			if command:			
				
				response = self.ping( command, args )
				if response : client.send( str(response) )
				else: client.send( '[]' )
			else: client.send( '[]' )
			
			self.times.append( time.time() - t0 )
			if len( self.times ) > 10:
				sec = float(sum( self.times )) / len( self.times )
				print command, "average", sec*1000.00 , "msec (", sec, " sec)" 
				self.times = []

		"""message = client.recv(1024)
		self.attributes = parse_qs( message )
		if not message: #arrive si la connexion est coupee
			break
		print 'Server receive : ', message
		if self.get('aid'):
			response = self.receive( self.get('aid') )
			if response: 
				client.send( str(response) )
		client.send('')
		break"""
			
	
	def command( self, command, *args ): pass

	def listen( self ):
		self.socket = socket.socket(   )
		self.socket.bind( self.addr )
		self.socket.listen(5)

		while 1: 
			client, addr = self.socket.accept()
			threading.Thread( target=self.handle, args=(client, addr)).start()
	
def send( command, addr ):
	sock = socket.socket(  )
	sock.connect( addr )
	sock.send( command )
	data = sock.recv(2024)
	sock.close()
	return data
	
	
