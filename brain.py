import requests
import json
import config

POLLINATIONS_URL = "https://text.pollinations.ai/"

def load_memory():
    try:
        with open(config.MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"conversations": [], "preferences": {}, "notes": []}

def save_memory(memory):
    with open(config.MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def understand_intent(query):
    prompt = f"""You are JARVIS intent classifier. Given user input, return ONLY a JSON like:
{{"intent": "general_question", "entity": ""}}

Intents: open_app, close_app, play_music, search_web, get_weather, send_email, take_note, get_time, get_date, system_stats, morning_briefing, general_question

User said: {query}
JSON only:"""

    try:
        response = requests.get(
            POLLINATIONS_URL + requests.utils.quote(prompt),
            timeout=10
        )
        import json as js
        text = response.text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        return js.loads(text[start:end])
    except:
        return {"intent": "general_question", "entity": query}

def ask_gemini(query, context=""):
    memory = load_memory()
    last_convos = memory["conversations"][-5:] if memory["conversations"] else []
    history_text = ""
    for c in last_convos:
        history_text += f"User: {c['user']}\nJarvis: {c['jarvis']}\n"

    prompt = f"""You are JARVIS, an advanced AI assistant just like from Iron Man.
You are helping your boss named {config.USER_NAME}.
Be smart, witty, confident and helpful. Keep responses concise — 1 to 2 sentences max.
Never say you are an AI. You are JARVIS.

Previous conversation:
{history_text}

Boss says: {query}

Respond as JARVIS:"""

    try:
        response = requests.get(
            POLLINATIONS_URL + requests.utils.quote(prompt),
            timeout=15
        )
        reply = response.text.strip()
        memory["conversations"].append({"user": query, "jarvis": reply})
        save_memory(memory)
        return reply
    except Exception as e:
        return f"My apologies Boss: {str(e)}"