import math

from .asset import Asset

from .errors import DuplicateTickerError, InvalidPriceError, UnknownTickerError


class AssetService:
    def __init__(self):
        self.assets = {}
        self.prices = {}

    def add_asset(self, ticker, name):
        ticker_name = ticker.strip().upper()
        if ticker_name in self.assets:
            raise DuplicateTickerError(f"{ticker_name} already exists")

        self.assets[ticker_name] = Asset(ticker_name, name)
        return self.assets[ticker_name]

    def set_price(self, ticker, price):
        ticker_name = ticker.strip().upper()
        if ticker_name not in self.assets:
            raise UnknownTickerError(f"{ticker_name} does not exist")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise InvalidPriceError(f"{price} is not a valid price")

        if not math.isfinite(price) or price < 0:
            raise InvalidPriceError(f"{price} is not a valid price")

        self.prices[ticker_name] = float(price)

    def list_assets(self):
        results = []
        for ticker, asset in self.assets.items():
            results.append((ticker, asset.name, self.prices.get(ticker)))
        return results

