import webbrowser
import requests
import wikipedia
import urllib.parse


def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching Google for {query} Boss"


def play_youtube(query):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Playing {query} on YouTube Boss"


def get_weather(city):
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3"
        response = requests.get(url, timeout=5)
        return response.text.strip()
    except:
        return f"Couldn't fetch weather for {city} Boss"


def get_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            result = wikipedia.summary(e.options[0], sentences=2)
            return result
        except:
            return "Could you be more specific Boss?"
    except:
        return "I couldn't find that on Wikipedia Boss"


def open_maps(location):
    url = f"https://www.google.com/maps/search/{urllib.parse.quote(location)}"
    webbrowser.open(url)
    return f"Opening maps for {location} Boss"


def get_news():
    try:
        webbrowser.open("https://news.google.com")
        return "Opening Google News Boss"
    except:
        return "Couldn't open news Boss"


def search_maps_distance(origin, destination):
    url = f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}/{urllib.parse.quote(destination)}"
    webbrowser.open(url)
    return f"Showing directions from {origin} to {destination} Boss"

def morning_briefing():
    import datetime
    hour = datetime.datetime.now().hour
    weather = get_weather("Bengaluru")
    news = "Opening Google News for latest headlines"
    return f"Good Morning Boss! It's {datetime.datetime.now().strftime('%I:%M %p')}. Weather update: {weather}. {news}"