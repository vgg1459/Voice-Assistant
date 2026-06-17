import requests

OLLAMA_URL = "http://localhost:11434/"
OLLAMA_MODEL = "qwen2.5:7b-Instruct"

tools1= [
    {
      "type": "function",
      "function": {
        "name": "create_calendar_event",
        "description": "Create, add or make a calendar event or meeting or appointment",
        "parameters": {
          "properties": {
            "title": { "type": "string" },
            "description": { "type": "string" },
            "start_time": { "type": "string" },
            "end_time": { "type": "string" },
            "location": { "type": "string" }
          },
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "update_calendar_event",
        "description": "Update a calendar event, Change Title, location, time or description of meeting",
        "parameters": {
          "properties": {
            "id": { "type": "number" },
            "title": { "type": "string" },
            "description": { "type": "string" },
            "start_time": { "type": "string" },
            "end_time": { "type": "string" },
            "location": { "type": "string" }
          },
            "required": ["id"],
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "delete_calendar_event",
        "description": "Delete/Remove a calendar event",
        "parameters": {
          "properties": {
            "id": { "type": "number" },
            "title": {"type": "string"},
            "description": {"type": "string"},
            "start_time": {"type": "string"},
            "end_time": {"type": "string"},
            "location": {"type": "string"}
          },
            "required": ["id"],
        }
      }
    },
    {
        "type": "function",
        "function": {
            "name": "list_calendar_events",
            "description": "List all calendar events or meetings for the user. Get details about existing, next events for user.",
            "parameters": {
                "properties": {}
            }
        }
    }
]

tools2 =[{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get weather for a place",
        "parameters": {
          "properties": {
            "place": {
              "type": "string",
              "description": "City or place name"
            }
          },
          "required": ["place"]
        }
      }
    }]
import json

def load_conversation_history(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def query_ollama(prompt: str, user_text: str, tool, model: str = OLLAMA_MODEL):
    conversation_history = load_conversation_history(
        "../database/conversation_history.json"
    )
    if tool == "weather":
        tools = tools2
    else:
        tools = tools1

    current_user_message = {
        "role": "user",
        "content": user_text
    }

    payload = {
        "model": model,
        "messages": [
           *conversation_history,
           {"role": "system", "content": prompt},
            current_user_message
        ],
        "tools": tools,
        "stream": False
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload
    )
    response.raise_for_status()

    data = response.json()
    message = data.get("message", {})

    if message.get("tool_calls"):
        return {
            "type": "tool_call",
            "tool_calls": message["tool_calls"]
        }

    return {
        "type": "message",
        "content": message.get("content", "").strip()
    }

def query_ollama2(prompt: str, user_text, model: str = OLLAMA_MODEL) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text},
            ],
            "stream": False,
        }
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            stream=True
        )

        response.raise_for_status()
        data = response.json()
        print(data)
        raw = data["message"]["content"]
        return raw.strip()

tools3= [
    {
      "type": "function",
      "function": {
        "name": "update_calendar_event",
        "description": "Update a calendar event, Change Title, location, time or description of meeting",
        "parameters": {
          "properties": {
            "id": { "type": "number" },
            "title": { "type": "string" },
            "description": { "type": "string" },
            "start_time": { "type": "string" },
            "end_time": { "type": "string" },
            "location": { "type": "string" }
          },
            "required": ["id"],
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "delete_calendar_event",
        "description": "Delete/Remove a calendar event",
        "parameters": {
          "properties": {
            "id": { "type": "number" },
            "title": {"type": "string"},
            "description": {"type": "string"},
            "start_time": {"type": "string"},
            "end_time": {"type": "string"},
            "location": {"type": "string"}
          },
            "required": ["id"],
        }
      }
    },
]
def query_ollama3(prompt: str, user_text, model: str = OLLAMA_MODEL):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text},
        ],
        "stream": False,
        "tools": tools3
    }
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=True
    )

    response.raise_for_status()

    data = response.json()
    message = data.get("message", {})

    if message.get("tool_calls"):
        return {
            "type": "tool_call",
            "tool_calls": message["tool_calls"]
        }

    return {
        "type": "message",
        "content": message.get("content", "").strip()
    }