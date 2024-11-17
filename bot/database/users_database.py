from typing import Optional
import aiosqlite

from core import config

CLIENTS_DATABASE = config.CLIENTS_DATABASE
TABLE_NAME = "users"


class UsersDatabase:

    def __init__(self) -> None:
        self.database_path = CLIENTS_DATABASE

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    telegram_id INTEGER
                )
            ''')
            await connection.commit()

    async def add_new_user(self, telegram_id: int) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                INSERT INTO {TABLE_NAME} (telegram_id)
                VALUES (?)
            ''', (telegram_id,))
            await connection.commit()

    async def get_all_users_id(self, ) -> Optional[list]:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
            SELECT telegram_id FROM {TABLE_NAME}
            ''') as cursor:
                result = await cursor.fetchall()
                return list(map(lambda x: x[0], result)) if result else None

    async def check_user_exist(self, telegram_id: int) -> bool:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
                SELECT 1 FROM {TABLE_NAME} WHERE telegram_id = ?
            ''', (telegram_id,)) as cursor:
                return await cursor.fetchone() is not None


users = UsersDatabase()
