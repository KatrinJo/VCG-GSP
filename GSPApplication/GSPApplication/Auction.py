from Bidder import Bidder
from Slots import Slots
import numpy as np
import string
import operator
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

    def __init__(self, numbid, numslots, valueGenFunc, truthOrRandom):
        self.maxValueBid = 10
        self.bidders = [] # 出价人序列,[Bidder,Bidder,Bidder]
        self.bidVec = [] # 出价向量

        self.numOfBidder = int(numbid)
        self.numOfSlots = int(numslots)
        self.allocation = [ -1 for i in range(self.numOfBidder)] # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = [ -1 for i in range(self.numOfBidder)] # slot编号>=numOfSlots的相当于lose the auction
        self.priceBids = [0 for i in range(self.numOfBidder)]
        self.revenue = 0
        self.SocialWelfare = 0
        self.truthOrNot = truthOrRandom
        self.valueGenerator = valueGenFunc
        
        tmpValueVec = []
        tmpBidVec = []
        bidder = []
        for i in range(self.numOfBidder):
            bidder.append(Bidder(i,[0,self.maxValueBid],valueGenFunc,truthOrRandom))
        bidder = sorted(bidder, key=operator.attrgetter('intrinsicValue'), reverse = True)

        for i in range(self.numOfBidder):
            bidder[i].bidderName = i
            tmpValueVec = np.append(tmpValueVec, bidder[i].intrinsicValue)
            tmpBidVec = np.append(tmpBidVec, bidder[i].bidValue)
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
        
        tmpValueVec = []
        tmpBidVec = []
        bidder = []
        for i in range(self.numOfBidder):
            bidder.append(Bidder(i,[0,self.maxValueBid],self.valueGenerator,self.truthOrNot))
        bidder = sorted(bidder, key=operator.attrgetter('intrinsicValue'), reverse = True)

        for i in range(self.numOfBidder):
            bidder[i].bidderName = i
            tmpValueVec = np.append(tmpValueVec, bidder[i].intrinsicValue)
            tmpBidVec = np.append(tmpBidVec, bidder[i].bidValue)
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
            self.bidders[tmp[i]].finalPrice = self.priceBids[tmp[i]]
        self.priceBids[tmp[self.numOfSlots-1]] = 0
        self.bidders[tmp[self.numOfSlots-1]].finalPrice = 0

        alpha = np.append(self.slots.clickRate,[0 for i in range(self.numOfBidder - self.numOfSlots)])
        bidPrice = np.append(sortBid[1:],0)
        self.revenue = np.sum(np.multiply(alpha, bidPrice))

        bidValue = np.array(self.valueVec)[self.allocation]
        self.SocialWelfare = np.sum(np.multiply(alpha, bidValue))


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
            self.bidders[i].finalPrice = self.priceBids[i]

        sumRevenue = 0
        for i in list(range(1,self.numOfBidder)):
            tmp = (i - 1) * (alpha[i - 1] - alpha[i]) * self.bidders[i].finalPrice # 根据GSP是finalPrice，但是由于VCG是truth-telling，finalPrice和实际value一样
            sumRevenue = sumRevenue + tmp
        self.revenue = sumRevenue
        bidValue = np.array(self.valueVec)[self.allocation]
        self.SocialWelfare = np.sum(np.multiply(alpha, bidValue))