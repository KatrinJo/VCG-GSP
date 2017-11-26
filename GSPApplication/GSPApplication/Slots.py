import numpy as np
import string

class Slots(object):
    numOfSlots = 0
    clickRate = []

    def __init__(self, numSlots, numBidders = 0):
        self.numOfSlots = int(numSlots)
        cR = sorted(np.random.random_sample(self.numOfSlots),reverse=True)
        cR = cR / np.sum(cR)
        self.clickRate = cR
        if (numBidders-numSlots) > 0:
            self.clickRate = np.append(self.clickRate, [0]*(numBidders-numSlots))
        # clickTimes = np.random.randint(0,100,(self.numOfSlots))
        # np.divide(clickTimes,np.sum(clickTimes))
