import speech_recognition as sr
import os
import json

VOICEPRINT_FILE = "D:/J.A.R.V.I.S/data/voiceprint.json"

def record_sample(label):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Recording sample {label}... Speak now")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        return audio

def enroll_user():
    print("JARVIS Voice Enrollment — speak 3 samples")
    r = sr.Recognizer()
    samples = []
    for i in range(3):
        print(f"Sample {i+1}: Say 'Hello JARVIS my name is Boss'")
        audio = record_sample(i)
        try:
            text = r.recognize_google(audio)
            samples.append(text.lower())
            print(f"Got: {text}")
        except:
            print("Couldn't hear that, try again")

    data = {"enrolled": True, "samples": samples}
    with open(VOICEPRINT_FILE, 'w') as f:
        json.dump(data, f)
    print("Enrollment complete!")
    return True

def is_authorized():
    try:
        with open(VOICEPRINT_FILE, 'r') as f:
            data = json.load(f)
        return data.get("enrolled", False)
    except:
        return False

def verify_voice():
    if not is_authorized():
        print("No voiceprint found. Enrolling...")
        enroll_user()
        return True

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Voice verification — say the passphrase")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio).lower()
            print(f"Heard: {text}")
            if any(word in text for word in ["hello jarvis", "hey jarvis", "jarvis"]):
                return True
            return False
        except:
            return False