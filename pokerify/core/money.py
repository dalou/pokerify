# -*- coding: utf8 -*-


class Chips( ):
	def __init__( self, amount, values=[ 100, 200, 500, 1000, 5000 ] ):
			
		self.amount = 0	
		self.minvalue = None
		self.values = values
		self.counts = []
		for value in self.values: 
			self.counts.append( 0 )
			if not self.minvalue: self.minvalue = value
			if value < self.minvalue: self.minvalue = value
		self.amountToChips( amount )
		
	def __repr__( self ):
		result = {}
		i = 0
		for value in self.values:
			result[ value ] = self.counts[ i ]
			i+=1
		return result.__repr__()
			
	def amountToChips( self, amount ):
		
		amount = int( amount )
		itoken=0
		self.chips = {}
		value = self.values[ itoken ]
		count = 0 
		equilibrium = len( self.values )
		while amount > 0:
			if amount < self.minvalue: return 
			if amount >= value and count < itoken + equilibrium:
				count += 1
				self.counts[ itoken ] += 1
				amount -= value
				self.amount += value
			else: 
				itoken += 1
				if itoken > len( self.values )-1: 
					itoken = 0
					equilibrium -= 1
					if equilibrium < itoken: equilibrium = 1
				value = self.values[ itoken ]
				count = 0
			
	def addChips( self, chips ):
		i = 0
		for count in chips.counts(): 
			self.counts[ i ] += count
			i+=1
		self.amount += chips.amount
		
	def addAmount( self, amount ):
		self.insertChips( Chips( amount, self.values ) )
		
		
	def popAmount( self, amount ):
		chips = Chips( amount, self.values )
		stack = Chips( self.amount - chips.amount, self.values )
		self.amount = stack.amount
		self.counts = stack.counts
		return chips
	
	def popChips( self, chips ):
		return popAmount( self, chips.amount )
		

def popChipsToChips( chips, tochips ):
	for value, count in chips.items(): tochips[ value ] -= count
	return chips



def popAmountToChips( amount, chips ):
	
	tokens = chips.keys()
	tokens.sort()
	stack = convertChipsToAmount( chips )
	chipsneeded = convertAmountToChips( amount, tokens )	
	stack -= convertChipsToAmount( chipsneeded )
	newchips = convertAmountToChips( stack, tokens )
	for v in newchips: chips[ v ] = newchips[ v ]
	return chipsneeded


	
