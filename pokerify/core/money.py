# -*- coding: utf8 -*-

def chips2amount( chips ):
	total = 0
	for value, count in chips.items(): total += count *  value
	return total

def amount2Chips( amount, tokens=[ 100, 200, 500, 1000, 5000 ], chips=None ):
	amount = int( amount )
	itoken=0
	chips = {}
	for value in tokens: chips[ value ] = 0
	value = tokens[ itoken ]
	count = 0 
	equilibrium = len( chips )
	while amount > 0:
		if amount < tokens[ 0 ]: return chips
		if amount >= value and count < itoken + equilibrium:
			count += 1
			chips[ value ] += 1
			amount -= value
		else: 
			itoken += 1
			if itoken > len( tokens )-1: 
				itoken = 0
				equilibrium -= 1
				if equilibrium < itoken: equilibrium = 1
			value = tokens[ itoken ]
			count = 0
	return chips

def amount2ChipsFromChips( amount, chips ):
	amount = int( amount )
	itoken=0
	chips = {}
	for value in tokens: chips[ value ] = 0
	value = tokens[ itoken ]
	count = 0 
	equilibrium = len( chips )
	while stack > 0:
		if stack < tokens[ 0 ]: return chips
		if stack >= value and count < itoken + equilibrium:
			count += 1
			chips[ value ] += 1
			stack -= value
		else: 
			itoken += 1
			if itoken > len( tokens )-1: 
				itoken = 0
				equilibrium -= 1
				if equilibrium < itoken: equilibrium = 1
			value = tokens[ itoken ]
			count = 0
	return chips
