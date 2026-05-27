import sqlite3
from datetime import datetime

DB_NAME = "data/focushub.db"


def create_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            focus_score INTEGER,
            presence_status TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_reading(temperature, humidity, focus_score, presence_status):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO readings (
            timestamp, temperature, humidity, focus_score, presence_status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        temperature,
        humidity,
        focus_score,
        presence_status
    ))

    connection.commit()
    connection.close()


def get_recent_readings(limit=10):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, temperature, humidity, focus_score, presence_status
        FROM readings
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    connection.close()

    return rows
