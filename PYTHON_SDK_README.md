"""Python Trading SDK for WealthArena

A production-ready Python client library for interacting with the WealthArena
trading platform API.

## Features

- ✅ Simple, intuitive client interface (`TradingClient`)
- ✅ Automatic JWT token management and authentication
- ✅ Portfolio management (create, list, delete)
- ✅ Trading operations (place orders, view positions, trade history)
- ✅ Type hints and comprehensive docstrings
- ✅ Retry logic with exponential backoff for resilient requests
- ✅ Meaningful error handling with clear exception types
- ✅ Modular design with separated concerns

## Installation

```bash
# Copy the python_sdk directory to your project
cp -r python_sdk /path/to/your/project/

# Import in your code
from python_sdk import TradingClient
```

## Quick Start

```python
from python_sdk import TradingClient

# Initialize client with credentials
client = TradingClient(
    base_url="http://localhost:8000",
    email="user@example.com",
    password="password"
)

# Authenticate
client.login()

# Create a portfolio
portfolio = client.create_portfolio("My Portfolio")

# Place an order
order = client.place_order(
    portfolio_id=portfolio.id,
    symbol="AAPL",
    quantity=10,
    side="buy"
)

# Get positions
positions = client.get_positions(portfolio_id=portfolio.id)
for pos in positions:
    print(f"{pos.symbol}: {pos.quantity} shares @ ${pos.average_price}")

# Get trade history
trades = client.get_trades(portfolio_id=portfolio.id)
```

## Architecture

### Directory Structure

```
python_sdk/
├── __init__.py              # Main exports
├── client.py               # TradingClient (main user interface)
├── auth.py                 # Authentication service & token management
├── models/                 # Data models
│   ├── __init__.py
│   ├── order.py           # Order model
│   ├── position.py        # Position model
│   └── trade.py           # Trade model
├── endpoints/             # API endpoint services
│   ├── __init__.py
│   ├── portfolio.py       # Portfolio operations
│   └── trading.py         # Trading operations
└── utils/                 # Utility modules
    ├── __init__.py
    └── http_client.py     # HTTP client with auth & retry logic
```

### Design Principles

**Separation of Concerns**
- `client.py` - High-level user interface
- `auth.py` - Authentication and token management
- `endpoints/` - Encapsulated API operations
- `utils/http_client.py` - Low-level HTTP communication
- `models/` - Data structures for responses

**Type Safety**
- Full type hints for better IDE support and error detection
- Dataclasses for clean, immutable data models
- Clear return types for all public methods

**Error Handling**
- Meaningful exception types (`TradingClientError`, `AuthError`, `PortfolioError`, `TradingError`)
- Clear error messages with context
- HTTP status codes and details preserved

**Resilience**
- Automatic retry logic with exponential backoff
- Handles transient failures gracefully
- Timeout protection for hung requests

## API Reference

### TradingClient

Main client class for all platform interactions.

#### Initialization

```python
# With email/password
client = TradingClient(
    base_url="http://localhost:8000",
    email="user@example.com",
    password="password"
)

# With existing JWT token
client = TradingClient(
    base_url="http://localhost:8000",
    token="existing-jwt-token"
)
```

#### Authentication

```python
# Register new user
result = client.register("user@example.com", "password")

# Login and obtain token
token = client.login()
# Returns: AuthToken with access_token, user_id, email, expires_in

# Check authentication status
if client.is_authenticated():
    print("Authenticated!")
```

#### Portfolio Operations

```python
# Create portfolio
portfolio = client.create_portfolio("My Portfolio")
# Returns: Portfolio(id, user_id, name, created_at)

# List portfolios
portfolios = client.list_portfolios()
# Returns: List[Portfolio]

# Get specific portfolio
portfolio = client.get_portfolio("portfolio-id")
# Returns: Portfolio

# Delete portfolio
client.delete_portfolio("portfolio-id")
# Returns: bool (True if successful)
```

#### Trading Operations

```python
# Place order
result = client.place_order(
    portfolio_id="portfolio-id",
    symbol="AAPL",
    quantity=10,
    side="buy"  # or "sell"
)
# Returns: dict with order, trade, position, status

# Get positions
positions = client.get_positions(portfolio_id="portfolio-id")
# Returns: List[Position]
# Each Position: symbol, quantity, average_price

# Get trades
trades = client.get_trades(portfolio_id="portfolio-id")
# Returns: List[Trade]
# Each Trade: trade_id, symbol, quantity, execution_price, timestamp_ms

# Get orders
orders = client.get_orders(portfolio_id="portfolio-id")
# Returns: List[Order]
# Each Order: order_id, symbol, quantity, side, status, timestamp_ms
```

## Models

### Portfolio
```python
@dataclass
class Portfolio:
    id: str
    user_id: str
    name: str
    created_at: Optional[str] = None
```

### Order
```python
@dataclass
class Order:
    order_id: str
    symbol: str
    quantity: int
    side: str  # "buy" or "sell"
    status: str
    timestamp_ms: Optional[int] = None
```

### Position
```python
@dataclass
class Position:
    symbol: str
    quantity: int
    average_price: float
```

### Trade
```python
@dataclass
class Trade:
    trade_id: str
    symbol: str
    quantity: int
    execution_price: float
    timestamp_ms: Optional[int] = None
```

### AuthToken
```python
@dataclass
class AuthToken:
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
```

## Error Handling

The SDK provides specific exception types for different failure scenarios:

```python
from python_sdk import TradingClientError, AuthError, PortfolioError, TradingError

try:
    client.login()
except AuthError as e:
    print(f"Authentication failed: {e}")

try:
    portfolio = client.create_portfolio("My Portfolio")
except PortfolioError as e:
    print(f"Portfolio operation failed: {e}")

try:
    order = client.place_order(...)
except TradingError as e:
    print(f"Trading operation failed: {e}")

try:
    # Any operation without authentication
    client.list_portfolios()
except TradingClientError as e:
    print(f"Client error: {e}")
```

## Advanced Usage

### Using Services Directly

For more control, you can use services directly:

```python
from python_sdk.auth import AuthService
from python_sdk.endpoints.portfolio import PortfolioService
from python_sdk.endpoints.trading import TradingService
from python_sdk.utils.http_client import HTTPClient

http_client = HTTPClient("http://localhost:8000")
auth = AuthService(http_client)
portfolios = PortfolioService(http_client)
trading = TradingService(http_client)

# Use services...
token = auth.login("user@example.com", "password")
http_client.set_token(token.access_token)
portfolio_list = portfolios.list_portfolios()
```

### Setting Token Programmatically

```python
# If you have a valid JWT token
client = TradingClient(base_url="http://localhost:8000", token="jwt-token")

# Or set it after initialization
client.http_client.set_token("jwt-token", "Bearer")
```

### Persistent Token Storage

```python
import json

# After successful login, save the token
token = client.login()
with open("token.json", "w") as f:
    json.dump({"token": token.access_token}, f)

# Later, restore the token
with open("token.json", "r") as f:
    data = json.load(f)
    client = TradingClient(
        base_url="http://localhost:8000",
        token=data["token"]
    )
```

## Testing

Run the example script to see the SDK in action:

```bash
cd examples/
python sdk_usage_example.py
```

This requires the backend API to be running on `http://localhost:8000`.

## Configuration

### Base URL

By default, the SDK assumes the API is at `http://localhost:8000`.
Configure it during initialization:

```python
client = TradingClient(
    base_url="https://api.wealtharena.com",
    email="user@example.com",
    password="password"
)
```

### Timeout & Retries

These can be configured when creating the HTTP client directly:

```python
from python_sdk.utils.http_client import HTTPClient

http = HTTPClient(
    base_url="http://localhost:8000",
    timeout=30,           # Request timeout in seconds
    max_retries=5         # Max retry attempts
)
```

## Development

The SDK is built with:
- **Python 3.10+** type hints
- **Dataclasses** for clean models
- **Standard library only** (no external dependencies)
- **urllib** for HTTP requests

This means the SDK has zero external dependencies and can be used in any Python environment.

## Production Readiness

The SDK is production-ready with:
- ✅ Clear error handling and exceptions
- ✅ Automatic retry with exponential backoff
- ✅ Request timeout protection
- ✅ Type hints for IDE support
- ✅ Comprehensive docstrings
- ✅ No external dependencies
- ✅ Clean, maintainable code structure

## License

[Your License Here]
""".strip()  # noqa: ignore long docstring

# This file serves as both documentation and a module docstring
