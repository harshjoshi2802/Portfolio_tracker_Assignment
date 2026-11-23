from .errors import (
    DuplicatePortfolioError,
    UnknownPortfolioError,
    PortfolioHasSharesError,
    NoSelectedPortfolioError,
)
from .portfolio import Portfolio


class PortfolioService:
    def __init__(self, asset_service, trading_service=None):
        if asset_service is None:
            raise ValueError("asset_service is required.")
        self.portfolios = {}
        self.selected_portfolio = None
        self.asset_service = asset_service
        self.trading_service = trading_service

    def attach_trading_service(self, trading_service):
        self.trading_service = trading_service

    def create_portfolio(self, name, strategy):
        if name in self.portfolios:
            raise DuplicatePortfolioError(f"Portfolio with name {name} already exists")

        portfolio = Portfolio(name, strategy)
        self.portfolios[name] = portfolio
        return portfolio

    def get_portfolio(self, name):
        if name not in self.portfolios:
            raise UnknownPortfolioError(f"Portfolio with name {name} does not exist")

        self.selected_portfolio = self.portfolios[name]
        return self.selected_portfolio

    def list_portfolios(self):
        results = []
        for portfolio in self.portfolios.values():
            is_selected = portfolio is self.selected_portfolio
            results.append((portfolio.name, portfolio.strategy, is_selected))
        return results

    def delete_portfolio(self, name):
        if name not in self.portfolios:
            raise UnknownPortfolioError(f"Portfolio with name {name} does not exist")

        portfolio = self.portfolios[name]
        if any(position.quantity > 0 for position in portfolio.positions.values()):
            raise PortfolioHasSharesError(
                f"Cannot delete portfolio with name {name} because it has shares."
            )

        del self.portfolios[name]
        if portfolio is self.selected_portfolio:
            self.selected_portfolio = None

    def get_selected_portfolio_view(self):
        if self.selected_portfolio is None:
            raise NoSelectedPortfolioError("No portfolio is currently selected.")
        portfolio = self.selected_portfolio

        holdings = []
        total_market_value = 0.0
        total_unrealized_gain = 0.0
        active_holdings_count = 0
        priced_holdings_count = 0

        for ticker, position in portfolio.positions.items():
            if position.quantity <= 0:
                continue

            active_holdings_count += 1
            current_price = self.asset_service.prices.get(ticker)

            if current_price is None:
                market_value = None
                unrealized_gain = None
            else:
                priced_holdings_count += 1
                market_value = position.quantity * current_price
                unrealized_gain = (current_price - position.avg_cost) * position.quantity
                total_market_value += market_value
                total_unrealized_gain += unrealized_gain

            holdings.append(
                {
                    "ticker": ticker,
                    "quantity": position.quantity,
                    "avg_cost": position.avg_cost,
                    "current_price": current_price,
                    "market_value": market_value,
                    "unrealized_gain": unrealized_gain,
                }
            )

        if active_holdings_count == 0:
            totals_label = "all holdings"
            displayed_market_value = 0.0
            displayed_unrealized_gain = 0.0
        elif priced_holdings_count == active_holdings_count:
            totals_label = "all holdings"
            displayed_market_value = total_market_value
            displayed_unrealized_gain = total_unrealized_gain
        elif priced_holdings_count > 0:
            totals_label = "priced holdings only"
            displayed_market_value = total_market_value
            displayed_unrealized_gain = total_unrealized_gain
        else:
            totals_label = "priced holdings only"
            displayed_market_value = 0.0
            displayed_unrealized_gain = 0.0

        cash_balance = self.trading_service.cash if self.trading_service is not None else 0.0

        return {
            "name": portfolio.name,
            "strategy": portfolio.strategy,
            "cash": cash_balance,
            "holdings": holdings,
            "totals_label": totals_label,
            "total_market_value": displayed_market_value,
            "total_unrealized_gain": displayed_unrealized_gain,
            "realized_gain": portfolio.realized_gain,
        }