#!/usr/bin/python

from bisect import bisect

def circular_highest(start, move, lst, theo=None):
    slst = sorted(lst)
    find = slst[(bisect(slst, start) - 1 + move) % len(lst)]
    
    print "seat:", start, "+", move, " seats:", lst, " wanted:", theo, " result:", find

   

"""circular_highest([2, 5, 8, 7, 1], 3, 2)
circular_highest([2, 5, 8, 7, 1], 7, 3)
circular_highest([1, 3], 4, 2)
circular_highest([5, 3, 9], 3, 1)
circular_highest([5, 3, 9], 3, 2)"""

circular_highest( 5, +3, [1, 5, 8, 4, 2], 2 )		
circular_highest( 8, +2, [2, 5, 8, 7, 1], 2 )
circular_highest( 2, +2, [2, 5, 8, 7, 1], 7 )
circular_highest( 4, +2, [1, 3], 3 )



def next( start, count, seats, theo ):
		
	
	i = 1
	find = 0
	diff = None	
	search = (start + count) % len( seats )
	leak = 0
	print 'search:', search
	for seat in seats: 
		
		leak = seat- i
		
		i += 1
		
		#if not diff: diff 
	
			

	print "seat:", start, "+", count, " seats:", seats, " wanted:", theo, " result:", find


				


"""

Get a number in an unordered straight that follow a start value from an interval 

Hello,
I search a fast method to perform my problem.

for examples : 

with this array : **[2, 5, 8, 7, 1]** , i started with value **3** and i move **+2** times,
the third next number in the list is 5, the second is **7**, the method must return this value

with the same **[2, 5, 8, 7, 1]** , i started from **7** and i move **+3** times
here the method must return to the minimal value. trought 8.. 1.. 2.., result : **2**

with **[1, 3]**, start **4**, count **+2**, result **3**

with **[5, 3, 9]**, start **3**, count **+1**, result **5**

with **[5, 3, 9]**, start **3**, count **+2**, result **9**

I hope someone will understand my problem.
thanks you
	
		"""

