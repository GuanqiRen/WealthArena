"""Example: Demonstrate the full API workflow.

Register a user → login → create portfolio → place orders → view positions.
Server commands (run from project root):
    PYTHONPATH=. .venv/bin/python -m uvicorn backend.api.main:app --reload
Run from project root:
    PYTHONPATH=. .venv/bin/python examples/api_demo.py
"""

import uuid
from backend.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# ================================================================
# 1. Health Check
# ================================================================
print("=" * 70)
print("1. HEALTH CHECK")
print("=" * 70)
resp = client.get("/health")
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")
print()

# ================================================================
# 2. USER REGISTRATION
# ================================================================
print("=" * 70)
print("2. USER REGISTRATION")
print("=" * 70)
email = "demouser@wealtharena.dev"
password = "Demo1234!"

resp = client.post(
    "/auth/register",
    json={"email": email, "password": password},
)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    user_data = resp.json()
    user_id = user_data["user_id"]
    print(f"✓ Registered user_id: {user_id}")
    print(f"  Email: {user_data['email']}")
else:
    print(f"✗ Error: {resp.json().get('detail', resp.text)}")
    user_id = None
print()

# ================================================================
# 3. USER LOGIN
# ================================================================
print("=" * 70)
print("3. USER LOGIN")
print("=" * 70)
resp = client.post(
    "/auth/login",
    json={"email": email, "password": password},
)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    auth_data = resp.json()
    access_token = auth_data["access_token"]
    print(f"✓ Login successful")
    print(f"  Token (first 40 chars): {access_token[:40]}...")
    print(f"  Type: {auth_data['token_type']}")
    print(f"  Expires in: {auth_data['expires_in']}s")
else:
    print(f"✗ Error: {resp.json().get('detail', resp.text)}")
    access_token = None
print()

# ================================================================
# 4. CREATE PORTFOLIO
# ================================================================
print("=" * 70)
print("4. CREATE PORTFOLIO")
print("=" * 70)
headers = {"Authorization": f"Bearer {access_token}"}
resp = client.post(
    "/portfolios",
    json={"name": f"Demo Portfolio {uuid.uuid4().hex[:8]}"},
    headers=headers,
)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    portfolio = resp.json()
    portfolio_id = portfolio["id"]
    print(f"✓ Portfolio created")
    print(f"  Portfolio ID: {portfolio_id}")
    print(f"  Name: {portfolio['name']}")
    print(f"  User ID: {portfolio['user_id']}")
else:
    print(f"✗ Error: {resp.json().get('detail', resp.text)}")
    portfolio_id = None
print()

# ================================================================
# 5. LIST PORTFOLIOS
# ================================================================
print("=" * 70)
print("5. LIST PORTFOLIOS")
print("=" * 70)
resp = client.get("/portfolios", headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    portfolios = resp.json()
    print(f"✓ Found {len(portfolios)} portfolio(s)")
    for p in portfolios:
        print(f"  — {p['id']}: {p['name']}")
else:
    print(f"✗ Error: {resp.json().get('detail', resp.text)}")
print()

# ================================================================
# 6. PLACE ORDER
# ================================================================
print("=" * 70)
print("6. PLACE ORDER (BUY 10 AAPL)")
print("=" * 70)
if portfolio_id:
    resp = client.post(
        "/trading/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "AAPL",
            "quantity": 10,
            "side": "buy",
        },
        headers=headers,
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        order_result = resp.json()
        print(f"✓ Order placed")
        print(f"  Order ID: {order_result['order']['order_id']}")
        print(f"  Status: {order_result['order']['status']}")
        print(f"  Symbol: {order_result['order']['symbol']}")
        print(f"  Quantity: {order_result['order']['quantity']}")
        if order_result.get("trade"):
            print(f"  Trade ID: {order_result['trade']['trade_id']}")
            print(f"  Execution Price: ${order_result['trade']['execution_price']:.2f}")
        if order_result.get("position"):
            print(f"  Position Qty: {order_result['position']['quantity']}")
            print(f"  Avg Price: ${order_result['position']['average_price']:.2f}")
    else:
        print(f"✗ Error: {resp.json().get('detail', resp.text)}")
else:
    print("Skipped (no portfolio_id)")
print()

# ================================================================
# 7. GET POSITIONS
# ================================================================
print("=" * 70)
print("7. GET POSITIONS")
print("=" * 70)
if portfolio_id:
    resp = client.get(
        f"/trading/positions?portfolio_id={portfolio_id}",
        headers=headers,
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        positions = resp.json()
        print(f"✓ Found {len(positions)} position(s)")
        for pos in positions:
            print(f"  — {pos['symbol']}: {pos['quantity']} @ ${pos['average_price']:.2f}")
    else:
        print(f"✗ Error: {resp.json().get('detail', resp.text)}")
else:
    print("Skipped (no portfolio_id)")
print()

# ================================================================
# 8. GET TRADES
# ================================================================
print("=" * 70)
print("8. GET TRADES")
print("=" * 70)
if portfolio_id:
    resp = client.get(
        f"/trading/trades?portfolio_id={portfolio_id}",
        headers=headers,
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        trades = resp.json()
        print(f"✓ Found {len(trades)} trade(s)")
        for t in trades:
            print(f"  — {t['symbol']}: {t['quantity']} @ ${t['execution_price']:.2f}")
    else:
        print(f"✗ Error: {resp.json().get('detail', resp.text)}")
else:
    print("Skipped (no portfolio_id)")
print()

print("=" * 70)
print("API DEMO COMPLETE")
print("=" * 70)
