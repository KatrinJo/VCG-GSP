import string
import numpy as np
from historyBidderTuple import historyBidderTuple as hbt
import warnings
class Bidder:
    bidderName = 0 # Bidder的名字，其实就是编号
    history = []
    revenue = []
    clickOrNot = 0
    valuation = 0.0
    bid = 0.0
    price = 0.0
    # i0ntrinsicValue = 0.0 # 对slot的真实内心出价
    # b0idValue = 0.0 # 对商品的实际投标价格
    # f0inalPrice = 0.0 # 最后付款
    # regret = 0.0 # 后悔程度
                    # IRpenalty = 0.0 # the penalty for violating individual rationality for
                    # bidder i
  
    def __init__(self, name, ValueRange, vfunction, truthOrNot):
        self.bidderName = name
        self.valuation = 0
        self.history = []
        self.revenue = []
        self.clickOrNot = 0
        self.price = 0.0
        
        if vfunction == 'uniform':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'uniform-BsmallthanV':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'normal':
            self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]         # 不是很清楚

        if truthOrNot == 'truth':
            self.bid = self.valuation
        elif truthOrNot == 'random':
            if vfunction == 'uniform': 
                self.bid = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'uniform-BsmallthanV':                                                        # bid<=valuation
                self.bid = np.random.random_sample()*(self.valuation - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'normal':
                self.bid = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    def newValuation(self, ValueRange, vfunction):
        if vfunction == 'uniform':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'uniform-BsmallthanV':
            self.valuation = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'normal':
            self.valuation = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    # TODO: 产生bid的策略在这里补充
    def get_bid_poly(self,k,p,ValueRange):
        warnings.simplefilter('ignore', np.RankWarning)
        l=len(self.history)
#        print("history of",self.bidderName,l)
        if l<=1:
            return self.valuation
        else:
            if p>l-1:
                p=l-1
            start=max(0,l-k)
            click = np.array([self.history[i].clickOrNot for i in range(start,l)])
            price = np.array([self.history[i].price      for i in range(start,l)])
            bid   = np.array([self.history[i].bid        for i in range(start,l)])
            bidMean = bid.mean()
            bid = bid - bidMean
#            a = np.polyfit(bid,click,p)
#            b = np.polyfit(bid,click*price,p)
            c = np.polyfit(bid,click*(np.array([self.valuation for i in range(start,l)]) - price),p)
#            print(c)
            d = np.polyder(c)
            root = np.roots(d)
            root = [x for x in root if np.isreal(x)]
            root = np.append(root,ValueRange[0])
            root = np.append(root,ValueRange[1])
#            print(root)
            ma = np.argmax([np.polyval(c,x) for x in root if x >= ValueRange[0] and x <= ValueRange[1]])
            return ma+bidMean

    def newBid(self, ValueRange, bfunction, truthOrNot):
        if truthOrNot == 'truth':
            self.bid = self.valuation

        elif truthOrNot == 'random':
            if bfunction == 'uniform': 
                self.bid = np.random.random_sample()*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif bfunction == 'uniform-BsmallthanV':
                self.bid = np.random.random_sample()*(self.valuation - ValueRange[0]) + ValueRange[0]
            elif bfunction == 'normal':
                self.bid = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]
            elif bfunction == 'poly':
                self.bid = self.get_bid_poly(50,10,ValueRange)


    def getClickPrice(self, clickOrNot, price):
        self.clickOrNot = clickOrNot
        self.price = price

    def insertHistory(self, t = -1):
        h = hbt(self.valuation, self.bid, self.clickOrNot, self.price)
        l = len(self.history)
        for x in range(l):                                      # 不正确的改正
            if self.history[x].bid == self.bid:			# 写成这样是因为bid（自变量）相同的数据会让多项式拟合出现除0错误
                self.history[x] = h
                return None
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