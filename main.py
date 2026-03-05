import sys
import traceback
import threading
from skills.email_handler import send_email
from ui.jarvis_ui import text_command_queue
sys.path.insert(0, 'D:/J.A.R.V.I.S')

try:
    import datetime
    import webbrowser
    import subprocess
    import os

    from voice import speak, listen
    from brain import ask_gemini
    from skills.system_control import (
        get_time, get_date, get_system_stats,
        open_application, take_screenshot,
        volume_up, volume_down, mute
    )
    from skills.web_tasks import (
        search_google, play_youtube, get_weather,
        get_wikipedia, open_maps, get_news,
        search_maps_distance,
    )
    from skills.notes import take_note, read_notes, clear_notes
    from skills.email_handler import send_email
    import config
    from ui.jarvis_ui import launch_ui

    ui = None

    APP_EXECUTABLES = {
        "whatsapp": "WhatsApp.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "notepad": "notepad.exe",
        "spotify": "Spotify.exe",
        "discord": "Discord.exe",
        "telegram": "Telegram.exe",
        "vlc": "vlc.exe",
        "zoom": "Zoom.exe",
        "pycharm": "pycharm64.exe",
        "vscode": "Code.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "obs": "obs64.exe",
        "task manager": "Taskmgr.exe",
        "calculator": "CalculatorApp.exe",
        "paint": "mspaint.exe",
        "teams": "ms-teams.exe",
        "slack": "slack.exe",
        "skype": "Skype.exe",
        "notion": "Notion.exe",
    }

    def greet():
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        msg = f"{greeting} {config.USER_NAME}. I am JARVIS, your personal AI assistant. How can I assist you today?"
        ui.add_log("JARVIS", msg)
        speak(msg)

    def handle_command(query):
        if not query:
            return

        ui.set_state("processing")
        ui.add_log("You", query)

        if "send email" in query or "email to" in query or "send an email" in query:
            speak("Who should I send it to Boss?")
            to = listen()
            speak("What's the subject?")
            subject = listen()
            speak("What should I say?")
            body = listen()
            r = send_email(to, subject, body)
            ui.add_log("JARVIS", r); speak(r)


        elif "time" in query:
            r = get_time()
            ui.add_log("JARVIS", r); speak(r)

        elif "date" in query:
            r = get_date()
            ui.add_log("JARVIS", r); speak(r)

        elif "system status" in query or "cpu" in query or "ram" in query or "battery" in query:
            r = get_system_stats()
            ui.add_log("JARVIS", r); speak(r)

        elif "screenshot" in query:
            r = take_screenshot()
            ui.add_log("JARVIS", r); speak(r)

        elif "system shutdown" in query or "shutdown system" in query:
            r = "Shutting down the system in 5 seconds Boss"
            ui.add_log("JARVIS", r); speak(r)
            os.system("shutdown /s /t 5")

        elif "system restart" in query or "restart system" in query:
            r = "Restarting in 5 seconds Boss"
            ui.add_log("JARVIS", r); speak(r)
            os.system("shutdown /r /t 5")

        elif "exit jarvis" in query or "goodbye jarvis" in query or "stop jarvis" in query or "turn off jarvis" in query:
            r = f"Goodbye {config.USER_NAME}. JARVIS signing off."
            ui.add_log("JARVIS", r); speak(r)
            sys.exit()

        elif "volume up" in query:
            r = volume_up()
            ui.add_log("JARVIS", r); speak(r)

        elif "volume down" in query:
            r = volume_down()
            ui.add_log("JARVIS", r); speak(r)

        elif "mute" in query:
            r = mute()
            ui.add_log("JARVIS", r); speak(r)

        elif "close" in query or "kill" in query:
            query_clean = query.replace("close", "").replace("kill", "").replace("please", "").replace("for me", "").strip()
            if "tab" in query_clean or ("all" in query_clean and "chrome" in query_clean):
                os.system("taskkill /f /im chrome.exe")
                r = "Closed all Chrome tabs Boss"
            else:
                closed = False
                for key, exe in APP_EXECUTABLES.items():
                    if key in query_clean:
                        result = os.system(f"taskkill /f /im {exe}")
                        r = f"Closed {key} Boss" if result == 0 else f"{key} wasn't running Boss"
                        closed = True
                        break
                if not closed:
                    r = "I couldn't find that app to close Boss"
            ui.add_log("JARVIS", r); speak(r)

        elif "open" in query and "youtube" in query and "play" not in query:
            webbrowser.open("https://www.youtube.com")
            r = "Opening YouTube Boss"
            ui.add_log("JARVIS", r); speak(r)

        elif "play" in query:
            song = query.replace("play", "").replace("on youtube", "").replace("youtube", "").replace("for me", "").strip()
            r = play_youtube(song)
            ui.add_log("JARVIS", r); speak(r)

        elif "chrome" in query and ("tab" in query or "new" in query):
            subprocess.Popen("chrome.exe --new-tab")
            r = "Opening a new Chrome tab Boss"
            ui.add_log("JARVIS", r); speak(r)

        elif "open" in query:
            app = query.replace("open", "").replace("for me", "").replace("please", "").strip()
            r = open_application(app)
            ui.add_log("JARVIS", r); speak(r)

        elif "search" in query or "google" in query:
            search_query = query.replace("search", "").replace("google", "").strip()
            r = search_google(search_query)
            ui.add_log("JARVIS", r); speak(r)

        elif "weather" in query:
            city = query.replace("weather", "").replace("in", "").strip()
            if not city:
                city = "Bengaluru"
            r = get_weather(city)
            ui.add_log("JARVIS", r); speak(r)

        elif "wikipedia" in query:
            search = query.replace("wikipedia", "").strip()
            r = get_wikipedia(search)
            ui.add_log("JARVIS", r); speak(r)

        elif "map" in query or "location" in query or "where is" in query:
            location = query.replace("map", "").replace("location", "").replace("where is", "").strip()
            r = open_maps(location)
            ui.add_log("JARVIS", r); speak(r)

        elif "distance" in query or "direction" in query:
            speak("Where from Boss?")
            origin = listen()
            speak("Where to Boss?")
            destination = listen()
            r = search_maps_distance(origin, destination)
            ui.add_log("JARVIS", r); speak(r)

        elif "news" in query or "headlines" in query:
            r = get_news()
            ui.add_log("JARVIS", r); speak(r)

        elif "take note" in query or "note this" in query or "remember this" in query:
            note = query.replace("take note", "").replace("note this", "").replace("remember this", "").strip()
            if not note:
                speak("What should I note Boss?")
                note = listen()
            r = take_note(note)
            ui.add_log("JARVIS", r); speak(r)

        elif "read notes" in query or "my notes" in query:
            r = read_notes()
            ui.add_log("JARVIS", r); speak(r)

        elif "clear notes" in query:
            r = clear_notes()
            ui.add_log("JARVIS", r); speak(r)

        else:
            r = ask_gemini(query)
            ui.add_log("JARVIS", r); speak(r)

        ui.set_state("idle")

    def run_jarvis():
        greet()
        ui.add_log("JARVIS", "Say JARVIS to wake me up Boss")
        speak("Say JARVIS to wake me up Boss")

        wake_words = ["jarvis", "davis", "travis", "service", "javish",
                      "javis", "jaarvis", "jarwis", "jervis", "harvey", "jarv"]

        while True:
            # Check for text commands
            try:
                text_cmd = text_command_queue.get_nowait()
                handle_command(text_cmd)
            except:
                pass
            try:
                print("Waiting for wake word...", flush=True)
                ui.set_state("idle")
                query = listen()

                if not query:
                    continue

                if any(word in query for word in wake_words):
                    ui.set_state("listening")
                    speak("Yes Boss?")
                    ui.add_log("JARVIS", "Yes Boss?")

                    command = query
                    for word in wake_words + ["hey"]:
                        command = command.replace(word, "").strip()

                    if command:
                        handle_command(command)

                    # Conversation mode - silent listen, no "Anything else Boss?"
                    empty_count = 0
                    while True:
                        ui.set_state("listening")
                        print("Listening for follow up...", flush=True)
                        follow_up = listen()

                        if not follow_up:
                            empty_count += 1
                            if empty_count >= 3:
                                speak("Standing by Boss.")
                                ui.set_state("idle")
                                break
                            continue

                        empty_count = 0

                        if any(word in follow_up for word in ["thanks", "done", "that's all", "nothing", "no", "thank you", "bye"]):
                            speak("Anytime Boss!")
                            ui.add_log("JARVIS", "Anytime Boss!")
                            ui.set_state("idle")
                            break
                        else:
                            handle_command(follow_up)

            except KeyboardInterrupt:
                speak("JARVIS signing off.")
                break
            except Exception as e:
                print(f"Error: {e}", flush=True)
                continue

    def main():
        global ui
        ui = launch_ui()

    def email_callback(to, subject, body):
        r = send_email(to, subject, body)
        ui.add_log("JARVIS", r)
        speak(r)

    ui.on_email_send = email_callback

    t = threading.Thread(target=run_jarvis, daemon=True)
    t.start()
    ui.run()

main()

except Exception as e:
    print("STARTUP ERROR:", e)
    traceback.print_exc()
    input("Press enter to close...")