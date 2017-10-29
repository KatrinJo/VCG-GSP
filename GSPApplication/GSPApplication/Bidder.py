import string
import numpy as np

class Bidder:
  bidderName = 0 # Bidder的名字，其实就是编号
  intrinsicValue = 0.0 # 对slot的真实内心出价
  bidValue = 0.0 # 对商品的实际投标价格
  finalPrice = 0.0 # 最后付款
  # regret = 0.0 # 后悔程度
  # IRpenalty = 0.0 # the penalty for violating individual rationality for bidder i
  
  def __init__(self, name, v, b, function):
    self.bidderName = name
    self.intrinsicValue = v
    self.finalPrice = 0.0
    if function == 'truth':
      self.bidValue = v
    elif function == 'random':
      self.bidValue = b

  def utility(alpha):
    return alpha*(self.intrinsicValue - self.finalPrice)