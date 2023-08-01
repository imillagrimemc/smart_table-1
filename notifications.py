import os
from dotenv import load_dotenv
import psycopg2


# Load environment variables from .env file
load_dotenv()
# PostgreSQL database settings
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")

# OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY")

def save_to_postgres(text):
    try:
        # Replace the connection parameters with your PostgreSQL database credentials
        connection = psycopg2.connect(
            host="localhost",
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASS
        )
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS recognized_data (text TEXT)")

        # Insert the recognized text into the database
        cursor.execute("INSERT INTO recognized_data (text) VALUES (%s)", (text,))
        connection.commit()
        print("Text saved to the PostgreSQL database.")

    except Exception as e:
        print(f"Error saving to PostgreSQL database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def notification(text):
    print('yes sir')
    save_to_postgres(text)

    