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
		print("Bidder" + str(b.bidderName) + ", true value is :" + str(b.intrinsicValue) + ", bid is " + str(b.bidValue))

	if methodOfBid == 'VCG':
		auction.executeVCG()
	else:
		auction.executeGSP()
	print(" ")
	print("valueVac = " + str(auction.valueVec))
	print("bidVec = " + str(auction.bidVec))
	print("allocation = " + str(auction.allocation))
	print("The bidders should pay = " + str(auction.priceBids))
	print("revenue = " + str(auction.revenue))
	print("SocialWelfare = " + str(auction.SocialWelfare))
	print("clickThroughRate = " + str(auction.slots.clickRate))

if __name__ == '__main__':
	numbid = int(sys.argv[1])
	numitem = int(sys.argv[2])
	methodOfBid = sys.argv[3]
	runAndPrint(numbid, numitem, methodOfBid)