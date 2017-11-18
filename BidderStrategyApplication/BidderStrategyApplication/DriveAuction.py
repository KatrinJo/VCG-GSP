import sys
import io
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


def simulation(numbid, numitem, valueGenFunc, truthOrRandom, repeatTimes):
    auction = Auction(numbid, numitem, valueGenFunc, truthOrRandom)
    for i in range(repeatTimes):
        auction.executeGSP()
    auctionRGSP = auction.revenueSum
    bidderRGSP = []
    for i in range(int(numbid)):
        bidderRGSP.insert(i, auction.bidders[i].revenueSum())
    return auctionRGSP,bidderRGSP

def runAndPrint(numbid, numitem, valueGenFunc, truthOrRandom, repeatTimes):
    auction = Auction(numbid, numitem, valueGenFunc, truthOrRandom)
    SWVCGseq, RVCGseq, SWGSPseq, RGSPseq  = [], [], [], []
    for i in range(repeatTimes):
        # auction = Auction(numbid, numitem, truthOrRandom)
        auction.clearData()

        #auction.executeVCG()
        #swVCG = auction.SocialWelfare
        #rVCG = auction.revenue
        #SWVCGseq = np.append(SWVCGseq, swVCG)
        #RVCGseq = np.append(RVCGseq, rVCG)

        auction.executeGSP()
        #swGSP = auction.SocialWelfare
        rGSP = auction.revenue
        #SWGSPseq = np.append(SWGSPseq, swGSP)
        RGSPseq = np.append(RGSPseq, rGSP)
    #SWVCG = np.mean(SWVCGseq)
    #RVCG = np.mean(RVCGseq)
    #SWGSP = np.mean(SWGSPseq) 
    SWVCG, RVCG, SWGSP = 0, 0, 0
    RGSP = np.mean(RGSPseq)
    #print("seq: RVCG[0] = " + str(RVCGseq[0]) + ", RVCG[n-1] = " + str(RVCGseq[repeatTimes-1]))
    #print("seq: RGSP[0] = " + str(RGSPseq[0]) + ", RGSP[n-1] = " + str(RGSPseq[repeatTimes-1]))
    return [SWVCG, RVCG, SWGSP, RGSP]

if __name__ == '__main__':
    valueGenFunc, truthOrRandom = ['uniform', 'uniform-BsmallthanV', 'normal'], ['random', 'truth']
    lenValueGenFunc = len(valueGenFunc)
    RGSP = [[[] for i in range(lenValueGenFunc)] for j in range(2)]
    bidderRevenue = [[],[]]

    for j in range(1):
        for num in list(range(1,21)):
            for i in range(2):
                print("The number of Bidders is " + str(num) + ", and the number of Items is " + str(num) + ", " + truthOrRandom[i])
                #[swVCG, rVCG, swGSP, rGSP] = runAndPrint(num, num, valueGenFunc[j],truthOrRandom[i], 10000)
                auctionRGSP, bidderRGSP = simulation(num, num, valueGenFunc[j],truthOrRandom[i], 10000*num)
                bidderRevenue[i].append(bidderRGSP)
                RGSP[j][i] = np.append(RGSP[j][i], auctionRGSP)
                print("bidderRevenue = " + str(bidderRGSP))

    x_axis=[i for i in range(1,21)]
        
    # print(SWVCG[0][0])
    Revenue = io.open("Revenue.txt","w")
    #SocialWelfare = io.open("SocialWelfare.txt","w")
    for j in range(2):
        for i in range(2):
            #SocialWelfare.writelines("SWVCG" + valueGenFunc[j] + " " + truthOrRandom[i] +str(SWVCG[j][i]) + "\n")
            #SocialWelfare.writelines("SWGSP" + valueGenFunc[j] + " " + truthOrRandom[i] +str(SWGSP[j][i]) + "\n")
            #Revenue.writelines("RVCG" + valueGenFunc[j] + " " + truthOrRandom[i] +str(RVCG[j][i]) + "\n")
            Revenue.writelines("RGSP" + valueGenFunc[j] + " " + truthOrRandom[i] +str(RGSP[j][i]) + "\n")
    Revenue.close()

    plt.figure(1)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("revenue")
    plt.title("revenue with different number of bidder and slot")
    plt.plot(x_axis,RGSP[0][0],label = truthOrRandom[0] + ' GSP')
    plt.plot(x_axis,RGSP[0][1],label = truthOrRandom[1] + ' GSP')
    #plt.plot(x_axis,RGSP[1][0],label = "b<v " + truthOrRandom[0] + ' GSP')
    #plt.plot(x_axis,RGSP[1][1],label = "b<v " + truthOrRandom[1] + ' GSP')
    plt.legend()
    plt.savefig("revenue.png")