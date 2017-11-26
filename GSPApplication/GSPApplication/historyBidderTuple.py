class historyBidderTuple:
    def __init__(self, valuation, bid, clickOrNot, price):
        self.valuation = valuation
        self.bid = bid
        self.clickOrNot = clickOrNot
        self.price = price
        self.revenue = clickOrNot * (valuation - price)