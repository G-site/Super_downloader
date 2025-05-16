import sqlite3


def data_create():
    with sqlite3.connect("database.db") as db:
        query = """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER(20) NOT NULL,
            username VARCHAR(100) DEFAULT "Пользователь не имеет Username",
            name VARCHAR(100),
            balance INTEGER DEFAULT 0,
            lang TEXT DEFAULT "ru",
            status TEXT NOT NULL DEFAULT 'User'
        )
        """
        db.executescript(query)


def admin_create():
    with sqlite3.connect("database.db") as db:
        query = """
            CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER(20) NOT NULL,
            username VARCHAR(100) DEFAULT "Пользователь не имеет Username",
            name VARCHAR(100),
            range INTEGER DEFAULT 0
        )
        """
        db.executescript(query)


def check_admin(tg_id):
    admin_status = True
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT tg_id FROM admins WHERE tg_id = ?""", [tg_id])
    admin = cursor.fetchone()
    if admin is None:
        admin_status = False
    cursor.execute("""SELECT range FROM admins WHERE tg_id = ?""", [tg_id])
    range = cursor.fetchone()
    range = range[0] if range else 0
    db.commit()
    cursor.close()
    db.close()
    return admin_status, range


def set_user(tg_id, username, first_name):
    db = sqlite3.connect("database.db")
    res = False
    cursor = db.cursor()
    cursor.execute("""SELECT tg_id FROM users WHERE tg_id = ?""", [tg_id])
    if cursor.fetchone() is None:
        cursor.execute("""INSERT INTO users (tg_id, username, name) VALUES (?, ?, ?)""", (tg_id, username, first_name))
        db.commit()
        res = True
    cursor.close()
    db.close()
    return res


def check_user(tg_id, username, first_name):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT tg_id FROM users WHERE tg_id = ?""", [tg_id])
    if cursor.fetchone() is None:
        cursor.execute("""INSERT INTO users (tg_id, username, name) VALUES (?, ?, ?)""", (tg_id, username, first_name))
    cursor.execute("""SELECT name FROM users WHERE tg_id = ?""", [tg_id])
    name = cursor.fetchone()
    cursor.execute("""SELECT balance FROM users WHERE tg_id = ?""", [tg_id])
    balance = cursor.fetchone()
    cursor.execute("""SELECT status FROM users WHERE tg_id = ?""", [tg_id])
    status = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return name, balance, status


def download_user(tg_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT balance FROM users WHERE tg_id = ?""", [tg_id])
    result = cursor.fetchone()
    balance = result[0]
    balance += 1
    cursor.execute("""UPDATE users SET balance = ? WHERE tg_id = ?""", (balance, tg_id))
    db.commit()
    cursor.close()
    db.close()


def add_admin(tg_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT name, username FROM users WHERE tg_id = ?""", [tg_id])
    rows = cursor.fetchall()
    be_admin = False
    for row in rows:
        name, username = row
    cursor.execute("""SELECT tg_id FROM admins WHERE tg_id = ?""", [tg_id])
    if cursor.fetchone() is None:
        cursor.execute("""INSERT INTO admins (tg_id, username, name) VALUES (?, ?, ?)""", (tg_id, username, name))
        cursor.execute("""UPDATE users SET status = 'Admin' WHERE tg_id = ? """, [tg_id])
    else:
        be_admin = True
    db.commit()
    cursor.close()
    db.close()
    return name, be_admin


def basic_static():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT id FROM users""")
    users1 = cursor.fetchall()
    users = len(users1)
    cursor.execute("""SELECT balance FROM users""")
    balance = cursor.fetchall()
    downloads = sum(row[0] for row in balance)
    cursor.execute("""SELECT id FROM users WHERE lang = 'ru'""")
    ru = cursor.fetchall()
    rus = len(ru)
    cursor.execute("""SELECT id FROM users WHERE lang = 'en'""")
    en = cursor.fetchall()
    eng = len(en)
    db.commit()
    cursor.close()
    db.close()
    return users, rus, eng, downloads


def base():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT id FROM users""")
    users1 = cursor.fetchall()
    users = len(users1)
    db.commit()
    cursor.close()
    db.close()
    return users
