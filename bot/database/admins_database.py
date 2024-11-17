from typing import Optional
import aiosqlite

from core import config

ADMINS_DATABASE = config.ADMINS_DATABASE
TABLE_NAME = "admins"


class AdminsDatabase:

    def __init__(self) -> None:
        self.database_path = ADMINS_DATABASE

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    telegram_id INTEGER
                )
            ''')
            await connection.commit()

    async def add_new_admin(self, telegram_id: int) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                INSERT INTO {TABLE_NAME} (telegram_id)
                VALUES (?)
            ''', (telegram_id,))
            await connection.commit()

    async def get_all_admins_id(self, ) -> Optional[list]:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
            SELECT telegram_id FROM {TABLE_NAME}
            ''') as cursor:
                result = await cursor.fetchall()
                return list(map(lambda x: x[0], result)) if result else None

    async def check_admin_exist(self, telegram_id: int) -> bool:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
                SELECT 1 FROM {TABLE_NAME} WHERE telegram_id = ?
            ''', (telegram_id,)) as cursor:
                return await cursor.fetchone() is not None


admins = AdminsDatabase()
