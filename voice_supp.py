import pyaudio
import wave
import noisereduce as nr

# параметры записи голоса
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# создание объекта PyAudio
audio = pyaudio.PyAudio()

# открытие потока записи голоса
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Запись голоса началась...")

# чтение данных из потока записи голоса
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Запись голоса завершена.")

# остановка потока записи голоса и закрытие объекта PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# сохранение записанного голоса в файл
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# загрузка записанного голоса и удаление шума
wave_data = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
audio_signal = wave_data.readframes(-1)
sample_rate = wave_data.getframerate()
noise_sample = audio_signal[:int(sample_rate)]
audio_signal = audio_signal[int(sample_rate):]
reduced_noise = nr.reduce_noise(audio_clip=audio_signal, noise_clip=noise_sample, verbose=False)

# сохранение записанного и обработанного голоса в файл
with wave.open("output_processed.wav", 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(reduced_noise)