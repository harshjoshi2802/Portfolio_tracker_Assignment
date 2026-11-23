import logging
from pathlib import Path
from portfolio_tracker.asset_service import AssetService
from portfolio_tracker.cli import run_cli
from portfolio_tracker.portfolio_service import PortfolioService
from portfolio_tracker.trading_service import TradingService

logger = logging.getLogger("portfolio_tracker")


def _configure_logging(log_path="portfolio_tracker.log"):
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)


def main():
    _configure_logging()
    assets = AssetService()
    portfolios = PortfolioService(assets)
    trading = TradingService(assets, portfolios)
    portfolios.attach_trading_service(trading)

    logger.info("Portfolio Tracker started.")
    run_cli(assets, portfolios, trading, logger=logger)


if __name__ == "__main__":
    main()