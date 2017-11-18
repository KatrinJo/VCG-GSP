import string
import numpy as np
from historyBidderTuple import historyBidderTuple as hbt

class Bidder:
    bidderName = 0 # Bidder的名字，其实就是编号
    history = []
    revenue = []
    clickOrNot = 0
    valuation = 0.0
    bid = 0.0
    price = 0.0
    epislonGreedy = 0.0
    # i0ntrinsicValue = 0.0 # 对slot的真实内心出价
    # b0idValue = 0.0 # 对商品的实际投标价格
    # f0inalPrice = 0.0 # 最后付款
    # regret = 0.0 # 后悔程度
                    # IRpenalty = 0.0 # the penalty for violating individual rationality for
                    # bidder i
  
    def __init__(self, name, ValueRange, valueGenerator, truthOrNot):
        self.bidderName = name
        # self.valuation = v
        self.history = []
        self.revenue = []
        self.clickOrNot = 0
        self.price = 0.0
        self.epislonGreedy = np.random.random_sample()
        
        if valueGenerator == 'uniform':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif valueGenerator == 'uniform-BsmallthanV':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif valueGenerator == 'normal':
            self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

        if truthOrNot == 'truth':
            self.bid = self.valuation
        elif truthOrNot == 'random':
            if valueGenerator == 'uniform': 
                self.bid = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif valueGenerator == 'uniform-BsmallthanV':
                self.bid = np.random.random_sample()*(self.valuation - ValueRange[0]) + ValueRange[0]
            elif valueGenerator == 'normal':
                self.bid = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    def updateEpislonGreedy(self, e = -1):
        if e >= 0:
            self.epislonGreedy = e
        else:
            self.epislonGreedy = np.random.random_sample()

    def newValuation(self, ValueRange, valueGenerator):
        if valueGenerator == 'uniform':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif valueGenerator == 'uniform-BsmallthanV':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif valueGenerator == 'normal':
            self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    # TODO: 产生bid的策略在这里补充，可以利用的数据在history里
    def newBid(self, ValueRange, bidGenerator, truthOrNot):
        if truthOrNot == 'truth':
            self.bid = self.valuation

        elif truthOrNot == 'random':
            # TODO: 基本上在这里写bidGenerator是什么
            if bidGenerator == 'greedy':
                self.bid = 0
            elif bidGenerator == 'e-greedy':
                e = np.random.random_sample()
                if e < self.epislonGreedy:
                    self.bid = np.argmax([2,3,4,5]) # 我乱写了这里
                else:
                    self.bid = np.argmax([2,3,4,5]) # 我乱写了这里
            elif bidGenerator == 'uniform': 
                self.bid = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif bidGenerator == 'uniform-BsmallthanV':
                self.bid = np.random.random_sample()*(self.valuation - ValueRange[0]) + ValueRange[0]
            elif bidGenerator == 'normal':
                self.bid = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]


    def getClickPrice(self, clickOrNot, price):
        self.clickOrNot = clickOrNot
        self.price = price

    def insertHistory(self, t = -1):
        h = hbt(self.valuation, self.bid, self.clickOrNot, self.price)
        l = len(self.history)
        if t == -1:
            self.history.insert(l, h)
        else:
            self.history.insert(t, h)
        
    def revenueSum(self, t = -1): # 计算从0~t时刻的revenue总和
        # return alpha * (self.valuation - self.price)
        l = len(self.history)
        sum = 0
        if t > 0:
            time = np.min([l, t])
        else:
            time = l
        for i in range(time):
            hi = self.history[i]
            uR = hi.clickOrNot * (hi.valuation - hi.price)
            sum = sum + uR    
        return sum