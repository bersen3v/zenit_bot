import csv
import io
from datetime import datetime
from time import strftime
from typing import Optional
import aiosqlite

from core import config
from database.clients_telegram_database import clients_telegram
from database.clients_telegram_database import TABLE_NAME as TELEGRAM_TABLE_NAME

CLIENTS_DATABASE = config.CLIENTS_DATABASE
TABLE_NAME = "clients"


class ClientsDatabase:

    def __init__(self) -> None:
        self.database_path = CLIENTS_DATABASE

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    client_number INTEGER,
                    name TEXT,
                    gender TEXT,
                    date_of_birth TEXT )
            ''')

            await connection.execute(f'''
                CREATE INDEX IF NOT EXISTS idx_clients_client_number ON {TABLE_NAME}(client_number)
            ''')

            await connection.commit()

    async def update_table(self, csvfile: io.BytesIO) -> None:
        try:
            # удаление старой таблицы
            async with aiosqlite.connect(self.database_path) as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f'DELETE FROM {TABLE_NAME}')
                    # инициализация нужных переменных
                    reader = csv.reader(io.TextIOWrapper(csvfile, encoding='utf-8'))  # итератор файла
                    next(reader)  # пропускаем заголовок таблицы
                    # экземпляр для работы с тг таблицей клиентов
                    # заполнение таблицы и валидация меток
                    for row in reader:
                        client_number, name, gender, date_of_birth, mark, appendix = row
                        if mark:
                            if await clients_telegram.check_client_exist_by_number(client_number):
                                await clients_telegram.remove_client(client_number, cursor)
                            continue
                        await cursor.execute(f'''
                            INSERT INTO {TABLE_NAME} (client_number, name, gender, date_of_birth)
                            VALUES (?, ?, ?, ?)
                        ''', (client_number, name, gender, date_of_birth))
                await connection.commit()

        except Exception as e:
            raise Exception(f"Ошибка при обновлении базы данных: {e}")

    async def get_clients_number_with_birthday(self) -> tuple:
        today = datetime.now().strftime('%d/%m')
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"""
                SELECT c.telegram_id
                FROM {TELEGRAM_TABLE_NAME} c
                JOIN  {TABLE_NAME} t
                ON t.client_number = c.client_number
                WHERE SUBSTR(t.date_of_birth, 1, 5) = ?
                """, (today,))
                results = await cursor.fetchall()
                return tuple(map(lambda x: x[0], results))

    async def get_user_data_by_id(self, telegram_id: int) -> Optional[dict]:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
            SELECT t.name, t.gender, t.date_of_birth
            FROM {TABLE_NAME} t
            JOIN clients_telegram c
            ON t.client_number = c.client_number
            WHERE c.telegram_id = ?
            ''', (telegram_id,)) as cursor:
                key_list = ["name", "gender", "date_of_birth"]
                result = {key: value for key, value in zip(key_list, await cursor.fetchone())}
                return result if result else None

    async def check_client_exist(self, client_number: int) -> bool:
        async with aiosqlite.connect(self.database_path) as connection:
            async with connection.execute(f'''
                SELECT 1 FROM {TABLE_NAME} WHERE client_number = ?
            ''', (client_number,)) as cursor:
                return await cursor.fetchone() is not None


clients = ClientsDatabase()
