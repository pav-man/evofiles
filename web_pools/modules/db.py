import aiosqlite
from web_pools.modules import config
import logging.config

logging.config.dictConfig(config.LOGGING)
logs = logging.getLogger("aioserver")


async def init_db(app):
    db_conn = await aiosqlite.connect(app['config'].db)
    await db_conn.execute("PRAGMA foreign_keys = 1")
    await create_tables(db_conn)
    app['db_conn'] = db_conn
    return db_conn


async def close_db(app):
    await app['db_conn'].close()


async def create_tables(db_conn):
    table_files = "CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, " \
            "size INTEGER NOT NULL, path TEXT NOT NULL, expiry_dt INTEGER NOT NULL, insert_dt INTEGER NOT NULL);"
    table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE" \
                  ", password TEXT NOT NULL, insert_dt TEXT DEFAULT CURRENT_TIMESTAMP);"
    table_user_files = "CREATE TABLE IF NOT EXISTS user_files (" \
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                       "user_id INTEGER NOT NULL, " \
                       "file_id INTEGER NOT NULL, " \
                       "FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE, " \
                       "FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE )"
    await db_conn.execute(table_files)
    await db_conn.execute(table_users)
    await db_conn.execute(table_user_files)


async def insert_file(db_conn, filename, size, path, expiry):
    q = f"INSERT INTO files (name, size, path, expiry_dt, insert_dt) VALUES " \
        f"('{filename}', {size}, '{path}', strftime('%s','now') + {expiry}, strftime('%s','now'))"
    cursor = await db_conn.execute(q)
    lastrowid = cursor.lastrowid
    await db_conn.commit()
    return lastrowid


async def select_file(db_conn, path):
    q = f"SELECT id, name, size, path, expiry_dt -  strftime('%s','now'), datetime(insert_dt,'unixepoch') FROM files WHERE path = '{path}' AND expiry_dt > strftime('%s','now')"
    cursor = await db_conn.execute(q)
    row = await cursor.fetchone()
    return row


async def select_files(db_conn, filename):
    q = f"SELECT id, name, size, path, expiry_dt -  strftime('%s','now'), datetime(insert_dt,'unixepoch') FROM files WHERE name LIKE '%{filename}%' AND expiry_dt > strftime('%s','now')"
    cursor = await db_conn.execute(q)
    rows = await cursor.fetchall()
    return rows


async def add_user(db_conn, login, password_hash):
    q = f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}')"
    try:
        await db_conn.execute(q)
        await db_conn.commit()
        return True
    except aiosqlite.IntegrityError as err:
        return False


async def get_user_by_login(db_conn, login):
    q = f"SELECT login, password FROM users WHERE login = '{login}'"
    cursor = await db_conn.execute(q)
    row = await cursor.fetchone()
    return row


async def add_file_to_user(db_conn, username, file_id):
    q = f"INSERT INTO user_files SELECT NULL id, id user_id, {file_id} file_id FROM users WHERE login='{username}';"
    await db_conn.execute(q)
    await db_conn.commit()
    return


async def user_files(db_conn, username):
    q = f"SELECT t3.id, t3.name, t3.size, t3.path, t3.expiry_dt -  strftime('%s','now'), datetime(t3.insert_dt,'unixepoch') FROM user_files t1 " \
        f"LEFT JOIN users t2 ON t1.user_id = t2.id " \
        f"LEFT JOIN files t3 ON t1.file_id = t3.id " \
        f" WHERE t2.login = '{username}' AND t3.expiry_dt > strftime('%s','now')"
    cursor = await db_conn.execute(q)
    rows = await cursor.fetchall()
    return rows

async def select_expire_files(db_conn):
    q = f"SELECT id, name, path FROM files WHERE expiry_dt <= strftime('%s','now')"
    cursor = await db_conn.execute(q)
    rows = await cursor.fetchall()
    return rows

async def delete_expire_files(db_conn, ids):
    q = f"DELETE FROM files WHERE id IN ({ids})"
    await db_conn.execute(q)
    await db_conn.commit()