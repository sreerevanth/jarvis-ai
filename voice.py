import speech_recognition as sr
import pyttsx3
import time

def speak(text):
    print(f"JARVIS: {text}", flush=True)
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.2)

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.8
    with sr.Microphone() as source:
        print("Listening...", flush=True)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            query = r.recognize_google(audio, language='en-in')
            print(f"You: {query}", flush=True)
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""