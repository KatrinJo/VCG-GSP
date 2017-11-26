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
import multi_simulate as ms
import multiprocessing
import time

from Bidder import Bidder
from Auction import Auction
from Slots import Slots

def simulation(numOfBid, numOfSlot, valueGenFunc, truthOrRandom, repeatTimes):
    auction = Auction(numOfBid, numOfSlot, valueGenFunc, truthOrRandom)
    for i in range(repeatTimes):
        auction.executeGSP()
    auctionRGSP = auction.revenueSum
    bidderRGSP = []
    for i in range(int(numOfBid)):
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
    # numbid = int(sys.argv[1])
    # numitem = int(sys.argv[2])
    # method = ['VCG','GSP']
    # methodOfBid = sys.argv[3]
    # truthOrRandom = sys.argv[4]
    #SWVCG = [[[] for i in range(lenValueGenFunc)] for j in range(2)]#[[[]]*(lenValueGenFunc)]*2
    #SWGSP = [[[] for i in range(lenValueGenFunc)] for j in range(2)]
    #RVCG = [[[] for i in range(lenValueGenFunc)] for j in range(2)]
        
    # post order : j num i

    
    valueGenFunc, truthOrRandom = ['uniform', 'uniform-BsmallthanV', 'normal'], ['random', 'truth']
    lenValueGenFunc = len(valueGenFunc)
    bidderRevenue = [[],[]]
    RGSP = [[[] for i in range(lenValueGenFunc)] for j in range(2)]

    NUM=20

    
    for i in range(2):
        bidderRevenue[i] = [[] for x in range(NUM)]
        for j in range(1):
            RGSP[j][i] = [0 for x in range(NUM)]
    
    
    q=multiprocessing.Queue()

    p = []
    for i in range(2):
        for j in range(1):
            for num in list(range(1,NUM+1)):
                print("The number of Bidders is " + str(num) + ", and the number of Items is " + str(num) + ", " + truthOrRandom[i])
                print ("now it is",num,'\n')
                #[swVCG, rVCG, swGSP, rGSP] = runAndPrint(num, num, valueGenFunc[j],truthOrRandom[i], 10000)
                #SWVCG[j][i] = np.append(SWVCG[j][i], swVCG)
                #RVCG[j][i] = np.append(RVCG[j][i], rVCG)
                #SWGSP[j][i] = np.append(SWGSP[j][i], swGSP)
                #ms.simulate(num ,j ,i ,100,valueGenFunc,truthOrRandom)
                p.append(multiprocessing.Process(target = ms.simulate, args = (num ,j ,i ,2000,valueGenFunc,truthOrRandom,q)))
                p[len(p)-1].start()
                #auctionRGSP, bidderRGSP = simulation(num, num, valueGenFunc[j],truthOrRandom[i], 100)
                #bidderRevenue[i][num-1] = bidderRGSP
                #RGSP[j][i][num-1] = auctionRGSP
                #print("SWVCG = " + str(swVCG) + ", SWGSP = " + str(swGSP) + ", RVCG = " + str(rVCG) + ", RGSP = " + str(rGSP))
    while 1:
        time.sleep(1)
        flag=0
        for x in p:
            if x.is_alive():
                flag+=1
        if flag == 0:
            break
        print(flag)

    while not q.empty():
        a=q.get(1)
        RGSP[a[0]][a[1]][a[2]-1]=a[3]
        print(a)

    x_axis=[i for i in range(1,NUM+1)]
    
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