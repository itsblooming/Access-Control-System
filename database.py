import sqlite3

def create_database():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS behavior_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            typing_speed REAL,
            mouse_movement REAL,
            hold_time REAL,
            flight_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        conn.commit()

def add_user(username):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Username already exists!")

def get_user_id(username):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_user_behavior_data(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT typing_speed, mouse_movement, hold_time, flight_time
            FROM behavior_data WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchall()  # Возвращает список [(val1, val2, val3, val4), ...]
