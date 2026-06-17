import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JSON_FILE = os.path.join(BASE_DIR, "database", "conversation_history.json")
WEATHER_FILE = os.path.join(BASE_DIR, "database", "weather_history.json")

def add_conversation_history(role: str, content: str):
    if role not in ("system", "user", "assistant"):
        return

    # Ensure content is always a string
    content = str(content)

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append({
        "role": role,
        "content": content
    })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_weather_history(role: str, content: str):
    if role not in ("system", "user", "assistant"):
        return

    # Ensure content is always a string
    content = str(content)

    if os.path.exists(WEATHER_FILE):
        with open(WEATHER_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append({
        "role": role,
        "content": content
    })

    with open(WEATHER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_last_weather():
    if not os.path.exists(JSON_FILE):
        return None

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

    if not data:
        return None

    return data[-1]