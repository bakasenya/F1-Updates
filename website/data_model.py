import sqlite3

def get_db_connection():
    con = sqlite3.connect("stats_database.db")
    cur = con.cursor()
    return con, cur

def create_stats_table():
    con, cur = get_db_connection()
    cur.execute("""CREATE TABLE IF NOT EXISTS stats
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    year INTEGER, 
                    url TEXT)
                    """)
    con.commit()
    con.close()
