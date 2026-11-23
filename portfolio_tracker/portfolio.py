class Portfolio:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.prices = {}
        self.trades = []
        self.gain = 0.0

class Position:
    def __init__(self, ticker, quantity = 0.0, avg_cost = 0.0):
        self.ticker = ticker
        self.quantity = float(quantity)
        self.avg_cost = float(avg_cost)
