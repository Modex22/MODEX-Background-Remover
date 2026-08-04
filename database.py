import sqlite3

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            images_processed INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO stats (id, images_processed)
        VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


def add_user(user):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (
        user.id,
        user.username,
        user.first_name
    ))

    conn.commit()
    conn.close()


def increment_images():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE stats
        SET images_processed = images_processed + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()


def total_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def total_images():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT images_processed
        FROM stats
        WHERE id = 1
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count