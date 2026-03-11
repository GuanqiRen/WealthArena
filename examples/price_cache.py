from dotenv import load_dotenv
load_dotenv() 

from market_data.cache.price_cache import PriceCache

# Uses market_data/config/price_cache_config.yaml by default (expiry_seconds: 5)
cache = PriceCache()

symbol = "AAPL"

# First call fetches from MarketDataClient (and then stores in cache)
price_1 = cache.get_price(symbol)
print(f"First call: {symbol} -> {price_1}")

# Second call within expiry window returns cached value (no new API call)
price_2 = cache.get_price(symbol)
print(f"Second call (cached): {symbol} -> {price_2}")