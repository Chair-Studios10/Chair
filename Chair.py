from googletrans import Translator
from playsound import playsound
from datetime import datetime
from difflib import SequenceMatcher
from gtts import gTTS
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
import random
import os
import subprocess
import time
import sqlite3
import wikipedia
import webbrowser
import wolframalpha
import random


rec = sr.Recognizer()
merhaba_rules = [
    (r"merhaba", ["Merhaba!", "Selam!", "Hey!", "Nasılsınız?",]),
    (r"nasılsın?", ["Ben bir botum, dolayısıyla duygularım yok. Siz nasılsınız?",]),
    (r"ne yapıyorsun?", ["Size yardımcı olmak için buradayım.", "Kurallara uygun cevaplar veriyorum.",]),
    (r"adın ne?", ["Ben bir botum ve henüz bir ismim yok.",]),
]

def benzer_mi(kelime1, kelime2,rate_oran):
    oran = SequenceMatcher(None, kelime1, kelime2).ratio()
    return oran >= rate_oran

def record(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        voice_rec = ''
        audio = rec.listen(source)
        try:
            voice_rec = rec.recognize_google(audio, language='tr-TR')
        except sr.UnknownValueError:
            speak("Bir daha tekrarlarmısınız")
        return voice_rec   
def record_en(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        voice_rec = ''
        audio = rec.listen(source)
        try:
            voice_rec = rec.recognize_google(audio, language='en_EN')
        except sr.UnknownValueError:
            speak("Can you repeat it again?")
        return voice_rec

def speak(text):
    tts = gTTS(text, lang='tr',slow=False)
    rand = random.randint(1,10000)
    file = 'ses' + str(rand) + '.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)
def speak_en(text):
    tts = gTTS(text, lang='en',slow=False)
    rand = random.randint(1,10000)
    file = 'ses_en' + str(rand) + '.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

def response(voice):
    if "saat kaç" in voice:
        speak(datetime.now().strftime('%H:%M:%S'))
    elif 'arama yap' in voice:#googlede arama yaptırıp arama sayfasını açtırıyoruz
        search = record('ne aramak istiyorsunuz')
        url = 'https://www.google.com/search?q=' + search
        webbrowser.get().open(url)
        speak(search + ' için bulduklarım')
    elif 'kapan' in voice:
        speak('görüşürüz')
        exit() #kapan dediğimizde döngüyü kırıp çıkması için exit() fonksiyonunu kullandık
    elif "aç" in voice:
        txt_file_path = "program_mapping.txt"
        folder_paths = "C:\\"

        if os.path.exists(txt_file_path):
            program_mapping = load_program_mapping_from_txt(txt_file_path)
        else:
            program_mapping = create_program_mapping(folder_paths)
            save_program_mapping_to_txt(program_mapping, txt_file_path)

        chosen_program_r = record('hangi programı açmak istersiniz')
        chosen_program = benzer_mi(chosen_program_r,chosen_program_r,0.7)
        if chosen_program == True:
            speak(chosen_program_r + "Açılıyor")
            launch_program(chosen_program_r, program_mapping)
        #else:
            #chosen_program_r = record_en('Which program would you like to open')
            #chosen_program = benzer_mi(chosen_program_r,chosen_program_r,0.4)
            #speak(chosen_program_r + "Opening...")
            #launch_program(chosen_program_r, program_mapping)
    else:
        chatbot = Chat(merhaba_rules, reflections)
        response = chatbot.respond(voice)
        speak(str(response))

def create_program_mapping(folder_paths):
    program_mapping = {}

    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".exe"):
                    program_name = os.path.splitext(file)[0]
                    program_path = os.path.join(root, file)
                    program_mapping[program_name] = program_path

    return program_mapping

    return program_mapping
def launch_program(program_name, exe_locations):
    if program_name in exe_locations:
        exe_path = exe_locations[program_name]
        subprocess.run([exe_path])
def save_program_mapping_to_txt(program_mapping, file_path):
    with open(file_path, "w") as file:
        for program_name, program_path in program_mapping.items():
            file.write(f"{program_name}:{program_path}\n")
def load_program_mapping_from_txt(file_path):
    program_mapping = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) >= 2:
                program_name = parts[0]
                program_path = ":".join(parts[1:])  # Eğer : karakteri içeriyorsa bu kısmı tekrar bir araya getir
                program_mapping[program_name] = program_path
    return program_mapping


while True:
    voice = record()
    response(voice)
