from .errors import PortfolioTrackerError


def run_cli(assets, portfolios, trading, logger=None):
    print("Welcome to Portfolio Tracker.")

    while True:
        print("\n1. Add asset        2. List assets       3. Set price")
        print("4. Create portfolio 5. List portfolios   6. Select portfolio")
        print("7. Delete portfolio 8. View selected    9. Deposit cash")
        print("10. Cash balance   11. Buy             12. Sell")
        print("0. Quit")

        choice = input("Select an option: ").strip()
        if choice == "0":
            if logger:
                logger.info("Portfolio Tracker exited.")
            print("Goodbye.")
            break

        try:
            if choice == "1":
                asset = assets.add_asset(input("Ticker: "), input("Name: "))
                if logger:
                    logger.info("Added asset %s (%s)", asset.ticker, asset.name)
                print(f"Added {asset.ticker} ({asset.name}).")
            elif choice == "2":
                rows = assets.list_assets()
                if logger:
                    logger.info("Listed %d assets", len(rows))
                for ticker, name, price in rows:
                    print(f"{ticker} | {name} | {price}")
            elif choice == "3":
                ticker = input("Ticker: ")
                price = float(input("Price: "))
                assets.set_price(ticker, price)
                norm = ticker.strip().upper()
                if logger:
                    logger.info("Set price for %s to %.2f", norm, float(price))
                print("Price updated.")
            elif choice == "4":
                p = portfolios.create_portfolio(input("Name: "), input("Strategy: "))
                if logger:
                    logger.info("Created portfolio '%s' (%s)", p.name, p.strategy)
                print(f"Created portfolio '{p.name}'.")
            elif choice == "5":
                rows = portfolios.list_portfolios()
                if logger:
                    logger.info("Listed %d portfolios", len(rows))
                for name, strategy, selected in rows:
                    mark = " (selected)" if selected else ""
                    print(f"{name} | {strategy}{mark}")
            elif choice == "6":
                p = portfolios.get_portfolio(input("Name: "))
                if logger:
                    logger.info("Selected portfolio '%s'", p.name)
                print(f"Selected '{p.name}'.")
            elif choice == "7":
                name = input("Name: ")
                portfolios.delete_portfolio(name)
                if logger:
                    logger.info("Deleted portfolio '%s'", name)
                print(f"Deleted '{name}'.")
            elif choice == "8":
                view = portfolios.get_selected_portfolio_view()
                if logger:
                    logger.info("Viewed selected portfolio '%s'", view["name"])
                print(f"\nPortfolio: {view['name']} ({view['strategy']})")
                print(f"Cash: {view['cash']:.2f}")
                for h in view["holdings"]:
                    print(
                        f"  {h['ticker']}: qty={h['quantity']}, avg={h['avg_cost']:.2f}, "
                        f"price={h['current_price']}, mv={h['market_value']}, "
                        f"unrealized={h['unrealized_gain']}"
                    )
                label = view.get("totals_label", "all holdings")
                print(f"Market value ({label}): {view['total_market_value']:.2f}")
                print(f"Unrealized gain ({label}): {view['total_unrealized_gain']:.2f}")
                print(f"Realized gain: {view['realized_gain']:.2f}")
            elif choice == "9":
                amount = float(input("Amount: "))
                bal = trading.deposit_cash(amount)
                if logger:
                    logger.info("Deposited %.2f; cash balance now %.2f", amount, bal)
                print(f"Cash balance: {bal:.2f}")
            elif choice == "10":
                bal = trading.get_cash()
                if logger:
                    logger.info("Checked cash balance: %.2f", bal)
                print(f"Cash balance: {bal:.2f}")
            elif choice == "11":
                trade = trading.buy(
                    input("Ticker: "),
                    float(input("Quantity: ")),
                    float(input("Price: ")),
                )
                if logger:
                    logger.info(
                        "BUY %s qty=%s @ %.2f (cash=%.2f)",
                        trade["ticker"],
                        trade["quantity"],
                        trade["price"],
                        trading.get_cash(),
                    )
                print(f"Bought {trade['quantity']} {trade['ticker']} @ {trade['price']:.2f}.")
            elif choice == "12":
                trade = trading.sell(
                    input("Ticker: "),
                    float(input("Quantity: ")),
                    float(input("Price: ")),
                )
                if logger:
                    logger.info(
                        "SELL %s qty=%s @ %.2f realized_gain=%.2f (cash=%.2f)",
                        trade["ticker"],
                        trade["quantity"],
                        trade["price"],
                        trade["realized_gain"],
                        trading.get_cash(),
                    )
                print(
                    f"Sold {trade['quantity']} {trade['ticker']} @ {trade['price']:.2f} "
                    f"(realized gain: {trade['realized_gain']:.2f})."
                )
            else:
                if logger:
                    logger.warning("Rejected invalid menu choice: '%s'", choice)
                print("Invalid option.")
        except ValueError as err:
            if logger:
                logger.warning("Rejected invalid numeric input on option %s: %s", choice, err)
            print("Please enter a valid number.")
        except PortfolioTrackerError as err:
            if logger:
                logger.warning("Rejected request on option %s: %s", choice, err)
            print(f"Error: {err}")