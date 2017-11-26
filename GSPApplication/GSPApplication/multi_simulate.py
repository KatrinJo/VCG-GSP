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
import multiprocessing
import DriveAuction as DA

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

def simulate(num,j,i,time,valueGenFunc,truthOrRandom,q):

    auctionRGSP, bidderRGSP = simulation(num, num, valueGenFunc[j],truthOrRandom[i], time)
    #bidderRevenue[i][num-1] = bidderRGSP       #sorry 这个被我注掉了，如果以后需要再加上
    #print("A",auctionRGSP)
    #RGSP[j][i][num-1]=auctionRGSP
    q.put([j,i,num,auctionRGSP])
    #print("here ",RGSP[j][i])
    #DA.set_RGSP(j,i,num,auctionRGSP)


