import sqlite3
import datetime


class Database:
    def __init__(self, db_name = 'bot_database.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_users_table()
        self.create_stats_table()

    def create_users_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    created_at TEXT
                )
            """)

    def create_stats_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    checkpoint_id TEXT,
                    car_last_hour INTEGER,
                    car_last_day INTEGER,
                    truck_last_hour,
                    truck_last_day,
                    carCount,
                    truckCount,
                    created_at_date TEXT,
                    created_at_time TEXT,
                    weekday TEXT
                )
            """)


    def add_user(self, user_id, username):
        created_at = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        with self.conn:
            self.conn.execute("""
                INSERT INTO users (user_id, username, created_at) VALUES (?, ?, ?)
            """, (user_id, username, created_at))


    def user_exists(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM users WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone() is not None


    def add_statistics(self, checkpoint_id, car_last_hour, car_last_day, truck_last_hour, truck_last_day, carCount, truckCount):
        creation_date = datetime.datetime.now().strftime('%Y-%m-%d')
        creation_time = datetime.datetime.now().strftime('%H:%M:%S')
        weekday = datetime.datetime.now().strftime('%A')
        with self.conn:
            self.conn.execute("""
                INSERT INTO statistics (checkpoint_id, car_last_hour, car_last_day, truck_last_hour, truck_last_day, carCount, truckCount, created_at_date, created_at_time, weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (checkpoint_id, car_last_hour, car_last_day, truck_last_hour, truck_last_day, carCount, truckCount, creation_date, creation_time, weekday))
    

    def close(self):
        self.conn.close()

