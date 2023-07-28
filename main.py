import subprocess
import speech_recognition as sr
from light import switch_off, switch_on
from volume import increase_vol, decrease_vol
import openai
import threading

# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
openai.api_key = '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'

def openai_ask(question):
    print('Asking ChatGPT...')
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the language model you prefer
        prompt=question,
        max_tokens=50  # You can adjust the response length as needed
    )
    answer = response['choices'][0]['text'].strip()
    return answer

def process_question_and_get_answer(question):
    answer = openai_ask(question)
    print("ChatGPT says:")
    print(answer)

def listen():
    recognizer = sr.Recognizer()
    help_mode = False
    user_question = None  # Variable to store the user's question

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

if __name__ == "__main__":
    listen()


#           Command to activate voice assistant - hey billy, billy etc
#       QUESTIONS related to table
#1. Volume regulations /increase_voice, /decrease_voice
#2. Light adjustment /switch on/off - Lumos 
#3. Notifications /remember  ->chatgpt -> paraphrase from 3rd party -> save to database.

#       DYNAMIC QUESTIONS
#Dynamic questions will be by command word /billy_help_me. After which comes question. 
# Remember messages from user /remember

# Шумоподавление
# Озвучка результата с терминала
# команда/remember 