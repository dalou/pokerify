import os, signal
	

def apply( self ):
	os.remove( self.server.ridfile )
	os.kill(os.getpid(), signal.SIGTERM)
