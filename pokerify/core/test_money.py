# -*- coding: utf8 -*-

import money
import unittest

MONEYS = [ { 'amount': 5275, 'chips' : { 200: 1, 1000: 3, 400: 5 }, 'min': 200 },
		  { 'amount': 120000, 'chips' : { 200: 18, 500: 18, 5000: 17, 100: 14, 1000: 21 }, 'min': 100 },
		  { 'amount': 6570, 'chips' : { 200: 6, 500: 7, 5000: 0, 100: 8, 1000: 1 }, 'min': 100 },
		  { 'amount': 4200, 'chips' : {200: 6, 500: 5, 5000: 0, 100: 5, 1000: 0}, 'min': 100 }

]

AMOUNTS = [ 4200, 100000, 3000, 2129, 100, 200, 0 ]



class MoneyCase(unittest.TestCase):
	
	
	
	def testMinValue(self):
		for m in MONEYS:	              
			result = money.minValue( m['chips'] )			
			self.assertEqual( result, m['min']  )
	
	def testconvertChipsToAmount(self):                          
		"""Chips amount must be equal to the real amount"""
		for m in MONEYS:	              
			result = money.convertChipsToAmount( m['chips'] )			
			self.assertTrue( abs( m['amount'] - result ) <  m['min'] )
		
	def testconvertAmountToChips(self):                          
		""" Chips amount must be equal or less than min value"""		        
		for m in MONEYS:
			result = money.convertAmountToChips( m['amount'] )				
			self.assertTrue( abs( m['amount'] - money.convertChipsToAmount( result ) ) <  m['min'] )
			
	def testretrieveAmountFromChips(self):  
		for m in MONEYS:
			for a in AMOUNTS:
				result = money.retrieveAmountFromChips( a, dict(m['chips']) )	
				self.assertTrue( abs( a - int(money.convertChipsToAmount( result )) ) <  m['min'] )
		
	
if __name__ == "__main__":
	unittest.main()   