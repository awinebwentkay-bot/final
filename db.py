"""长期记忆 SQLite 数据库"""

import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS venue
        (id INTEGER PRIMARY KEY, name TEXT, max_num INTEGER, open_time TEXT, device TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS history_case
        (id INTEGER PRIMARY KEY, plan TEXT, budget INTEGER, feedback TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS rule
        (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()


def save_case(state: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO history_case(plan, budget, feedback) VALUES (?,?,?)',
                (state["activity_plan"], state["total_budget"], state["eval_comment"]))
    conn.commit()
    conn.close()


def search_history_case():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    res = cur.execute("SELECT plan,budget,feedback FROM history_case LIMIT 3")
    data = res.fetchall()
    conn.close()
    return [{"plan": i[0], "budget": i[1], "feedback": i[2]} for i in data]


init_db()