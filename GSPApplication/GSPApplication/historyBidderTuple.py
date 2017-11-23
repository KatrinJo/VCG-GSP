class historyBidderTuple:
    def __init__(self, valuation, bid, clickRate, price):
        self.valuation = valuation
        self.bid = bid
        self.clickRate = clickRate
        self.price = price
        self.revenue = clickRate * (valuation - price)