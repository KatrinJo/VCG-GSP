import sys
import numpy as np
import string
import os
import matplotlib
import matplotlib.pyplot as plt
import pylab
from scipy.optimize import linprog
from scipy.stats import gaussian_kde
import math

from Bidder import Bidder
from Auction import Auction
from Slots import Slots

def runAndPrint(numbid, numitem, truthOrRandom):
    #str = "The number of Bidders is " + str(numbid) + ", and the number of Items
    #is " + str(numitem)
    auction = Auction(numbid, numitem, truthOrRandom)
    '''
    print("The bidderName and their true value:")
    for b in auction.bidders:
    print("Bidder" + str(b.bidderName) + ", true value is :" +
    str(b.intrinsicValue) + ", bid is " + str(b.bidValue))
    print(" ")
    '''
    auction.executeVCG()
    SWVCG = auction.SocialWelfare
    RVCG = auction.revenue
    '''
    print("Now it is VCG result: ")
    print("valueVac = " + str(auction.valueVec))
    print("bidVec = " + str(auction.bidVec))
    print("allocation = " + str(auction.allocation))
    print("The bidders should pay = " + str(auction.priceBids))
    print("revenue = " + str(auction.revenue))
    print("SocialWelfare = " + str(auction.SocialWelfare))
    print("clickThroughRate = " + str(auction.slots.clickRate))
    print(" ")
    '''
    auction.executeGSP()
    SWGSP = auction.SocialWelfare
    RGSP = auction.revenue
    '''
    print("Now it is GSP result: ")
    print("valueVac = " + str(auction.valueVec))
    print("bidVec = " + str(auction.bidVec))
    print("allocation = " + str(auction.allocation))
    print("The bidders should pay = " + str(auction.priceBids))
    print("revenue = " + str(auction.revenue))
    print("SocialWelfare = " + str(auction.SocialWelfare))
    print("clickThroughRate = " + str(auction.slots.clickRate))
    print(" ")
    '''
    return [SWVCG, RVCG, SWGSP, RGSP]

if __name__ == '__main__':
    # numbid = int(sys.argv[1])
    # numitem = int(sys.argv[2])
    # method = ['VCG','GSP']
    truthOrRand = ['random', 'truth']
    # methodOfBid = sys.argv[3]
    # truthOrRandom = sys.argv[4]
    SWVCG = [[],[]]
    SWGSP = [[],[]]
    RVCG = [[],[]]
    RGSP = [[],[]]
    for num in list(range(1,21)):
        for i in range(2):
            print("The number of Bidders is " + str(num) + ", and the number of Items is " + str(num) + ", " + truthOrRand[i])
            [swVCG, rVCG, swGSP, rGSP] = runAndPrint(num, num, truthOrRand[i])
            SWVCG[i] = np.append(SWVCG[i], swVCG)
            RVCG[i] = np.append(RVCG[i], rVCG)
            SWGSP[i] = np.append(SWGSP[i], swGSP)
            RGSP[i] = np.append(RGSP[i], rGSP)
            print("SWVCG = " + str(swVCG) + ", SWGSP = " + str(swGSP) + ", RVCG = " + str(rVCG) + ", RGSP = " + str(rGSP))
            # TODO : bidding_simulator-master -> stats.py draw the scatter plot
    # print(SWVCG)
    # print(SWGSP)
    x_axis=[i for i in range(1,21)]
    
    pylab.figure(1)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("social welfare")
    plt.title("random - social welfare with different number of bidder and slot")
    plt.plot(x_axis,SWVCG[0],label = 'VCG')
    plt.plot(x_axis,SWGSP[0],label = 'GSP')
    #print("SWVCG[0] = " + str(SWVCG[0]))
    #print("SWGSP[0] = " + str(SWGSP[0]))
    # plt.show()
    plt.legend()
    plt.savefig("random - social welfare.png")

    plt.figure(2)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("social welfare")
    plt.title("truth - social welfare with different number of bidder and slot")
    plt.plot(x_axis,SWVCG[1],label = 'VCG')
    plt.plot(x_axis,SWGSP[1],label = 'GSP')
    #print("SWVCG[1] = " + str(SWVCG[1]))
    #print("SWGSP[1] = " + str(SWGSP[1]))
    # plt.show()
    plt.legend()
    plt.savefig("truth - social welfare.png")

    plt.figure(3)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("revenue")
    plt.title("random - revenue with different number of bidder and slot")
    plt.plot(x_axis,RVCG[0],label = 'VCG')
    plt.plot(x_axis,RGSP[0],label = 'GSP')
    #print("RVCG[0] = " + str(RVCG[0]))
    #print("RGSP[0] = " + str(RGSP[0]))
    # plt.show()
    plt.legend()
    plt.savefig("random - revenue.png")
    
    plt.figure(4)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("revenue")
    plt.title("truth - revenue with different number of bidder and slot")
    plt.plot(x_axis,RVCG[1],label = 'VCG')
    plt.plot(x_axis,RGSP[1],label = 'GSP')
    #print("RVCG[1] = " + str(RVCG[1]))
    #print("RGSP[1] = " + str(RGSP[1]))
    # plt.show()
    plt.legend()
    plt.savefig("truth - revenue.png")