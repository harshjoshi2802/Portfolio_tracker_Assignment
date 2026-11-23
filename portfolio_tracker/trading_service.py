import math
from .errors import (
    NoSelectedPortfolioError,
    InvalidPriceError,
    InvalidQuantityError,
    InsufficientCashError,
    InsufficientSharesError,
    UnknownTickerError,
)
from .portfolio import Position


class TradingService:
    def __init__(self, asset_service, portfolio_service):
        if asset_service is None:
            raise ValueError("asset_service is required.")
        if portfolio_service is None:
            raise ValueError("portfolio_service is required.")

        self.asset_service = asset_service
        self.portfolio_service = portfolio_service
        self.cash = 0.0

    def deposit_cash(self, amount):
        validated_amount = self._validate_positive_number(
            amount, InvalidQuantityError, "Deposit amount must be greater than zero."
        )
        self.cash += validated_amount
        return self.cash

    def get_cash(self):
        return self.cash

    def buy(self, ticker, quantity, price):
        portfolio = self._require_selected_portfolio()
        norm_ticker = self._require_registered_ticker(ticker)
        qty = self._validate_positive_number(
            quantity, InvalidQuantityError, "Quantity must be greater than zero."
        )
        px = self._validate_positive_number(
            price, InvalidPriceError, "Buy price must be greater than zero."
        )

        cost = qty * px
        if cost > self.cash:
            raise InsufficientCashError(
                f"Insufficient cash: need {cost:.2f}, available {self.cash:.2f}."
            )

        self.cash -= cost

        position = portfolio.positions.get(norm_ticker)
        if position is None or position.quantity == 0:
            portfolio.positions[norm_ticker] = Position(norm_ticker, quantity=qty, avg_cost=px)
        else:
            total_qty = position.quantity + qty
            position.avg_cost = ((position.quantity * position.avg_cost) + cost) / total_qty
            position.quantity = total_qty

        trade = {
            "side": "BUY",
            "ticker": norm_ticker,
            "quantity": qty,
            "price": px,
            "total": cost,
        }
        portfolio.trade_history.append(trade)
        return trade

    def sell(self, ticker, quantity, price):
        portfolio = self._require_selected_portfolio()
        norm_ticker = self._require_registered_ticker(ticker)
        qty = self._validate_positive_number(
            quantity, InvalidQuantityError, "Quantity must be greater than zero."
        )
        px = self._validate_non_negative_price(price)

        position = portfolio.positions.get(norm_ticker)
        if position is None or position.quantity < qty:
            available = position.quantity if position is not None else 0.0
            raise InsufficientSharesError(
                f"Insufficient shares for {norm_ticker}: need {qty}, available {available}."
            )

        realized_gain = (px - position.avg_cost) * qty
        proceeds = px * qty

        position.quantity -= qty
        if position.quantity == 0:
            position.avg_cost = 0.0

        self.cash += proceeds
        portfolio.realized_gain += realized_gain

        trade = {
            "side": "SELL",
            "ticker": norm_ticker,
            "quantity": qty,
            "price": px,
            "proceeds": proceeds,
            "realized_gain": realized_gain,
        }
        portfolio.trade_history.append(trade)
        return trade

    def _require_selected_portfolio(self):
        portfolio = self.portfolio_service.selected_portfolio
        if portfolio is None:
            raise NoSelectedPortfolioError("No portfolio is currently selected.")
        return portfolio

    def _require_registered_ticker(self, ticker):
        norm_ticker = ticker.strip().upper()
        if norm_ticker not in self.asset_service.assets:
            raise UnknownTickerError(f"Ticker {norm_ticker} is not registered.")
        return norm_ticker

    @staticmethod
    def _validate_positive_number(value, error_cls, message):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value <= 0
        ):
            raise error_cls(message)
        return float(value)

    @staticmethod
    def _validate_non_negative_price(value):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise InvalidPriceError("Sell price must be finite and zero or greater.")
        return float(value)