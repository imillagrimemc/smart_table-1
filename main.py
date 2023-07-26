import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5)  # Listen for up to 5 seconds

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)  # Use Google Web Speech API
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Error accessing the Google Web Speech API: {e}")

    return None

if __name__ == "__main__":
    while True:
        result = listen()
        if result:
            print("You said:", result)