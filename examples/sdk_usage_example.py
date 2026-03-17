"""Example usage of the WealthArena Python Trading SDK.

This script demonstrates how to use the TradingClient to:
- Register and login
- Create and manage portfolios
- Place orders
- View positions and trades

Environment Variables (set in .env):
    API_URL: Base URL of the backend API (default: http://localhost:8000)
    USER_EMAIL: Email for authentication
    USER_PASSWORD: Password for authentication
    API_TOKEN: Existing JWT token (optional, alternative to email/password)
"""

import os
from dotenv import load_dotenv

from python_sdk import TradingClient, TradingClientError

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000")
USER_EMAIL = os.getenv("USER_EMAIL", "demouser@wealtharena.dev")
USER_PASSWORD = os.getenv("USER_PASSWORD", "Demo1234!")
API_TOKEN = os.getenv("API_TOKEN")  # Optional


def example_basic_usage():
    """Basic usage example: register, login, create portfolio, place order."""
    print("=" * 60)
    print("BASIC USAGE EXAMPLE")
    print("=" * 60)

    # Initialize client with environment variables
    client = TradingClient(
        base_url=API_URL,
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )
    '''
    # Register (if new user)
    print(f"\n[1] Registering new user {USER_EMAIL}")
    try:
        result = client.register(USER_EMAIL, USER_PASSWORD)
        print(f"✓ Registered: {result}")
    except TradingClientError as e:
        print(f"⚠ Registration failed (user may already exist): {e}")
    '''
    # Login
    print(f"\n[2] Logging in as {USER_EMAIL}...")
    try:
        token = client.login()
        print(f"✓ Logged in. User ID: {token.user_id}, Email: {token.email}")
    except TradingClientError as e:
        print(f"✗ Login failed: {e}")
        print("   Hint: Ensure the backend API is running and Supabase credentials are configured.")
        print("   Set SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY environment variables.")
        return

    # Create portfolio
    portfolio = None
    print("\n[3] Creating portfolio...")
    try:
        portfolio = client.create_portfolio("My Trading Portfolio")
        print(f"✓ Created portfolio: {portfolio.name} (ID: {portfolio.id})")
    except TradingClientError as e:
        print(f"✗ Portfolio creation failed: {e}")

    # List portfolios
    print("\n[4] Listing portfolios...")
    try:
        portfolios = client.list_portfolios()
        print(f"✓ Found {len(portfolios)} portfolio(s):")
        for p in portfolios:
            print(f"  - {p.name} (ID: {p.id})")
    except TradingClientError as e:
        print(f"✗ Failed to list portfolios: {e}")

    # Skip remaining operations if portfolio creation failed
    if not portfolio:
        print("\n⚠ Skipping order operations (no portfolio available)")
        return

    # Place order
    print(f"\n[5] Placing order in {portfolio.name}...")
    try:
        order_result = client.place_order(
            portfolio_id=portfolio.id,
            symbol="AAPL",
            quantity=10,
            side="buy",
        )
        print(f"✓ Order placed:")
        print(f"  Order ID: {order_result.get('order', {}).get('order_id')}")
        print(f"  Status: {order_result.get('status')}")
        if order_result.get("trade"):
            print(f"  Trade executed: {order_result['trade'].get('quantity')} shares @ "
                  f"${order_result['trade'].get('execution_price')}")
    except TradingClientError as e:
        print(f"✗ Order placement failed: {e}")

    # Get positions
    print(f"\n[6] Getting positions in {portfolio.name}...")
    try:
        positions = client.get_positions(portfolio_id=portfolio.id)
        print(f"✓ Found {len(positions)} position(s):")
        for pos in positions:
            print(f"  - {pos.symbol}: {pos.quantity} shares @ ${pos.average_price}")
    except TradingClientError as e:
        print(f"✗ Failed to get positions: {e}")

    # Get trades
    print(f"\n[7] Getting trade history...")
    try:
        trades = client.get_trades(portfolio_id=portfolio.id)
        print(f"✓ Found {len(trades)} trade(s):")
        for trade in trades:
            print(f"  - {trade.symbol}: {trade.quantity} shares @ ${trade.execution_price}")
    except TradingClientError as e:
        print(f"✗ Failed to get trades: {e}")

    # Get orders
    print(f"\n[8] Getting order history...")
    try:
        orders = client.get_orders(portfolio_id=portfolio.id)
        print(f"✓ Found {len(orders)} order(s):")
        for order in orders:
            print(f"  - {order.symbol}: {order.quantity} shares ({order.side.upper()}) - {order.status}")
    except TradingClientError as e:
        print(f"✗ Failed to get orders: {e}")

    # Clean up: delete portfolio
    print(f"\n[9] Deleting portfolio...")
    try:
        client.delete_portfolio(portfolio.id)
        print(f"✓ Portfolio deleted")
    except TradingClientError as e:
        print(f"✗ Portfolio deletion failed: {e}")


def example_with_existing_token():
    """Example: initialize client with existing JWT token."""
    print("\n" + "=" * 60)
    print("USING EXISTING TOKEN")
    print("=" * 60)

    # If API_TOKEN is set in .env, use it directly
    if not API_TOKEN:
        print("⚠ API_TOKEN not set in environment variables")
        print("  Set API_TOKEN in .env to use this example")
        return

    client = TradingClient(
        base_url=API_URL,
        token=API_TOKEN,
    )

    print(f"Authenticated: {client.is_authenticated()}")
    try:
        portfolios = client.list_portfolios()
        print(f"✓ Listed {len(portfolios)} portfolio(s) using existing token")
    except TradingClientError as e:
        print(f"✗ Failed: {e}")


def example_error_handling():
    """Example: proper error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING EXAMPLE")
    print("=" * 60)

    client = TradingClient(
        base_url=API_URL,
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    # Error 1: Trying to list portfolios without authentication
    print("\n[1] Attempting operation without login...")
    try:
        portfolios = client.list_portfolios()
    except TradingClientError as e:
        print(f"✓ Expected error caught: {e}")

    # Error 2: Invalid order (side)
    print("\n[2] Attempting order with invalid side...")
    try:
        client.login()
        portfolio = client.create_portfolio("Test")
        client.place_order(
            portfolio_id=portfolio.id,
            symbol="AAPL",
            quantity=10,
            side="invalid",  # Invalid side
        )
    except TradingClientError as e:
        print(f"✓ Expected error caught: {e}")
    except Exception as e:
        print(f"⚠ Operation failed (expected if API unavailable): {type(e).__name__}")

    # Error 3: Invalid quantity
    print("\n[3] Attempting order with invalid quantity...")
    try:
        # Use the portfolio from previous try block (may not exist)
        if 'portfolio' in locals():
            client.place_order(
                portfolio_id=portfolio.id,
                symbol="AAPL",
                quantity=-5,  # Invalid quantity
                side="buy",
            )
        else:
            raise TradingClientError("Portfolio not available (previous step failed)")
    except TradingClientError as e:
        print(f"✓ Expected error caught: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WealthArena Python SDK - Usage Examples")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  API URL: {API_URL}")
    print(f"  User Email: {USER_EMAIL}")
    print(f"  User Password: {'*' * len(USER_PASSWORD) if USER_PASSWORD else 'NOT SET'}")
    print(f"  API Token: {'SET' if API_TOKEN else 'NOT SET'}")

    # Run examples
    # Uncomment to run. Requires running backend server and .env configuration.
    example_basic_usage()
    # example_with_existing_token()
    # example_error_handling()

    print("\n" + "=" * 60)
    print("Configuration: Create a .env file with:")
    print("=" * 60)
    print("""
API_URL=http://localhost:8000
USER_EMAIL=your_email@example.com
USER_PASSWORD=your_password
API_TOKEN=your_jwt_token_optional
""")
    print("Then run this script to use the configured values.")
    print("=" * 60)
