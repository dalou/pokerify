# -*- coding: utf8 -*-

import money
import unittest

class MoneyCase(unittest.TestCase):
	
	amounts = [ 5200, 120000, 4500, 6000, 3450, 6570 ]
	chips = [ { 1000: 3, 400: 5, 200: 1 },
			  { 200: 18, 500: 18, 5000: 17, 100: 14, 1000: 21 } ]
	
	def testChips2Amount(self):                          
		"""toRoman should give known result with known input"""	
		i = 0
		for chip in self.chips:	              
			result = money.chips2amount( chip )               
			self.assertEqual( self.amounts[ i ], result ) 
			i += 1
		
	def testAmount2Chips(self):                          
		"""toRoman should give known result with known input"""	
	        
		for amount in self.amounts:	 
			result = money.amount2Chips( amount )	
			self.assertEqual( amount, money.chips2amount( result ) ) 
	
if __name__ == "__main__":
	unittest.main()   