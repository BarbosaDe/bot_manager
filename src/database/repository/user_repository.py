from datetime import UTC, datetime, timedelta
from sqlite3 import IntegrityError
from typing import Optional

from database import Database
from database.models.models import Plan, User
from utils.logger import logger


class UserRepository:
    @staticmethod
    async def get(user_id: int) -> Optional[User]:
        row = await Database.read(
            """SELECT 
                users.id AS user_row_id,
                users.user_id AS user_id,
                users.created_at AS user_created_at,
                users.expires_at AS user_expires_at,
                
                plans.id AS plan_id,
                plans.name AS plan_name,
                plans.price AS plan_price,
                plans.max_ram AS plan_max_ram

                FROM users
                LEFT JOIN plans ON users.plan_id = plans.id;
            """,
            (user_id,),
        )

        if not row:
            return

        plan = Plan(
            plan_id=row["plan_id"],
            plan_name=row["plan_name"],
            plan_price=row["plan_price"],
            plan_max_ram=row["plan_max_ram"],
        )

        return User(
            row_id=row["user_row_id"],
            user_id=row["user_id"],
            created_at=row["user_created_at"],
            expires_at=row["user_expires_at"],
            plan=plan,
        )

    @staticmethod
    async def update(user: User, expires_in_days: int = 30):
        now = datetime.now(UTC)

        expires_at = now + timedelta(expires_in_days)

        await Database.write(
            "UPDATE users SET plan_id = ?, created_at = ?, expires_at = ? WHERE user_id = ?",
            (user.plan.id, now, expires_at, user.user_id),
        )

    @staticmethod
    async def insert(user: User, expires_in_days: int = 30) -> None:
        now = datetime.now(UTC)

        expires_at = now + timedelta(expires_in_days)

        try:
            await Database.write(
                "INSERT INTO users (user_id, plan_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (user.user_id, user.plan.id, now.isoformat(), expires_at),
            )

        except IntegrityError as e:
            if "UNIQUE" in str(e):
                return await UserRepository.update(user)

            logger.critical("Erro de integridade inesperado", exc_info=True)
