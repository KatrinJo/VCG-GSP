from Bidder import Bidder
from Slots import Slots
from historyAuctionTuple import historyAuctionTuple as hat
import numpy as np
import string
import operator
import random
# sorted_x = sorted(x, key=operator.attrgetter('score'))

class Auction:
    #bidders = [] # 出价人序列,[Bidder,Bidder,Bidder]
    #valueVec = [] # 估值向量
    #bidVec = [] # 出价向量
  
    #allocation = [] # 第i个slot分配给第allocation[i]个bidder  [1,3,5,2,0]
    #priceBids = [] # 每个人要交的钱,[ 10, 10, 2]
    #bidGetSlot = [] # 第i个bidder拿到第bidGetSlot[i]个slot

    #numOfBidder = 0 # 出价人数量，编号从0~numOfBidder-1
    #numOfSlots = 0 # slot数量，编号从0~numOfBidder-1

    #revenue = 0
    #SocialWelfare = 0

    def __init__(self, numbid, numslots, valueGenerator, truthOrNot):
        self.maxCapValue = 10
        self.bidders = [] # 出价人序列,[Bidder,Bidder,Bidder]
        self.bidVec = [] # 出价向量 
        self.auctionHistory = [] # 历史数据

        self.numOfBidder = int(numbid)
        self.numOfSlots = int(numslots)
        self.allocation = [ -1 for i in range(self.numOfBidder)] # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = [ -1 for i in range(self.numOfBidder)] # slot编号>=numOfSlots的相当于lose the auction
        self.priceBids = [0 for i in range(self.numOfBidder)]
        self.revenue = 0
        self.SocialWelfare = 0
        self.truthOrNot = truthOrNot
        self.valueGenerator = valueGenerator
        
        tmpValueVec = []
        tmpBidVec = []
        bidder = []
        for i in range(self.numOfBidder):
            bidder.append(Bidder(i,[0,self.maxCapValue],valueGenerator,truthOrNot))
        bidder = sorted(bidder, key=operator.attrgetter('valuation'), reverse = True)

        for i in range(self.numOfBidder):
            bidder[i].bidderName = i
            tmpValueVec = np.append(tmpValueVec, bidder[i].valuation)
            tmpBidVec = np.append(tmpBidVec, bidder[i].bid)
        self.bidders = bidder
        self.valueVec = tmpValueVec
        self.bidVec = tmpBidVec
        self.slots = Slots(self.numOfSlots,self.numOfBidder)
  
    def clearData(self):
        self.allocation = [ -1 for i in range(self.numOfBidder)] # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = [ -1 for i in range(self.numOfBidder)] # slot编号>=numOfSlots的相当于lose the auction
        self.priceBids = [0 for i in range(self.numOfBidder)]
        self.revenue = 0
        self.SocialWelfare = 0
        self.bidders.clear()
        self.bidVec = []
        self.auctionHistory.clear()
        
        tmpValueVec = []
        tmpBidVec = []
        bidder = []
        for i in range(self.numOfBidder):
            bidder.append(Bidder(i,[0,self.maxCapValue],self.valueGenerator,self.truthOrNot))
        bidder = sorted(bidder, key=operator.attrgetter('valuation'), reverse = True)

        for i in range(self.numOfBidder):
            bidder[i].bidderName = i
            tmpValueVec = np.append(tmpValueVec, bidder[i].valuation)
            tmpBidVec = np.append(tmpBidVec, bidder[i].bid)
        self.bidders = bidder
        self.valueVec = tmpValueVec
        self.bidVec = tmpBidVec
        self.slots = Slots(self.numOfSlots,self.numOfBidder)
  
    def executeGSP(self):
        self.allocation = [ -1 for i in range(self.numOfBidder)] # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = [ -1 for i in range(self.numOfBidder)] # slot编号>=numOfSlots的相当于lose the auction
        self.priceBids = [0 for i in range(self.numOfBidder)]
        self.revenue = 0
        self.SocialWelfare = 0

        bv = np.array(self.bidVec)
        tmp = np.argsort(-bv)
        sortBid = bv[tmp]
        self.allocation = tmp # [6, 7, 0, 5, 2, 4, 1, 3]表示slot0号给bidder6号，slot1号给bidder7号
        for i in range(self.numOfBidder):
            self.bidGetSlot[tmp[i]]=i # [2, 6, 4, 7, 5, 3, 0, 1]表示bidder0号拿slot2号，bidder1号拿slot6号
    
        # TODO:
        for i in range(self.numOfSlots-1): # 实际每个人要出的钱
            self.priceBids[tmp[i]] = sortBid[i+1]
            self.bidders[tmp[i]].price = self.priceBids[tmp[i]]
        self.priceBids[tmp[self.numOfSlots-1]] = 0
        self.bidders[tmp[self.numOfSlots-1]].price = 0

        alpha = np.append(self.slots.clickRate,[0 for i in range(self.numOfBidder - self.numOfSlots)])
        bidPrice = np.append(sortBid[1:],0)
        self.revenue = np.sum(np.multiply(alpha, bidPrice))

        bidValue = np.array(self.valueVec)[self.allocation]
        self.SocialWelfare = np.sum(np.multiply(alpha, bidValue))

        result = hat(self.numOfBidder, self.numOfSlots, self.bidVec, self.allocation, self.bidGetSlot, alpha, self.priceBids, self.revenue)
        l = len(self.auctionHistory)
        self.auctionHistory.insert(l, result)

    def executeVCG(self):
        self.allocation = [ -1 for i in range(self.numOfBidder)] # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = [ -1 for i in range(self.numOfBidder)] # slot编号>=numOfSlots的相当于lose the auction
        self.priceBids = [0 for i in range(self.numOfBidder)]
        self.revenue = 0
        self.SocialWelfare = 0
    
        bv = np.array(self.bidVec)
        tmp = np.argsort(-bv)
        sortBid = bv[tmp]
        self.allocation = tmp # [6, 7, 0, 5, 2, 4, 1, 3]表示slot0号给bidder6号，slot1号给bidder7号
    
        for i in range(self.numOfBidder):
            self.bidGetSlot[tmp[i]] = i # [2, 6, 4, 7, 5, 3, 0, 1]表示bidder0号拿slot2号，bidder1号拿slot6号
    
        alpha = np.append(self.slots.clickRate,[0 for i in range(self.numOfBidder - self.numOfSlots)])
        alphaBidGetSlot = alpha[self.bidGetSlot]
    
        for i in range(self.numOfBidder): # 实际每个人要出的钱
            alphaSlotI = self.bidGetSlot[i] # 表示第i个bidder拿到的slot位
            if alpha[alphaSlotI] == 0:
                continue
            suma = 0
            for j in list(range(alphaSlotI + 1, self.numOfBidder)):
                suma = suma + (alpha[j - 1] - alpha[j]) * bv[self.allocation[j]]
            self.priceBids[i] = suma / alpha[alphaSlotI]
            self.bidders[i].price = self.priceBids[i]

        sumRevenue = 0
        for i in list(range(1,self.numOfBidder)):
            tmp = (i - 1) * (alpha[i - 1] - alpha[i]) * self.bidders[i].price # 根据GSP是price，但是由于VCG是truth-telling，price和实际value一样
            sumRevenue = sumRevenue + tmp
        self.revenue = sumRevenue
        bidValue = np.array(self.valueVec)[self.allocation]
        self.SocialWelfare = np.sum(np.multiply(alpha, bidValue))