# Portfolio Tracker CLI

A Python command-line application for managing registered assets and prices, organizing portfolios, executing trades against a shared cash balance, and logging activity to disk.

## Setup and Run Instructions

1. **Navigate to the project root** and verify Python 3 is installed:

   ```bash
   python3 --version
   ```

2. **Run the application** from the project root so package imports resolve cleanly:

   ```bash
   python3 -m main
   ```

   If `main.py` is inside `portfolio_tracker/`, run `python3 -m portfolio_tracker.main` from the project root instead.

3. **Use the menu** to add assets, set prices, create or select portfolios, deposit cash, buy or sell shares, view the selected portfolio, and quit. Activity and rejected actions are written to `portfolio_tracker.log`.

## Modules

* `main.py`: Configures file logging, creates single shared service instances, and starts the CLI loop.
* `portfolio_tracker/cli.py`: Prompts the user for menu actions and inputs, formats output, and catches invalid inputs or domain errors cleanly.
* `portfolio_tracker/asset_service.py`: Registers normalized tickers and asset names while validating and storing current prices.
* `portfolio_tracker/portfolio.py`: Defines `Portfolio` and `Position` state including share quantities, average cost, realized gains, and trade history.
* `portfolio_tracker/portfolio_service.py`: Manages portfolio creation, selection, listing, deletion rules, and the selected portfolio valuation view.
* `portfolio_tracker/trading_service.py`: Holds the shared cash balance and executes buy and sell trades against the active portfolio and asset registry.
* `portfolio_tracker/errors.py`: Defines custom `PortfolioTrackerError` exception subclasses for validation and domain rule violations.

## Design Decisions

1. **Single shared cash pool in `TradingService`**: Keeping cash on `TradingService` rather than duplicating balances per portfolio models a shared account across strategies and prevents split-cash drift.
2. **Explicit wiring between `AssetService`, `PortfolioService`, and `TradingService`**: Requiring `AssetService` and linking `TradingService` with `PortfolioService` ensures trades only use registered tickers, prices stay consistent across views, and portfolio selection changes apply immediately.
3. **Zero starting cash with positive deposit validation**: Starting cash at `0.0` and requiring deposits greater than zero prevents negative starting balances and makes funding explicit.
4. **Weighted-average cost on buys and realized gain retention on sells**: Updating average cost dynamically on buys and adding `(sale price - average cost) * quantity sold` on sells keeps accounting clear and preserves realized gains even after a position is sold down to zero shares.
5. **Domain exceptions plus file logging in the entry loop**: Raising specific `PortfolioTrackerError` subclasses and catching them alongside `ValueError` in the CLI lets invalid inputs or rejected trades log to file and return to the menu without crashing the session.