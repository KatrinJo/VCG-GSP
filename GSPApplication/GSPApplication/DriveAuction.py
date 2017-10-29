import sys
import numpy as np
import string
from Bidder import Bidder
from Auction import Auction
from Slots import Slots


def runAndPrint(numbid, numitem, methodOfBid):
	#str =  "The number of Bidders is " + str(numbid) + ", and the number of Items is " + str(numitem)
	print("The number of Bidders is " + str(numbid) + ", and the number of Items is " + str(numitem))

	auction = Auction(numbid, numitem, methodOfBid)
	print("The bidderName and their true value:")
	for b in auction.bidders:
		print(str(b.bidderName) + "," + str(b.value))

	if methodOfBid == 'VCG':
		auction.executeVCG()
	else:
		auction.executeGSP()
	print(" ")
	print(auction.allocation)
	print(auction.finalBids)
	print(auction.priceBids)

if __name__ == '__main__':
	numbid = int(sys.argv[1])
	numitem = int(sys.argv[2])
	methodOfBid = sys.argv[3]
	runAndPrint(numbid, numitem, methodOfBid)