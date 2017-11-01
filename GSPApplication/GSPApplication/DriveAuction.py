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



def runAndPrint(numbid, numitem, valueGenFunc, truthOrRandom, repeatTimes):
    auction = Auction(numbid, numitem, valueGenFunc, truthOrRandom)
    SWVCGseq, RVCGseq, SWGSPseq, RGSPseq  = [], [], [], []
    for i in range(repeatTimes):
        # auction = Auction(numbid, numitem, truthOrRandom)
        auction.clearData()

        auction.executeVCG()
        swVCG = auction.SocialWelfare
        rVCG = auction.revenue
        SWVCGseq = np.append(SWVCGseq, swVCG)
        RVCGseq = np.append(RVCGseq, rVCG)

        auction.executeGSP()
        swGSP = auction.SocialWelfare
        rGSP = auction.revenue
        SWGSPseq = np.append(SWGSPseq, swGSP)
        RGSPseq = np.append(RGSPseq, rGSP)
    SWVCG = np.mean(SWVCGseq)
    RVCG = np.mean(RVCGseq)
    SWGSP = np.mean(SWGSPseq) 
    RGSP = np.mean(RGSPseq)
    print("seq: RVCG[0] = " + str(RVCGseq[0]) + ", RVCG[n-1] = " + str(RVCGseq[repeatTimes-1]))
    print("seq: RGSP[0] = " + str(RGSPseq[0]) + ", RGSP[n-1] = " + str(RGSPseq[repeatTimes-1]))
    return [SWVCG, RVCG, SWGSP, RGSP]

if __name__ == '__main__':
    # numbid = int(sys.argv[1])
    # numitem = int(sys.argv[2])
    # method = ['VCG','GSP']
    # methodOfBid = sys.argv[3]
    # truthOrRandom = sys.argv[4]
    valueGenFunc, truthOrRandom = ['uniform', 'uniform-BsmallthanV', 'normal'], ['random', 'truth']
    lenValueGenFunc = len(valueGenFunc)
    SWVCG = [[[] for i in range(lenValueGenFunc)] for j in range(2)]#[[[]]*(lenValueGenFunc)]*2
    SWGSP = [[[] for i in range(lenValueGenFunc)] for j in range(2)]
    RVCG = [[[] for i in range(lenValueGenFunc)] for j in range(2)]
    RGSP = [[[] for i in range(lenValueGenFunc)] for j in range(2)]

    for j in range(2):
        for num in list(range(1,21)):
            for i in range(2):
                print("The number of Bidders is " + str(num) + ", and the number of Items is " + str(num) + ", " + truthOrRandom[i])
                [swVCG, rVCG, swGSP, rGSP] = runAndPrint(num, num, valueGenFunc[j],truthOrRandom[i], 10000)
                SWVCG[j][i] = np.append(SWVCG[j][i], swVCG)
                RVCG[j][i] = np.append(RVCG[j][i], rVCG)
                SWGSP[j][i] = np.append(SWGSP[j][i], swGSP)
                RGSP[j][i] = np.append(RGSP[j][i], rGSP)
                print("SWVCG = " + str(swVCG) + ", SWGSP = " + str(swGSP) + ", RVCG = " + str(rVCG) + ", RGSP = " + str(rGSP))

    x_axis=[i for i in range(1,21)]
        
    # print(SWVCG[0][0])
    Revenue = io.open("Revenue.txt","w")
    SocialWelfare = io.open("SocialWelfare.txt","w")
    for j in range(2):
        for i in range(2):
            SocialWelfare.writelines("SWVCG" + valueGenFunc[j] + " " + truthOrRandom[i] +str(SWVCG[j][i]) + "\n")
            SocialWelfare.writelines("SWGSP" + valueGenFunc[j] + " " + truthOrRandom[i] +str(SWGSP[j][i]) + "\n")
            Revenue.writelines("RVCG" + valueGenFunc[j] + " " + truthOrRandom[i] +str(RVCG[j][i]) + "\n")
            Revenue.writelines("RGSP" + valueGenFunc[j] + " " + truthOrRandom[i] +str(RGSP[j][i]) + "\n")
    Revenue.close()
    SocialWelfare.close()
    plt.figure(1)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("social welfare")
    plt.title("social welfare with different number of bidder and slot")
    plt.plot(x_axis,SWVCG[0][0],label = truthOrRandom[0] + ' VCG')
    plt.plot(x_axis,SWGSP[0][0],label = truthOrRandom[0] + ' GSP')
    plt.plot(x_axis,SWVCG[0][1],label = truthOrRandom[1] + ' VCG')
    plt.plot(x_axis,SWGSP[0][1],label = truthOrRandom[1] + ' GSP')
    plt.plot(x_axis,SWVCG[1][0],label = "b<v " + truthOrRandom[0] + ' VCG')
    plt.plot(x_axis,SWGSP[1][0],label = "b<v " + truthOrRandom[0] + ' GSP')
    plt.plot(x_axis,SWVCG[1][1],label = "b<v " + truthOrRandom[1] + ' VCG')
    plt.plot(x_axis,SWGSP[1][1],label = "b<v " + truthOrRandom[1] + ' GSP')
    plt.legend()
    plt.savefig("social welfare.png")

    plt.figure(2)
    plt.xlabel("The number of bidder and slot")
    plt.ylabel("revenue")
    plt.title("revenue with different number of bidder and slot")
    plt.plot(x_axis,RVCG[0][0],label = truthOrRandom[0] + ' VCG')
    plt.plot(x_axis,RGSP[0][0],label = truthOrRandom[0] + ' GSP')
    plt.plot(x_axis,RVCG[0][1],label = truthOrRandom[1] + ' VCG')
    plt.plot(x_axis,RGSP[0][1],label = truthOrRandom[1] + ' GSP')
    plt.plot(x_axis,RVCG[1][0],label = "b<v " + truthOrRandom[0] + ' VCG')
    plt.plot(x_axis,RGSP[1][0],label = "b<v " + truthOrRandom[0] + ' GSP')
    plt.plot(x_axis,RVCG[1][1],label = "b<v " + truthOrRandom[1] + ' VCG')
    plt.plot(x_axis,RGSP[1][1],label = "b<v " + truthOrRandom[1] + ' GSP')
    plt.legend()
    plt.savefig("revenue.png")