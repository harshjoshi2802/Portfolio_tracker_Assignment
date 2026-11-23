from .asset import Asset

from .errors import DuplicateTickerError

class AssetService:
    def __init__(self):
        self.assets = {}

    def add_asset(self, ticker, name):
        ticker_name = ticker.strip().upper()
        if ticker_name in self.assets:
            raise DuplicateTickerError(f"{ticker_name} already exists")

        self.assets[ticker_name] = Asset(ticker_name, name)
        return self.assets[ticker_name]
