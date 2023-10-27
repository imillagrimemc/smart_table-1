import speech_recognition as sr
import subprocess
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
# from gpt import gpt_answer
# from dht import runs
# from notifications import run
# from volume import increase_vol, decrease_vol
# from where_is import where_is
# from music import music_function


# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)
# GPIO.output(11, 1)


# Функция Текст-в-речь
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    subprocess.run(["mpg321", "output.mp3"])

def play_peep_sound():
    peep_sound_path = "peep.wav"  # Путь к файлу с звуком

    # Загрузите аудиофайл с использованием soundfile
    peep_data, sample_rate = sf.read(peep_sound_path)

    # Воспроизведите аудиофайл с использованием sounddevice
    sd.play(peep_data, sample_rate)
    sd.wait()

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Скажите что-нибудь:")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-en")
        print("Вы сказали: " + text)
        return text
    except sr.UnknownValueError:
        print("Речь не распознана")
    except sr.RequestError as e:
        print("Ошибка при обращении к сервису распознавания речи: {0}".format(e))
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
                if "switch on" in result.lower():
                    play_peep_sound()
                    # GPIO.output(11, 0)
                    print("lights are switched on")
                elif "switch off" in result.lower():
                    play_peep_sound()
                    # GPIO.output(11, 1)
                    print("lights are switched off")
                # elif "increase volume" in result.lower():
                #     increase_vol()
                # elif "decrease volume" in result.lower():
                #     decrease_vol()

                if "remember" in result.lower():
                    print("Remember mode activated.")
                    remember_mode = True
                    continue

                # print("remember_mode", remember_mode)
                
                # if remember_mode:
                #     user_question = result  # Store the user's question for later use
                #     print("You talked:")
                #     print(result)
                #     print(type(result))
                #     remember_mode = (
                #         False  # Disable help mode after capturing the question
                #     )
                #     run(message=result)

                # if "where is" in result.lower():
                #     print("Notification mode activated.")
                #     notification = where_is()
                #     print("notification: ", notification)
                #     speak(notification)
                #     music_function()

                if "help me" in result.lower():
                    print(
                        "Help mode activated. Please ask a question within 5 seconds."
                    )
                    help_mode = True
                    continue

                # if "temperature" in result.lower():
                #     temperature = runs()

                # if help_mode:
                #     user_question = result  # Store the user's question for later use
                #     print("You asked:")
                #     print(result)
                #     # print(type(result))
                #     help_mode = False  # Disable help mode after capturing the question
                #     answer = gpt_answer(query=user_question)
                #     speak(answer)
                #     music_function()
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            # Redirect ALSA error messages to /dev/null (suppress them)
            subprocess.run(["python3", "your_script.py"], stderr=subprocess.DEVNULL)
