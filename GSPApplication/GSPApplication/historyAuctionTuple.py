class historyAuctionTuple(object):
    def __init__(self, numbid, numslots, bidVec,  allocation, bidGetSlot, clickRate, priceBids, revenue):
        self.numOfBidder = int(numbid)
        self.numOfSlots = int(numslots)
        self.bidVec = bidVec # 出价向量
        self.allocation = allocation # 从numOfSlots~numOfBidder-1号的是点击率为0的
        self.bidGetSlot = bidGetSlot # slot编号>=numOfSlots的相当于lose the auction
        self.clickRate = clickRate
        self.priceBids = priceBids # 最后出的钱
        self.revenue = revenue