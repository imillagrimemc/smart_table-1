import subprocess
import speech_recognition as sr
from light import switch_off, switch_on
from notifications import run
from volume import increase_vol, decrease_vol

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
                    switch_on()
                elif 'switch off' in result.lower():
                    switch_off()
                elif 'increase volume' in result.lower():
                    increase_vol()
                elif 'decrease volume' in result.lower():
                    decrease_vol()
                
                    
                if 'remember' in result.lower():
                    print("Remember mode activated.")
                    remember_mode = True
                    continue

                if remember_mode:
                    user_question = result  # Store the user's question for later use
                    # print("You talked:")
                    # print(result)
                    # print(type(result))
                    remember_mode = False  # Disable help mode after capturing the question
                    run(message=result)



        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            # Redirect ALSA error messages to /dev/null (suppress them)
            subprocess.run(["python3", "your_script.py"], stderr=subprocess.DEVNULL)