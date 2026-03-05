# D:\J.A.R.V.I.S\skills\system_control.py

import os
import subprocess
import psutil
import pyautogui
import datetime
import webbrowser

def get_time():
    now = datetime.datetime.now()
    return f"It's {now.strftime('%I:%M %p')} Boss"

def get_date():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d %Y')} Boss"

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    
    stats = f"CPU is at {cpu}%, RAM usage is {ram.percent}%"
    if battery:
        stats += f", Battery at {int(battery.percent)}%"
        if battery.power_plugged:
            stats += " and charging"
    return stats

def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        "vscode": "code.exe",
        "explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "whatsapp": "WhatsApp.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "control panel": "control.exe",
        "settings": "ms-settings:",
        "device manager": "devmgmt.msc",
        "disk manager": "diskmgmt.msc",
        "services": "services.msc",
        "registry editor": "regedit.exe",
        "system information": "msinfo32.exe",
        "resource monitor": "resmon.exe",
        "event viewer": "eventvwr.msc",
        "snipping tool": "snippingtool.exe",
        "on screen keyboard": "osk.exe",
        "pycharm": "pycharm64.exe",
        "terminal": "wt.exe",
        "github desktop": "GitHubDesktop.exe",
        "docker": "Docker Desktop.exe",
        "postman": "Postman.exe",
        "android studio": "studio64.exe",
        "obs": "obs64.exe",
        "zoom": "zoom.exe",
        "teams": "ms-teams.exe",
        "discord": "discord.exe",
        "telegram": "Telegram.exe",
        "slack": "slack.exe",
        "skype": "skype.exe",
        "photoshop": "Photoshop.exe",
        "illustrator": "Illustrator.exe",
        "premiere pro": "Adobe Premiere Pro.exe",
        "after effects": "AfterFX.exe",
        "notion": "Notion.exe",
    }
    
    
    for key in apps:
        if key in app_name:
            try:
                subprocess.Popen(apps[key])
                return f"Opening {key} Boss"
            except:
                return f"Couldn't find {key} on your system Boss"
    
    try:
        subprocess.Popen(app_name)
        return f"Trying to open {app_name} Boss"
    except:
        return f"I couldn't open that Boss"

def open_website(url):
    if "http" not in url:
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url} Boss"

def take_screenshot(filename="screenshot"):
    path = f"D:/J.A.R.V.I.S/data/{filename}.png"
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename} Boss"

def shutdown():
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds Boss"

def restart():
    os.system("shutdown /r /t 5")
    return "Restarting in 5 seconds Boss"

def volume_up():
    for _ in range(5):
        pyautogui.press('volumeup')
    return "Volume increased Boss"

def volume_down():
    for _ in range(5):
        pyautogui.press('volumedown')
    return "Volume decreased Boss"

def mute():
    pyautogui.press('volumemute')
    return "Muted Boss"