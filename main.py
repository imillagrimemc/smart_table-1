import numpy as np
import sounddevice as sd
import noisereduce as nr
import speech_recognition as sr
import subprocess
from light import switch_off, switch_on
from notifications import run
from volume import increase_vol, decrease_vol

from gtts import gTTS

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)
# GPIO.output(11, 1)

# Function for text-to-speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    subprocess.run(["mpg321", "output.mp3"])

# Function for speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        print(audio)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Error accessing the Google Web Speech API: {e}")

    return None


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        print(audio)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Error accessing the Google Web Speech API: {e}")

    return None

def main():
    sample_rate = 44100
    duration = 5

    print("Recording audio...")

    # Recording audio from the microphone
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    sd.wait()

    print("Audio recorded. Processing...")

    # Applying noise reduction algorithm
    denoised_audio = nr.reduce_noise(y=recording.flatten(), sr=sample_rate)

    # Creating a Recognizer object
    recognizer = sr.Recognizer()

    # Using denoised audio for speech recognition
    with sr.AudioData(denoised_audio.tobytes(), sample_rate, 2) as source:
        print("Speak something:")
        audio = recognizer.listen(source)

    # Trying to recognize the voice command
    try:
        print("You said: " + recognizer.recognize_google(audio, language="en-US"))
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print("Error accessing the Google Web Speech API: {0}".format(e))

if __name__ == "__main__":
    remember_mode = False

    while True:
        try:
            result = listen()

            if result:
                print("You said:")
                print(result)
                print(type(result))
                if 'switch on' in result.lower():
                    # GPIO.output(11, 0)
                    print('lights are switched on')
                elif 'switch off' in result.lower():
                    # GPIO.output(11, 1)
                    print('lights are switched off')
                elif 'increase volume' in result.lower():
                    increase_vol()
                elif 'decrease volume' in result.lower():
                    decrease_vol()

                # Perform text-to-speech for recognized text
                speak(result)

                if 'remember' in result.lower():
                    print("Remember mode activated.")
                    remember_mode = True
                    continue

                if remember_mode:
                    user_question = result  # Store the user's question for later use
                    # print("You talked:")
                    # print(result)
                    print(type(result))
                    remember_mode = False  # Disable help mode after capturing the question
                    run(message=result)

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            # Redirect ALSA error messages to /dev/null (suppress them)
            subprocess.run(["python3", "your_script.py"], stderr=subprocess.DEVNULL)
