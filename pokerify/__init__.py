#!/usr/bin/python
import sys, os

ROOT = os.path.dirname( os.path.abspath(__file__) )
sys.path.append('%s/..' % ROOT)
sys.path.append( ROOT )

HOST, PORT = "localhost", 5003

from pokerify.core import casino, rooms

def get( cmd ): return casino.get( cmd, (HOST, PORT) )

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)

if __name__ == "__main__": casino.Casino( (HOST, PORT) ) 
				
			
			
	
		

