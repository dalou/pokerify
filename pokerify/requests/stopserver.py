import os, signal
	

def apply( ru, ro, pl, re ):
	os.remove( ro.ridfile )
	os.kill(os.getpid(), signal.SIGKILL)
	sys.exit()

	
