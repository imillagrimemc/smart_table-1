import sqlite3
from datetime import datetime

def get_last_row():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()

    query = "SELECT * FROM Data ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    last_row = cursor.fetchone()
    conn.close()
    return last_row


def format_datetime(datetime_str):
    dt_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    formatted_date = dt_object.strftime("%d-%m")
    formatted_time = dt_object.strftime("%H:%M")
    return f"{formatted_date} at {formatted_time}"

def where_is():
    last_row = get_last_row()
    formatted_datetime = format_datetime(last_row[2])
    return f"{last_row[1]} at {formatted_datetime}"


