from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal, Optional

import aiosqlite

CREATE_TABLE_TRANSACTIONS = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL UNIQUE,
    payer_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    price TEXT NOT NULL,
    created_at TEXT,
    status TEXT CHECK(status IN ('pending', 'success', 'canceled')) DEFAULT 'pending'
);
"""

CREATE_TABLE_WHITELIST = """
CREATE TABLE IF NOT EXISTS whitelist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('available', 'not available')) DEFAULT 'available',
    created_at TEXT NOT NULL,
    expires_in TEXT NOT NULL
);
"""

QUERYS = (
    CREATE_TABLE_TRANSACTIONS,
    CREATE_TABLE_WHITELIST,
    "CREATE INDEX IF NOT EXISTS idx_transactions_payment_id ON transactions(payment_id)",
    "CREATE INDEX IF NOT EXISTS idx_whitelist_user_id ON whitelist(user_id)",
)


DATABASE_PATH = Path(__file__).parent / "db.sqlite"


class Database:
    @staticmethod
    async def init_db():
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            for query in QUERYS:
                await db.execute(query)

            await db.commit()

    @staticmethod
    async def write(query: str, params: tuple) -> None:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(query, params)

            await db.commit()

    @staticmethod
    async def read(
        query: str, params: tuple, fetch: Literal["one", "all"] = "one"
    ) -> Optional[aiosqlite.Row] | list[aiosqlite.Row]:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute(query, params) as cursor:
                if fetch == "one":
                    return await cursor.fetchone()

                elif fetch == "all":
                    return await cursor.fetchall()


@dataclass(slots=True)
class Transaction:
    id: int
    payment_id: int
    payer_id: int
    server_id: int
    price: float
    created_at: str
    status: str

    @staticmethod
    async def get(payment_id: int) -> "Transaction | None":
        row = await Database.read(
            "SELECT * FROM transactions WHERE payment_id = ?", (payment_id,)
        )

        if row:
            return Transaction(**row)

    @staticmethod
    async def create(
        payment_id: int, payer_id: int, server_id: int, price: float
    ) -> None:
        params = (payment_id, payer_id, server_id, datetime.now(UTC).isoformat(), price)
        await Database.write(
            "INSERT INTO transactions (payment_id, payer_id, server_id, created_at, price) VALUES (?, ?, ?, ?, ?)",
            params,
        )

    @staticmethod
    async def change_status(
        payment_id: int, status: Literal["pending", "success", "canceled"]
    ):
        params = (status, payment_id)

        await Database.write(
            "UPDATE transactions SET status = ? WHERE payment_id = ?", params
        )


@dataclass(slots=True)
class Whitelist:
    id: int
    user_id: int
    status: str
    created_at: str
    expires_in: str

    @staticmethod
    async def get(user_id: int) -> "Whitelist | None":
        row = await Database.read(
            "SELECT * FROM whitelist WHERE user_id = ?", (user_id,)
        )

        if not row:
            return

        now = datetime.now(UTC)
        expires_in = datetime.fromisoformat(row["expires_in"])
        expired = now >= expires_in

        if not expired:
            return Whitelist(**row)

        await Whitelist.change_status(row["user_id"], status="not available")

    @staticmethod
    async def create(user_id: int, expires_in_days: int):
        now = datetime.now(UTC)

        expires_in = now + timedelta(days=expires_in_days)

        params = (user_id, now.isoformat(), expires_in.isoformat())
        await Database.write(
            "INSERT INTO whitelist (user_id, created_at, expires_in) VALUES (?, ?, ?)",
            params,
        )

    @staticmethod
    async def change_status(
        user_id: int, status: Literal["available", "not available"]
    ) -> None:
        await Database.write(
            "UPDATE whitelist SET status = ? WHERE user_id = ?",
            (status, user_id),
        )
