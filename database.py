# database

import sqlite3

DB_NAME = "database.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    # Таблиця користувачів
    curs.execute("""CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT NOT NULL,
                 age INTEGER NOT NULL
    )""")

    # Таблиця завдань
    curs.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT,
                created_at TIMESTAMP NOT NULL,
                due_at TIMESTAMP NOT NULL,
                priority INTEGER NOT NULL,
                done BOOLEAN NOT NULL,
                FOREIGN KEY("user_id") REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

#
def add_user(username, password, age):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", (username, password, age))
    conn.commit()
    conn.close()
#
def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = curs.fetchone()
    conn.close()
    return user

#
def delete_user(username):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("DELETE FROM tasks WHERE user_id = ?", (username,))
    curs.execute("DELETE FROM users WHERE id = ?", (username,))
    conn.commit()
    conn.close()

#
def add_task(user_id, description, created_at, due_at, priority):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("""INSERT INTO tasks (user_id, description, created_at, due_at, priority, done)
                    VALUES (?, ?, ?, ?, ?, 0)""", (user_id, description, created_at, due_at, priority))
    conn.commit()
    conn.close()


#
def get_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = curs.fetchone()
    conn.close()
    return task
#
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

#
def update_task(task_id, description, due_at, priority):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("""UPDATE tasks SET description = ?,
                 due_at = ?,
                 priority = ?
                 WHERE id = ?""", (description, due_at, priority, task_id))
    conn.commit()
    conn.close()

#
def toggle_task_done(task_id, done_value):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("UPDATE tasks SET done = ? WHERE id = ?", (done_value, task_id))
    conn.commit()
    conn.close()

#
def get_filtr_tasks(user_id, status=None, priority=None):
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    query = """SELECT * FROM tasks WHERE user_id = ?"""
    params = [user_id]

    if status == "done":
        query += " AND done = 1"
    elif status == "not_done":
        query += " AND done = 0"

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    curs.execute(query, params)
    tasks = curs.fetchall()
    conn.close()
    return tasks

#
def get_all_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'user'")
    return cursor.fetchall()

#
def get_all_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()
