import string
import numpy as np
from historyBidderTuple import historyBidderTuple as hbt
import warnings
class Bidder:
  
    def __init__(self, valuationGenerator, strategy):
        self.valuationGenerator = valuationGenerator
        self.strategy = strategy
        self.history = [] # [valuation, bid, click, price]
        self.revenue = 0
        

    def bid(self):
        valuation = self.valuationGenerator()
        bid = self.strategy.bid(valuation)
        self.history.append([valuation, bid, None, None])
        return bid


    def feedback(self, click, payment):
        self.history[-1][2] = click
        self.history[-1][3] = payment
        self.strategy.learn(self.history[-1])
        if click:
            self.revenue += self.history[-1][0] - payment

class Strategy:

    def bid(self, valuation):
        return valuation

    def learn(self, single_history):
        return

class RandomStrategy(Strategy):

    def bid(self, valuation):
        return np.random.random_sample() * valuation

class Auction:

    def __init__(self, bidders, mechanism):
        self.bidders = bidders
        self.mechanism = mechanism
        self.revenue = 0

    def takeAuction(self):
        bids = []
        for bidder in bidders:
            bids.append(bidder.bid())
        [allocation, payments] = self.mechanism.calcAllocationAndPayments(bids)
        single_history = [[bids[i], None, None] for i in range(len(bidders))]
        for i in range(len(self.mechanism.ctrs)):
            ctr = self.mechanism.ctrs[i]
            click = np.random.random_sample() < ctr
            if click:
                price = payments[i]
                self.revenue += price
            else:
                price = None
            self.bidders[allocation[i]].feedback(click, price)
            single_history[allocation[i]][1:] = [click, payments[i]]
        self.mechanism.learn(single_history)

class Mechanism:
    def __init__(self, ctrs):
        self.ctrs = ctrs

    def calcAllocationAndPayments(self, bids):
        return [allocation, payments]
    def learn(self, single_history):
        return

class GFP(Mechanism):
    pass

class VCG(Mechanism):
    pass


class GSP(Mechanism):
    def calcAllocationAndPayments(self, bids):
        return [allocation, payments]



def uniformValuationGenerator(left, right):
    return np.random.random_sample() * (right - left) + left

def main():
    n = 10
    bidders = [Bidder(uniformValuationGenerator, Strategy()) for i in range(n)]
    ctrs = [0.1 for i in range(10)]
    auction = Auction(bidders, GSP(ctrs))
    n_auction = 10000
    for i in range(n_auction):
        auction.takeAuction()
    print([bidders[i].revenue for i in range(n)])
    print(auction.revenue)







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