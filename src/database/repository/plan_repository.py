from sqlite3 import IntegrityError
from typing import Optional

from database import Database
from database.models.models import Plan
from exceptions import DuplicateEntryError
from utils.logger import logger


class PlanRepository:
    @staticmethod
    async def get(plan_id: int) -> Optional[Plan]:
        row = await Database.read("SELECT * FROM plans WHERE id = ?", (plan_id,))

        if row:
            return Plan(**row)

    @staticmethod
    async def insert(name: str, price: float, max_ram: int):
        try:
            await Database.write(
                "INSERT INTO plans (name, price, max_ram) VALUES (?, ?, ?)",
                (name, price, max_ram),
            )

        except IntegrityError as e:
            if "UNIQUE" in str(e):
                raise DuplicateEntryError("Já existe um plano com esse nome")

            logger.critical("Erro de integridade inesperado", exc_info=True)

    @staticmethod
    async def update(old: Plan, new: Plan):
        try:
            await Database.write(
                "UPDATE plans SET name = ?, price = ?, max_ram = ? WHERE id = ?",
                (new.name, new.price, new.max_ram, old.id),
            )

        except IntegrityError as e:
            if "UNIQUE" in str(e):
                raise DuplicateEntryError("Já existe um plano com esse nome")

            logger.critical("Erro de integridade inesperado", exc_info=True)

    async def delete(plan: Plan):
        await Database.write("DELETE FROM plans WHERE id = ?", (plan.id,))

    @staticmethod
    async def list(limit: int = 20) -> Optional[list[Plan]]:
        rows = await Database.read("SELECT * FROM plans", (), fetch="all")

        return (Plan(**row) for row in rows)
