from dotenv import load_dotenv
load_dotenv() 

from market_data.market_data_client import MarketDataClient

client = MarketDataClient()

latest = client.get_latest_price("AAPL")
history = client.get_historical_prices("AAPL", "2026-03-04", "2026-03-11")

print(latest)
print(len(history))