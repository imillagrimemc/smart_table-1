import subprocess
import speech_recognition as sr
from light import switch_off, switch_on
from volume import increase_vol, decrease_vol
import openai
import threading
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

def openai_ask(question):
    print('Asking ChatGPT...')
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the language model you prefer
        prompt=question,
        max_tokens=50  # Adjust the response length as needed
    )
    answer = response['choices'][0]['text'].strip()
    return answer

def process_question_and_get_answer(question):
    answer = openai_ask(question)
    print("ChatGPT says:")
    print(answer)

def save_to_postgres(text, table_name):
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
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (text TEXT)")

        # Insert the recognized text into the database
        cursor.execute(f"INSERT INTO {table_name} (text) VALUES (%s)", (text,))
        connection.commit()
        print("Text saved to the PostgreSQL database.")

    except Exception as e:
        print(f"Error saving to PostgreSQL database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

import subprocess
import speech_recognition as sr
from light import switch_off, switch_on
from volume import increase_vol, decrease_vol
import openai
import threading
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

def openai_ask(question):
    print('Asking ChatGPT...')
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the language model you prefer
        prompt=question,
        max_tokens=50  # Adjust the response length as needed
    )
    answer = response['choices'][0]['text'].strip()
    return answer

def process_question_and_get_answer(question):
    answer = openai_ask(question)
    print("ChatGPT says:")
    print(answer)

def save_to_postgres(text, table_name):
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
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (text TEXT)")

        # Insert the recognized text into the database
        cursor.execute(f"INSERT INTO {table_name} (text) VALUES (%s)", (text,))
        connection.commit()
        print("Text saved to the PostgreSQL database.")

    except Exception as e:
        print(f"Error saving to PostgreSQL database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


recognizer = sr.Recognizer()  # Declare the recognizer as a global variable
remembered_text = ""  # Variable to store the recognized words after "remember" command

def listen():
    recognizer = sr.Recognizer()
    help_mode = False
    remembering = False  # Flag to indicate "remember" mode
    remembered_text = ""  # Variable to store the recognized words after "remember" command

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                print(audio)

                print("Recognizing...")
                text = recognizer.recognize_google(audio)

                if 'help me' in text.lower():
                    print("Help mode activated. Please ask a question within 5 seconds.")
                    help_mode = True
                    continue

                if help_mode:
                    user_question = text  # Store the user's question for later use
                    print("You asked:")
                    print(text)
                    print(type(text))
                    help_mode = False  # Disable help mode after capturing the question

                    if 'remember' in text.lower():
                        remembering = True  # Enter "remember" mode
                        remembered_text = ""  # Clear any previously stored text
                        print("I'm listening...")

                        # Listen for the user to finish speaking in "remember" mode
                        while True:
                            audio = recognizer.listen(source)
                            try:
                                remembered_text += recognizer.recognize_google(audio) + " "
                            except sr.UnknownValueError:
                                break

                        remembered_text = remembered_text.strip()  # Remove leading/trailing spaces
                        print("Remembered text:")
                        print(remembered_text)
                        remembering = False  # Exit "remember" mode
                        save_to_postgres(remembered_text, "remember")  # Save the recognized text to the "remember" table
                        print("Text saved to the PostgreSQL database.")
                        continue

                    # Use threading to asynchronously process the ChatGPT request
                    thread = threading.Thread(target=process_question_and_get_answer, args=(user_question,))
                    thread.start()

                    continue

                if text:
                    print("You said:")
                    print(text)
                    print(type(text))

                    if 'switch on' in text.lower():
                        switch_on()
                    elif 'switch off' in text.lower():
                        switch_off()
                    elif 'increase volume' in text.lower():
                        increase_vol()
                    elif 'decrease volume' in text.lower():
                        decrease_vol()

            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print(f"Error accessing the Google Web Speech API: {e}")
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception as e:
                # Redirect ALSA error messages to /dev/null (suppress them)
                subprocess.run(["python3", "your_script.py"], stderr=subprocess.DEVNULL)

def save_remembered_text():
    global remembered_text
    if remembered_text:
        save_to_postgres(remembered_text, "remember")
        remembered_text = ""  # Clear the stored text after saving

if __name__ == "__main__":
    listen()
