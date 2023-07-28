import subprocess
import speech_recognition as sr
from light import switch_off, switch_on
from volume import increase_vol, decrease_vol
import openai

# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
openai.api_key = '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'

def openai_ask(question):
    print('Asking ChatGPT...')
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the language model you prefer
        prompt=question,
        max_tokens=100  # You can adjust the response length as needed
    )
    answer = response.choices[0].text.strip()
    return answer

def listen_for_question():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for question...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        print(audio)

    try:
        print("Recognizing question...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the question.")
    except sr.RequestError as e:
        print(f"Error accessing the Google Web Speech API: {e}")

    return None

def listen():
    recognizer = sr.Recognizer()
    help_mode = False

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                print(audio)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)

            if help_mode:
                print("You asked:")
                print(text)
                print(type(text))
                help_mode = False  # Disable help mode after capturing the question

                print("Asking ChatGPT...")
                answer = openai_ask(text)  # Call the function to ask ChatGPT
                print("ChatGPT says:")
                print(answer)
                continue

            if 'help me' in text.lower():
                print("Help mode activated. Please ask a question within 5 seconds.")
                help_mode = True
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


# Шумоподавление
# Озвучка результата с терминала