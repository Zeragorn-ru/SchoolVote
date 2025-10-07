import os
import asyncio
from typing import Optional
from random import randint

import aiosqlite

from logger import *

class PermissonError(Exception):
    def __init__(self):
        pass

class SchoolUserNotFoundError(Exception):
    def __init__(self):
        pass

class SchoolUserAlreadyLinkedError(Exception):
    def __init__(self):
        pass

class DataBase():
    def __init__(self, db_name: str, admins: list[int] = [5874936084, 5949001476]) -> None:
        self.db_name: str = db_name
        self.connection: Optional[aiosqlite.Connection] = None
        self.admins = admins


    async def init(self) -> None:
        with open(self.db_name, "a"):
                        pass
                    
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
            "CREATE TABLE IF NOT EXISTS candidates (id INTEGER UNIQUE, name TEXT, description TEXT, tg_chanen TEXT, photo TEXT)"
            )
            await db.execute(
            "CREATE TABLE IF NOT EXISTS school_users (id INTEGER UNIQUE, name TEXT, calss TEXT, vote INTEGER, FOREIGN KEY (vote) REFERENCES candidates(id))"
            )
            await db.execute(
            "CREATE TABLE IF NOT EXISTS tg_users (tg_id INTEGER UNIQUE, name TEXT, is_admin BOOL, id INTEGER, FOREIGN KEY (id) REFERENCES school_users(id))"
            )
            await db.commit()
            logging.info("Table [school_users, tg_users, candidates] created successfully")


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


    async def get_users_tg_ids(self) -> list[any]:
        try:
            async with await self._db() as db:
                logging.info("Getting tg_id from tg_users")
                users = await (await db.execute("SELECT tg_id FROM tg_users")).fetchall()
                return users
        except Exception as e:
            logging.error(f"Get users tg_id error: {e}")

    async def get_candidate_by_id(self, id: int) -> list[tuple[any]]:
        try:
            async with await self._db() as db:
                logging.info("Getting candidate by id")
                candidate = await (await db.execute("SELECT * FROM candidates WHERE id = ?", (id,))).fetchall()
                return candidate
        except Exception as e:
            logging.error(f"Get candidate error: {e}")

    async def add_tg_user(self, tg_id: int, name: str) -> None:
        try:
            async with await self._db() as db:

                if tg_id in self.admins:
                    await db.execute('INSERT INTO tg_users (tg_id, name, is_admin) VALUES (?, ?, True)', (tg_id, name))
                    await db.commit()
                    logging.info(f"user {tg_id}@{name} added and made admin")
                    return
                
                await db.execute('INSERT INTO tg_users (tg_id, name) VALUES (?, ?)', (tg_id, name))
                await db.commit()

                logging.info(f"user {tg_id}@{name} added")

        except aiosqlite.IntegrityError:
            logging.error(f"{tg_id}@{name} alredy in database")
            raise
        
        except Exception as e:
            logging.error(f"Add user error: {e}")
            raise

        except Exception as e:
             logging.error(f"Add user {tg_id}@{name} error: {e}")
             raise
        

    async def make_admin(self, tg_id: int) -> None:
        try:
            async with await self._db() as db:
                await db.execute(f"UPDATE tg_users SET is_admin = True WHERE tg_id = {tg_id}")
                logging.info(f"User {tg_id} maked admin")
                await db.commit()
        except Exception as e:
            logging.error(f"Make admin error: {e}")
            raise


    async def is_admin(self, tg_id: int) -> bool:
        try:
            async with await self._db() as db:
                admins = await (await db.execute("SELECT tg_id FROM tg_users WHERE is_admin = 1")).fetchall()
                return (tg_id, ) in admins
            
        except Exception as e:
            logging.error(f"Admin check error: {e}")
    

    async def add_candidate(self, name: str) -> None:
        try:
            async with await self._db() as db:
                await db.execute("INSERT INTO candidates (id, name) VALUES (?, ?)", (randint(100000,999999), name))
                await db.commit()
                logging.info(f"Candidate {name} added")
        except Exception as e:
            logging.error(f"Add candidate error: {e}")

    
    async def add_school_user(self, name: str = "Иванов Иван Иванович", _class: str = "11А") -> None:
        try:
            async with await self._db() as db:
                await db.execute(f"INSERT INTO school_users (id, name, calss) VALUES (?, ?, ?)", (randint(100000,999999), name, _class))
                logging.info(f"User [{name}]@{_class} added")
                await db.commit()
        except Exception as e:
            logging.error(f"Add school user error: {e}")
            raise


    async def link_tg2school(self, tg_id: int, school_id: int) -> None:
        try:
            async with await self._db() as db:
                if await (await db.execute(f"SELECT tg_id FROM tg_users WHERE id = {school_id}")).fetchall() == []:
                    await db.execute("PRAGMA foreign_keys = ON")
                    await db.execute(f"UPDATE tg_users SET id = {school_id} WHERE tg_id = {tg_id}")
                    await db.commit()
                    logging.info(f"link tg[{tg_id}] to school[{school_id}]")
                else:
                    logging.error(f"SchoolUserAlreadyLinkedError tg_id:{tg_id}, school_id:{school_id}")
                    raise SchoolUserAlreadyLinkedError
                
        except aiosqlite.IntegrityError:
            logging.error(f"user {school_id} not found")
            raise SchoolUserNotFoundError

        except Exception as e:
            logging.error(f"Link tg2school error: {e}")
            raise


    async def vote(self, tg_id: int, candidate_id: int) -> None:
        try:
            async with await self._db() as db:
                await db.execute("PRAGMA foreign_keys = ON")
                id = (await (await db.execute(f"SELECT id FROM tg_users WHERE tg_id = {tg_id}")).fetchall())[0][0]
                if not id:
                    logging.error("Not link with school_id")
                    raise PermissionError(f"User {tg_id}, not linked")

                await db.execute(f"UPDATE school_users SET vote = {candidate_id} WHERE id = {id}")
                await db.commit()

        except aiosqlite.IntegrityError:
            logging.error(f"Candidate[{candidate_id}] not found")
            raise

        except Exception as e:
            logging.error(f"Vote error: {e}")
            raise

    
    async def is_linked(self, tg_id: int) -> None:
        try:
            async with await self._db() as db:
                link = await (await db.execute(f"SELECT id FROM tg_users WHERE tg_id = {tg_id}")).fetchall()
                return link != [(None,)]
        except Exception as e:
            logging.error(f"Link check error tg_id: {tg_id}")


    async def get_candidates(self) -> list[tuple[any]]:
        try:
            async with await self._db() as db:
                candidates = await db.execute("SELECT * from candidates")
                return await candidates.fetchall()
        except Exception as e:
            logging.error(f"Get candidates list error: {e}")



async def main():
    db =  DataBase("test.db")


if __name__ == "__main__":
    asyncio.run(main())
