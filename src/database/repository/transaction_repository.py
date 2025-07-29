from datetime import UTC, datetime
from typing import Optional

from database import Database
from database.models import Transaction
from database.models.models import Plan


class TransactionRepository:
    @staticmethod
    async def get(payment_id: int) -> Optional[Transaction]:
        row = await Database.read(
            "SELECT * FROM transactions WHERE payment_id = ?", (payment_id,)
        )

        if row:
            return Transaction(**row)

    @staticmethod
    async def insert(transaction: Transaction):
        now = datetime.now(UTC).isoformat()

        await Database.write(
            """INSERT INTO transactions 
                (payment_id, payer_id, server_id, price, plan, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                transaction.payment_id,
                transaction.payer_id,
                transaction.server_id,
                transaction.price,
                transaction.plan,
                now,
            ),
        )

    @staticmethod
    async def change_status(transaction: Transaction):
        await Database.write(
            "UPDATE transactions SET status = ? WHERE id = ?",
            (transaction.status, transaction.id),
        )

    async def delete(plan: Plan):
        await Database.write("DELETE FROM plans WHERE id = ?", (plan.id,))

    @staticmethod
    async def list(limit: int = 20) -> Optional[list[Plan]]:
        rows = await Database.read("SELECT * FROM plans", (), fetch="all")

        return (Plan(**row) for row in rows)
