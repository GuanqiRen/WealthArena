"""Utility for creating or dropping the local project schema in Supabase Postgres.

Usage:
    python backend/db/manage_schema.py create
    python backend/db/manage_schema.py drop

Environment:
    Loads variables from .env via python-dotenv.
    Requires one of:
    - DIRECT_URL
    - DATABASE_URL
"""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
SCHEMA_FILE = Path(__file__).resolve().with_name("schema.sql")
DROP_SQL = """
drop table if exists trades cascade;
drop table if exists orders cascade;
drop table if exists positions cascade;
drop table if exists portfolios cascade;
"""


def _get_database_url() -> str:
    import os

    database_url = (
        os.getenv("DIRECT_URL")
        or os.getenv("DATABASE_URL")
    )
    if not database_url:
        raise RuntimeError(
            "Missing database connection string. Set DIRECT_URL or DATABASE_URL in .env."
        )
    return database_url


def _connect(database_url: str):
    try:
        psycopg = importlib.import_module("psycopg")
        connection = psycopg.connect(database_url)
        connection.autocommit = False
        return connection
    except ImportError:
        try:
            psycopg2 = importlib.import_module("psycopg2")
            connection = psycopg2.connect(database_url)
            connection.autocommit = False
            return connection
        except ImportError as exc:
            raise RuntimeError(
                "Missing PostgreSQL driver. Install `psycopg[binary]` or `psycopg2-binary`."
            ) from exc


def create_schema() -> None:
    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    database_url = _get_database_url()

    connection = _connect(database_url)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print(f"Created schema from {SCHEMA_FILE}")


def drop_schema() -> None:
    database_url = _get_database_url()
    connection = _connect(database_url)
    try:
        with connection.cursor() as cursor:
            cursor.execute(DROP_SQL)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print("Dropped tables: trades, orders, positions, portfolios")


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")

    parser = argparse.ArgumentParser(description="Create or drop Supabase schema tables.")
    parser.add_argument("action", choices=["create", "drop"], help="Schema action to perform")
    args = parser.parse_args()

    if args.action == "create":
        create_schema()
        return

    drop_schema()


if __name__ == "__main__":
    main()
