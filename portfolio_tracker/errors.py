class PortfolioTrackerError(Exception):
    pass

class DuplicateTickerError(PortfolioTrackerError):
    pass

class InvalidPriceError(PortfolioTrackerError):
    pass

class UnknownTickerError(PortfolioTrackerError):
    pass

class DuplicatePortfolioError(PortfolioTrackerError):
    pass

class UnknownPortfolioError(PortfolioTrackerError):
    pass

class PortfolioHasSharesError(PortfolioTrackerError):
    pass

class NoSelectedPortfolioError(PortfolioTrackerError):
    pass

class InvalidQuantityError(PortfolioTrackerError):
    pass

class InsufficientCashError(PortfolioTrackerError):
    pass

class InsufficientSharesError(PortfolioTrackerError):
    pass
