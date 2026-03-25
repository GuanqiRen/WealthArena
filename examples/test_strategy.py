from python_sdk import TradingClient, TradingClientError

API_URL = "http://localhost:8000"
USER_EMAIL = 'guanqi.ren@bofa.com'
USER_PASSWORD = 'ready2go'

client = TradingClient(
    base_url=API_URL, 
    email=USER_EMAIL, 
    password=USER_PASSWORD,
)


client.login()
client.list_portfolios()

client.create_portfolio('SPY_BENCHMARK')
client.get_portfolio('SPY_BENCHMARK')

portfolios = client.list_portfolios()
client.place_order(portfolios[0].id, 'SPY', 10, 'buy')

client.create_portfolio('Strategy_1')

portfolio = client.get_portfolio(portfolios[0].id)
