import sys
import numpy as np
import string
import os
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from scipy.stats import gaussian_kde
import math

from Bidder import Bidder
from Auction import Auction
from Slots import Slots





def runAndPrint(numbid, numitem, truthOrRandom):
	#str =  "The number of Bidders is " + str(numbid) + ", and the number of Items is " + str(numitem)
	
	auction = Auction(numbid, numitem, truthOrRandom)
	#print("The bidderName and their true value:")
	#for b in auction.bidders:
	#	print("Bidder" + str(b.bidderName) + ", true value is :" + str(b.intrinsicValue) + ", bid is " + str(b.bidValue))
	
	#print("  ")
	auction.executeVCG()
	SWVCG = auction.SocialWelfare
	RVCG = auction.revenue
	#print("Now it is VCG result: ")
	#print("valueVac = " + str(auction.valueVec))
	#print("bidVec = " + str(auction.bidVec))
	#print("allocation = " + str(auction.allocation))
	#print("The bidders should pay = " + str(auction.priceBids))
	#print("revenue = " + str(auction.revenue))
	#print("SocialWelfare = " + str(auction.SocialWelfare))
	#print("clickThroughRate = " + str(auction.slots.clickRate))
	
	#print("  ")
	auction.executeGSP()
	SWGSP = auction.SocialWelfare
	RGSP = auction.revenue
	#print("Now it is GSP result: ")
	#print("valueVac = " + str(auction.valueVec))
	#print("bidVec = " + str(auction.bidVec))
	#print("allocation = " + str(auction.allocation))
	#print("The bidders should pay = " + str(auction.priceBids))
	#print("revenue = " + str(auction.revenue))
	#print("SocialWelfare = " + str(auction.SocialWelfare))
	#print("clickThroughRate = " + str(auction.slots.clickRate))
	#print("  ")
	return [SWVCG, RVCG, SWGSP, RGSP]

if __name__ == '__main__':
	# numbid = int(sys.argv[1])
	# numitem = int(sys.argv[2])
	# method = ['VCG','GSP']
	truthOrRand = ['random', 'truth']
	# methodOfBid = sys.argv[3]
	# truthOrRandom = sys.argv[4]
	SWVCG = []
	SWGSP = []
	RVCG = []
	RGSP = []
	for num in list(range(1,21)):
		for i in range(2):
			print("The number of Bidders is " + str(num) + ", and the number of Items is " + str(num) + ", " + truthOrRand[i])
			[swVCG, rVCG, swGSP, rGSP] = runAndPrint(num, num, truthOrRand[i])
			np.append(SWVCG, swVCG)
			np.append(RVCG, rVCG)
			np.append(SWGSP, swGSP)
			np.append(RGSP, rGSP)
			print("SWVCG = " + str(swVCG)+", SWGSP = "+str(swGSP)+", RVCG = "+str(rVCG)+", RGSP = "+str(rGSP))
	# TODO : bidding_simulator-master -> stats.py draw the scatter plot
