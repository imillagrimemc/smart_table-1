import sqlite3
from datetime import datetime


def create_table():
    # Step 1: Establish a connection to the database (creates the database if it doesn't exist)
    conn = sqlite3.connect("water.db")

    # Step 2: Create a cursor
    cursor = conn.cursor()

    # Step 3: Execute SQL to create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Data (
            id INTEGER PRIMARY KEY,
            message TEXT,
            event_date DATETIME
        )
    """)

    # Step 4: Commit the changes
    conn.commit()

    # Step 5: Close the cursor and connection
    cursor.close()
    conn.close()


def insert_data(message, event_date):
    # Step 1: Establish a connection to the database
    conn = sqlite3.connect("water.db")

    # Step 2: Create a cursor
    cursor = conn.cursor()

    # Step 3: Execute SQL to insert data
    cursor.execute("INSERT INTO Data (message, event_date) VALUES (?, ?)", (message, event_date))

    # Step 4: Commit the changes
    conn.commit()

    # Step 5: Close the cursor and connection
    cursor.close()
    conn.close()


def run(message):
    # Create the table (you only need to do this once)
    create_table()
    now = datetime.now()
    # Insert data into the table
    insert_data(message=message, event_date=now)