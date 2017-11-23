import string
import numpy as np
from historyBidderTuple import historyBidderTuple as hbt

class Bidder:
    bidderName = 0 # Bidder的名字，其实就是编号
    valuation = 0.0 # 对slot的真实内心出价
    bid = 0.0 # 对商品的实际投标价格
    price = 0.0 # 最后付款
    revenue = [] # 多时期的收益
    history = [] # 多时期的历史数据
    clickRate = 0.0 # 点击率
    # regret = 0.0 # 后悔程度
                    # IRpenalty = 0.0 # the penalty for violating individual rationality for
                    # bidder i
  
    def __init__(self, name, ValueRange, vfunction, truthOrRandom):
        self.bidderName = name
        # self.valuation = v
        self.price = 0.0
        self.history = []
        self.revenue = []
        self.clickRate = 0
        self.price = 0.0

        if vfunction == 'uniform':
            self.valuation = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'uniform-BsmallthanV':
            self.valuation = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'normal':
            self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

        if truthOrRandom == 'truth':
            self.bid = self.valuation
        elif truthOrRandom == 'random':
            if vfunction == 'uniform': 
                self.bid = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'uniform-BsmallthanV':
                self.bid = np.random.rand(1,1)[0][0]*(self.valuation - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'normal':
                self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    def utility(self, alpha):
        # return alpha * (self.valuation - self.price)
        return alpha * (self.valuation - self.price)
        sum = 0
        
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

    def insertHistory(self, t = -1):
        h = hbt(self.valuation, self.bid, self.clickOrNot, self.price)
        l = len(self.history)
        if t == -1:
            self.history.insert(l, h)
        else:
            self.history.insert(t, h)