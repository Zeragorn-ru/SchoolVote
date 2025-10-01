import os
import asyncio
from typing import Optional

import aiosqlite

from logger import *

class DataBase():
    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name
        self.connection: Optional[aiosqlite.Connection] = None

    async def init(self):
        with open(self.db_name, "a"):
                        pass
                    
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER, name TEXT, is_admin BOOL, vote INTEGER)"
            )
            await db.commit()
            logging.info("Table 'users' created successfully")


    async def _db(self) -> aiosqlite.Connection:
        if self.connection is None:
            try:
                if not os.path.exists(self.db_name):
                    await self.init()
                
                self.connection = aiosqlite.connect(self.db_name)
                logging.info("Successful connection to the database")

            except Exception as e:
                logging.critical(f"Database connect error: {e}")
                raise
        return self.connection

    async def test(self, names: list[str]) -> None:                       
        async with await self._db() as db:
            for name in names:
                await db.execute('INSERT INTO users (name) VALUES (?)', (name,))
                await db.commit()

    async def get_users(self) -> list[any]:
        async with await self._db() as db:
            users = await db.execute("SELECT * FROM users")
            return await users.fetchall()
        
    
async def main():
    db =  DataBase("test.db")
    await db.test1()

if __name__ == "__main__":
    asyncio.run(main())
