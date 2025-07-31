from typing import Optional

from database import Database
from database.models.models import Application


class ApplicationRepository:
    @staticmethod
    async def insert(owner: int, app_id: str, app_name: str, ram: int):
        await Database.write(
            "INSERT INTO applications (owner, application_id, name, ram) VALUES (?, ?, ?, ?)",
            (owner, app_id, app_name, ram),
        )

    @staticmethod
    async def delete(app_id: str):
        await Database.write(
            "DELETE FROM applications WHERE application_id == ?", (app_id,)
        )

    @staticmethod
    async def list(owner) -> Optional[list[Application]]:
        rows = await Database.read(
            "SELECT * FROM applications WHERE owner = ?", (owner,), fetch="all"
        )
        return [Application(**row) for row in rows][:25] if rows else None
