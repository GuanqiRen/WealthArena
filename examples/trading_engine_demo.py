from dotenv import load_dotenv

from trading_engine.engine.trading_engine import TradingEngine


load_dotenv()


def main() -> None:
    engine = TradingEngine()

    order_1 = engine.place_order("AAPL", 10, "buy")
    order_2 = engine.place_order("AAPL", 10, "buy")
    order_3 = engine.place_order("AAPL", 5, "sell")

    print("Orders:")
    print(order_1)
    print(order_2)
    print(order_3)

    print("\nPositions:")
    for position in engine.get_positions():
        print(position)

    print("\nTrade History:")
    for trade in engine.get_trade_history():
        print(trade)

    try:
        pnl = engine.get_pnl()
        print(f"\nPnL: {pnl:.2f}")
    except Exception as exc:
        print(f"\nPnL unavailable: {exc}")


if __name__ == "__main__":
    main()
