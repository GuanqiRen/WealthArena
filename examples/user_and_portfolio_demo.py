"""Example: register a new user, log in, and create a portfolio.

Run from the project root:
    python examples/user_and_portfolio_demo.py

Requires .env to have:
    SUPABASE_URL
    SUPABASE_PUBLISHABLE_KEY  — used for login
    SUPABASE_SECRET_KEY       — used for admin user creation (bypasses email confirmation)

Registration uses the Admin API so no confirmation email is sent, which means
the demo works immediately without needing to configure Supabase email settings.
"""

import os

from dotenv import load_dotenv

from backend.repositories.user_repository import UserRepository, UserRepositoryError
from backend.services.auth_service import AuthService, AuthError
from backend.services.portfolio_service import PortfolioService

load_dotenv()

# Fixed demo credentials — change these or override via env.
DEMO_EMAIL = os.getenv("DEMO_EMAIL", "demouser@wealtharena.dev")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "Demo1234!")


def main() -> None:
    auth = AuthService()
    user_repo = UserRepository()
    portfolios = PortfolioService()

    email = DEMO_EMAIL
    password = DEMO_PASSWORD

    # ------------------------------------------------------------------ #
    # 1. Register via Admin API (email_confirm=True skips confirmation email)
    # ------------------------------------------------------------------ #
    print(f"Registering {email} ...")
    try:
        new_user = user_repo.create_user(email, password, email_confirm=True)
        print(f"  Registered  — user_id: {new_user['id']}")
    except UserRepositoryError as exc:
        error_str = str(exc)
        if "already been registered" in error_str or "already exists" in error_str or "422" in error_str:
            print("  Already registered — proceeding to login.")
        else:
            print(f"  Registration failed: {exc}")
            return

    # ------------------------------------------------------------------ #
    # 2. Log in
    # ------------------------------------------------------------------ #
    print("\nLogging in ...")
    try:
        token = auth.login_user(email, password)
        print(f"  Logged in   — token_type : {token.token_type}")
        print(f"               expires_in : {token.expires_in}s")
        print(f"               access_token (first 40 chars): {token.access_token[:40]}...")
    except AuthError as exc:
        print(f"  Login failed: {exc}")
        return

    # ------------------------------------------------------------------ #
    # 3. Verify identity from the token
    # ------------------------------------------------------------------ #
    print("\nVerifying token ...")
    try:
        current_user = auth.get_current_user(token.access_token)
        print(f"  Verified    — email   : {current_user.email}")
        print(f"               user_id : {current_user.id}")
    except AuthError as exc:
        print(f"  Token verification failed: {exc}")
        return

    # ------------------------------------------------------------------ #
    # 4. Create a portfolio for that user
    # ------------------------------------------------------------------ #
    print("\nCreating portfolio ...")
    try:
        portfolio = portfolios.create_portfolio(
            user_id=current_user.id,
            name="My Demo Portfolio",
        )
        print(f"  Created     — portfolio_id : {portfolio['id']}")
        print(f"                name         : {portfolio['name']}")
        print(f"                user_id      : {portfolio['user_id']}")
    except Exception as exc:
        print(f"  Portfolio creation failed: {exc}")
        return

    # ------------------------------------------------------------------ #
    # 5. List portfolios for the user
    # ------------------------------------------------------------------ #
    print("\nListing portfolios for user ...")
    user_portfolios = portfolios.get_user_portfolios(current_user.id)
    for p in user_portfolios:
        print(f"  — {p['id']}  |  {p['name']}")


if __name__ == "__main__":
    main()
