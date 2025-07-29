from pathlib import Path
from typing import Literal, Optional

import aiosqlite

DATABASE_DIR = Path(__file__).parent
DATABASE_FILE = DATABASE_DIR / "db.sqlite"
DATABASE_SCHEMA = DATABASE_DIR / "schema.sql"


class Database:
    @staticmethod
    async def init_db():
        async with aiosqlite.connect(DATABASE_FILE) as db:
            sql_str = DATABASE_SCHEMA.read_text()
            await db.executescript(sql_str)
            await db.commit()

    @staticmethod
    async def write(query: str, params: tuple) -> None:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            await db.execute(query, params)

            await db.commit()

    @staticmethod
    async def read(
        query: str, params: tuple, fetch: Literal["one", "all"] = "one"
    ) -> Optional[aiosqlite.Row] | list[aiosqlite.Row]:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute(query, params) as cursor:
                if fetch == "one":
                    return await cursor.fetchone()

                elif fetch == "all":
                    return await cursor.fetchall()
