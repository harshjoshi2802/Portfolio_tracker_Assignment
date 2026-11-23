class PortfolioTrackerError(Exception):
    pass

class DuplicateTickerError(PortfolioTrackerError):
    pass

class InvalidPriceError(PortfolioTrackerError):
    pass

class UnknownTickerError(PortfolioTrackerError):
    pass