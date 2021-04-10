import sqlite3
import config


def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute("""create table if not exists stat(event_time TEXT, status TEXT, text TEXT, bot_status TEXT, 
    unique(event_time, text) ON CONFLICT REPLACE);""")
    conn.commit()


init_db()


def ins_stat(update):
    print("row to insert:", update)
    if len(update) == 3:
        conn = sqlite3.connect(config.DB_PATH)
        cur = conn.cursor()
        event_time = update[0]
        status = update[1]
        text = update[2]
        cur.execute(
            """insert or replace into stat(event_time, status, text) values(:event_time, :status, :text) 
            ON CONFLICT(event_time, text) DO NOTHING;""",
            {"event_time": event_time, "status": status, "text": text})
        print("inserted rows:", conn.total_changes)
        conn.commit()

    else:
        print("no data to insert")


def select_to_send():
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute("""select * from stat where bot_status is null order by event_time;""")
    return cur.fetchall()


def set_sent(x):
    event_time = x[0]
    text = x[2]
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute("""UPDATE stat SET bot_status = 'send' WHERE event_time=:event_time and text=:text;""",
                {"event_time": event_time, "text": text})
    conn.commit()
