import numpy as np
import string

class Slots(object):
  numOfSlots = 0
  clickRate = []

  def __init__(self, numSlots, numBidders = 0):
    self.numOfSlots = int(numSlots)
    self.clickRate = sorted(np.random.rand(1,self.numOfSlots)[0],reverse=True)
    if (numBidders-numSlots) > 0:
      self.clickRate.append([0]*(numBidders-numSlots))
    # clickTimes = np.random.randint(0,100,(self.numOfSlots))
    # np.divide(clickTimes,np.sum(clickTimes))
