import pyaudio
from vosk import Model, KaldiRecognizer
import serial
import time
import serial.tools.list_ports
import random
import pygame

pygame.mixer.init()

words_json = '["привет", "здравствуйте", "здравствуй", "добрый день", "ладонь", "кулак", "рок", "лайк", "окей", "пока", "до свидания", "конец работы", "большой", "указательный", "средний", "безымянный", "мизинец"]'

def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            print(f"Автоматически найдено устройство: {port.device}")
            return port.device
    return None

def manual_arduino_selection():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Устройства не найдены.")
        return None
    
    for port in ports:
        print(f"Порт: {port.device}")
        print(f"Описание: {port.description}")
        print(f"Производитель: {port.manufacturer}\n")
    print("Введите порт вручную:")
    return f"COM{input()}"

COM = find_arduino()

if COM is None:
    print("Устройство Arduino не найдено. Хотите завершить программу или ввести порт вручную?")
    choice = input("Введите 'q' для выхода или любую другую клавишу для ручного выбора порта: ")
    if choice.lower() == 'q':
        print("Программа завершена.")
        exit()
    else:
        COM = manual_arduino_selection()
        if COM is None:
            print("Программа завершена. Не удалось найти устройства.")
            exit()

try:
    arduino = serial.Serial(COM, 9600)
    time.sleep(2)
    print(f"Успешно подключено к {COM}")
except serial.SerialException as e:
    print(f"Ошибка подключения к {COM}: {e}")
    print("Программа завершена.")
    exit()

model = Model("voiceModels/small_model")
rec = KaldiRecognizer(model, 16000, words_json)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

while True:
    data = stream.read(4096, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        text = rec.Result()
        recognized_text = text[14:-3]
        print(recognized_text)
        
        if recognized_text in ["привет", "здравствуйте", "здравствуй", "добрый день"]:
            stream.stop_stream()
            random_hello = random.randint(1, 5)
            play_sound(f'sounds/hello/{random_hello}.mp3')
            arduino.write(b'0')
            stream.start_stream()

        elif recognized_text in ["ладонь"]:
            stream.stop_stream()
            play_sound(f'sounds/jests/ladon.mp3')
            arduino.write(b'1')
            stream.start_stream()

        elif recognized_text in ["кулак"]:
            stream.stop_stream()
            play_sound(f'sounds/jests/kulak.mp3')
            arduino.write(b'2')
            stream.start_stream()

        elif recognized_text in ["рок"]:
            stream.stop_stream()
            play_sound(f'sounds/jests/rock.mp3')
            arduino.write(b'3')
            stream.start_stream()

        elif recognized_text in ["лайк"]:
            stream.stop_stream()
            play_sound(f'sounds/jests/like.mp3')
            arduino.write(b'4')
            stream.start_stream()

        elif recognized_text in ["окей"]:
            stream.stop_stream()
            play_sound(f'sounds/jests/okay.mp3')
            arduino.write(b'5')
            stream.start_stream()

        elif recognized_text in ["большой"]:
            stream.stop_stream()
            arduino.write(b'6')
            stream.start_stream()

        elif recognized_text in ["указательный"]:
            stream.stop_stream()
            arduino.write(b'7')
            stream.start_stream()

        elif recognized_text in ["средний"]:
            stream.stop_stream()
            arduino.write(b'8')
            stream.start_stream()

        elif recognized_text in ["безымянный"]:
            stream.stop_stream()
            arduino.write(b'9')
            stream.start_stream()

        elif recognized_text in ["мизинец"]:
            stream.stop_stream()
            arduino.write(b'10')
            stream.start_stream()

        elif recognized_text in ["пока", "до свидания", "конец работы"]:
            stream.stop_stream()            
            play_sound('sounds/goodbye/1.mp3')
            arduino.write(b'0')
            stream.start_stream()
            break

stream.stop_stream()
stream.close()
mic.terminate()
arduino.close()
pygame.quit()