import os
import asyncio
from typing import Optional

import aiosqlite

from logger import *

roots = [5874936084, 5949001476]

class DataBase():
    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name
        self.connection: Optional[aiosqlite.Connection] = None

    async def init(self):
        with open(self.db_name, "a"):
                        pass
                    
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
            "CREATE TABLE IF NOT EXISTS school_users (id INTEGER UNIQUE, name TEXT, vote INTEGER)"
            )
            await db.execute(
            "CREATE TABLE IF NOT EXISTS tg_users (tg_id INTEGER UNIQUE, name TEXT, is_admin BOOL, id INTEGER, FOREIGN KEY (id) REFERENCES school_users(id))"
            )
            await db.commit()
            logging.info("Table school_users and tg_users created successfully")


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
        
        if self.connection is not None:
            await self.connection.close()
            self.connection = aiosqlite.connect(self.db_name)

        return self.connection

    async def test(self, names: list[str]) -> None:                       
        async with await self._db() as db:
            for name in names:
                await db.execute('INSERT INTO tg_users (name) VALUES (?)', (name,))
                await db.commit()

    async def get_users_tg_id(self) -> list[any]:
        async with await self._db() as db:
            users = await (await db.execute("SELECT tg_id FROM tg_users")).fetchall()
            return users
        
    async def add_tg_user(self, tg_id, name):
         async with await self._db() as db:
            logging.info(f"start additing {name}:{tg_id}")
            if tg_id in roots:
                 await db.execute('INSERT INTO tg_users (tg_id, name, is_admin) VALUES (?, ?, True)', (tg_id, name))
                 await db.commit()
                 return
            await db.execute('INSERT INTO tg_users (tg_id, name) VALUES (?, ?)', (tg_id, name))
            logging.info(f"user {name}:{tg_id} added")
            await db.commit()
        
    async def make_admin(self, tg_id):
         async with await self._db() as db:
              await db.execute(f"UPDATE tg_users SET is_admin = True WHERE tg_id = {tg_id}")
              await db.commit()
    
async def main():
    db =  DataBase("test.db")
    print(await db.add_tg_user(112323, "234"))
    await db.make_admin(112323)

if __name__ == "__main__":
    asyncio.run(main())
