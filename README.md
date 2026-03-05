# J.A.R.V.I.S
### Just A Rather Very Intelligent System

> *"Sometimes you gotta run before you can walk."* — Tony Stark

---

## What is JARVIS?

JARVIS is a fully voice-powered AI desktop assistant built in Python — inspired by the AI from Iron Man. It listens, thinks, speaks, and acts. Not just a command executor — a **thinking assistant** that understands natural language, remembers context, and controls your entire PC.

---

## Features

### Voice & Interaction
- Wake word detection — just say **"Jarvis"**
- Natural conversation mode — no need to repeat wake word between commands
- Text input box — type commands when you can't speak
- Speaks back with a natural voice via Windows SAPI5

### AI Brain
- Powered by **Pollinations AI** (free, no API key needed)
- Persistent memory — remembers past conversations
- Answers general knowledge, jokes, explanations, anything

### System Control
- Open and close any application
- Volume up / down / mute
- Take screenshots
- System stats — CPU, RAM, battery
- Shutdown and restart system

### Web & Information
- Search Google
- Play anything on YouTube
- Get weather for any city
- Wikipedia search
- Google Maps — locations and directions
- Top news headlines

### Productivity
- Send real emails via Gmail
- Take and read notes
- Email compose window with UI

### UI
- Futuristic animated interface with rotating rings
- Real-time conversation log
- State indicators — Standby, Listening, Speaking, Processing
- Text input bar at the bottom

---

## Project Structure

```
D:\J.A.R.V.I.S\
├── main.py                  # Entry point
├── brain.py                 # AI brain (Pollinations)
├── voice.py                 # Speech recognition & text-to-speech
├── config.py                # API keys & settings
├── skills\
│   ├── system_control.py    # PC control
│   ├── web_tasks.py         # Web, weather, YouTube, maps
│   ├── notes.py             # Notes & memory
│   └── email_handler.py     # Gmail email sending
├── ui\
│   └── jarvis_ui.py         # Tkinter UI
└── data\
    ├── memory.json          # Persistent conversation memory
    └── notes.txt            # Saved notes
```

---

## Setup & Installation

### Requirements
- Windows 10/11
- Python 3.11.x

### Install Dependencies
```bash
py -3.11 -m pip install speechrecognition pyttsx3 pyaudio openai requests psutil pillow pyautogui wikipedia newsapi-python google-genai
```

### Configure `config.py`
```python
GEMINI_API_KEY = ""          # Optional - if using Gemini
EMAIL_ADDRESS  = "your@gmail.com"
EMAIL_PASSWORD = "your-app-password"
JARVIS_NAME    = "Jarvis"
USER_NAME      = "Boss"
WAKE_WORD      = "jarvis"
MEMORY_FILE    = "D:/J.A.R.V.I.S/data/memory.json"
NOTES_FILE     = "D:/J.A.R.V.I.S/data/notes.txt"
```

### Gmail App Password
1. Go to **myaccount.google.com**
2. Security → 2-Step Verification → App Passwords
3. Generate one for "Mail"
4. Paste it in `config.py` as `EMAIL_PASSWORD`

### Run JARVIS
```bash
C:\Users\<you>\AppData\Local\Programs\Python\Python311\python.exe D:\J.A.R.V.I.S\main.py
```

---

## How to Use

| You say | JARVIS does |
|---|---|
| "Jarvis what time is it" | Tells the time |
| "Jarvis open Chrome" | Opens Chrome |
| "Jarvis close Spotify" | Closes Spotify |
| "Jarvis play Blinding Lights" | Plays on YouTube |
| "Jarvis weather in Mumbai" | Tells weather |
| "Jarvis search Python tutorials" | Googles it |
| "Jarvis take a screenshot" | Saves screenshot |
| "Jarvis system status" | CPU, RAM, battery |
| "Jarvis note this buy groceries" | Saves a note |
| "Jarvis read my notes" | Reads all notes |
| "Jarvis send email" | Walks you through it |
| "Jarvis tell me a joke" | AI responds |
| "Jarvis who is Elon Musk" | AI answers |
| "Thanks" / "Done" | Ends conversation mode |
| "Exit Jarvis" | Shuts down JARVIS |
| "System shutdown" | Shuts down your PC |

---

## Wake Words Supported
JARVIS responds to:
`jarvis`, `javis`, `javish`, `jaarvis`, `jervis`, `harvey`, `jarv`, `travis`, `davis`

*(because speech recognition isn't perfect)*

---

## Built With

- **Python 3.11**
- **SpeechRecognition** — voice input
- **pyttsx3 + SAPI5** — voice output
- **Pollinations AI** — free AI brain
- **Tkinter** — UI
- **psutil** — system stats
- **pyautogui** — screenshots & automation
- **smtplib** — email sending
- **Wikipedia API** — knowledge
- **webbrowser + requests** — web tasks

---

## Roadmap

- [ ] Voice authentication — respond only to your voice
- [ ] Google Calendar integration
- [ ] Browser automation — click, scroll, type
- [ ] Spotify API control
- [ ] Proactive morning briefing
- [ ] Emotion detection from voice tone
- [ ] Multi-language support

---

## Built by

Two people, one competition, zero chill. 🔥

*"They built a remote control. We built something that thinks."*
