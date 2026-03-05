# D:\J.A.R.V.I.S\skills\notes.py

import datetime
import json
import config

def take_note(note):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    with open(config.NOTES_FILE, 'a') as f:
        f.write(f"[{timestamp}] {note}\n")
    return f"Note saved Boss"

def read_notes():
    try:
        with open(config.NOTES_FILE, 'r') as f:
            notes = f.read()
        if notes.strip():
            return f"Here are your notes Boss: {notes}"
        else:
            return "You have no notes Boss"
    except:
        return "No notes found Boss"

def clear_notes():
    with open(config.NOTES_FILE, 'w') as f:
        f.write("")
    return "All notes cleared Boss"

def save_to_memory(key, value):
    try:
        with open(config.MEMORY_FILE, 'r') as f:
            memory = json.load(f)
    except:
        memory = {"conversations": [], "preferences": {}, "notes": []}
    
    memory["preferences"][key] = value
    
    with open(config.MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)
    
    return f"Got it Boss, I'll remember that"

def get_from_memory(key):
    try:
        with open(config.MEMORY_FILE, 'r') as f:
            memory = json.load(f)
        return memory["preferences"].get(key, None)
    except:
        return None