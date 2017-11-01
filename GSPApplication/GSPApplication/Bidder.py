import string
import numpy as np

class Bidder:
    bidderName = 0 # Bidder的名字，其实就是编号
    intrinsicValue = 0.0 # 对slot的真实内心出价
    bidValue = 0.0 # 对商品的实际投标价格
    finalPrice = 0.0 # 最后付款
    # regret = 0.0 # 后悔程度
                    # IRpenalty = 0.0 # the penalty for violating individual rationality for
                    # bidder i
  
    def __init__(self, name, ValueRange, vfunction, truthOrRandom):
        self.bidderName = name
        # self.intrinsicValue = v
        self.finalPrice = 0.0
        if vfunction == 'uniform':
            self.intrinsicValue = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'uniform-BsmallthanV':
            self.intrinsicValue = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
        elif vfunction == 'normal':
            self.intrinsicValue = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

        if truthOrRandom == 'truth':
            self.bidValue = self.intrinsicValue
        elif truthOrRandom == 'random':
            if vfunction == 'uniform': 
                self.bidValue = np.random.rand(1,1)[0][0]*(ValueRange[1] - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'uniform-BsmallthanV':
                self.bidValue = np.random.rand(1,1)[0][0]*(self.intrinsicValue - ValueRange[0]) + ValueRange[0]
            elif vfunction == 'normal':
                self.intrinsicValue = np.abs((np.random.randn(1)+1)*(ValueRange[1] - ValueRange[0])/2)[0]

    def utility(alpha):
        return alpha * (self.intrinsicValue - self.finalPrice)