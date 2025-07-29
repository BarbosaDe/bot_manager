from typing import Optional

from database import Database
from database.models.models import Application


class ApplicationRepository:
    @staticmethod
    async def insert(name: str, price: float, max_ram: int):
        await Database.write(
            "INSERT INTO applications (name, price, max_ram) VALUES (?, ?, ?)",
            (name, price, max_ram),
        )

    @staticmethod
    async def list(limit: int = 20) -> Optional[list[Application]]:
        rows = await Database.read(
            "SELECT * FROM applications LIMIT ?", (limit,), fetch="all"
        )
        return [Application(**row) for row in rows]
