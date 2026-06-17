from services.weather_history import add_weather_history
from source.constants import is_weather_query
from source.services.weather_history import add_conversation_history
from source.util.prompts import initial_extract_prompt, weather_response_prompt, initial_extract_prompt2, \
    calendar_response_prompt3, calendar_response_prompt2
from source.services.weather import get_weather_forecast
from datetime import datetime

from source.util.ask_llm import query_ollama, query_ollama2, query_ollama3
from source.services.calender import (
    list_calendar_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event, get_calendar_event,
)
from source.util.helpers import summarize_calendar_events, delete_event_by_id, update_summary_in_conversation_file, \
    is_delete_intent
import spacy

nlp = spacy.load("en_core_web_sm")

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def get_current_day_name():
    return datetime.now().strftime("%A")

def get_calendar_or_chat(user_text: str) -> str:
    doc = nlp(user_text)
    if is_weather_query(doc):
        print("is weather query is true")
        day = get_current_day_name()
        raw = query_ollama(initial_extract_prompt2(), user_text, "weather")
        print("raw", raw)
        if raw["type"] == "tool_call":
            call = raw["tool_calls"][0]
            tool_name = call["function"]["name"]
            if tool_name == "get_weather":
                args = call["function"]["arguments"]
                print(args["place"])
                tool_output = get_weather_forecast(args["place"])
                print(tool_output)
                prompt = weather_response_prompt(user_text, tool_output, day)
                response = query_ollama2(prompt, user_text)
                add_weather_history("user", user_text)
                add_weather_history("assistant", response)
                return response
        else:
            message = raw["content"]
            return message
    events = list_calendar_events()
    events_summary = summarize_calendar_events(events)
    print("events_summary")
    print(events_summary)
    prompt = initial_extract_prompt(get_current_datetime())
    raw = query_ollama(prompt, user_text, "calender")
    print("initial response", raw)

    if raw["type"] == "tool_call":
        call = raw["tool_calls"][0]
        tool_name = call["function"]["name"]
        if tool_name == "create_calendar_event":
            args = call["function"]["arguments"]
            tool_output = create_calendar_event(args)
            print("tool_output", tool_output)
            message = f"Your appointment titled {tool_output['title']} has been created!"
            events = list_calendar_events()
            event_summary = summarize_calendar_events([events[-1]])
            reply = message
            add_conversation_history("user", user_text)
            add_conversation_history("assistant", event_summary)
            return reply
        elif tool_name == "delete_calendar_event":
            args = call["function"]["arguments"]
            id = call["function"]["arguments"]["id"]
            tool_output = delete_calendar_event(args)
            reply = "Your mentioned event has been deleted!"
            delete_event_by_id(id)
            print(tool_output)
            return reply
        elif tool_name == "update_calendar_event":
            id = call["function"]["arguments"]["id"]
            args = call["function"]["arguments"]
            tool_output = update_calendar_event(args)
            reply = "Your meeting has been updated!"
            print(tool_output)
            event = get_calendar_event(id)
            new_sum = summarize_calendar_events([event])
            update_summary_in_conversation_file(id, new_sum)
            return reply
        elif tool_name == "list_calendar_events":
            events = list_calendar_events()
            events_summary = summarize_calendar_events(events)
            if is_delete_intent(user_text):
                prompt = calendar_response_prompt3(get_current_datetime(), events_summary)
                raw = query_ollama3(prompt, user_text)
                call = raw["tool_calls"][0]
                tool_name = call["function"]["name"]
                print("initial response", raw)
                if tool_name == "delete_calendar_event":
                    args = call["function"]["arguments"]
                    id = call["function"]["arguments"]["id"]
                    tool_output = delete_calendar_event(args)
                    reply = "Your mentioned event has been deleted!"
                    delete_event_by_id(id)
                    print(tool_output)
                elif tool_name == "update_calendar_event":
                    id = call["function"]["arguments"]["id"]
                    args = call["function"]["arguments"]
                    tool_output = update_calendar_event(args)
                    reply = "Your meeting has been updated!"
                    print(tool_output)
                    event = get_calendar_event(id)
                    new_sum = summarize_calendar_events([event])
                    update_summary_in_conversation_file(id, new_sum)
                else:
                    message = raw["content"]
                    return message
                return reply
            else:
                prompt = calendar_response_prompt2(get_current_datetime(), events_summary)
                reply = query_ollama2(prompt, user_text)
            return reply
    else:
        message = raw["content"]
        return message

if __name__ == "__main__":
    import time

    start = time.perf_counter()
    # result = get_calendar_or_chat(" What is weather in Berlin on Friday ?")
    # result = get_calendar_or_chat("What will it rain there on monday?")
    # result =   get_weather_or_chat("How are you?")
    # result = get_calendar_or_chat("add a meeting for timepass at a 8 PM tomorrow.")
    result = get_calendar_or_chat("Tell me all my meetings tomorrow")
    # result = get_calendar_or_chat("what are my calendar events for tomorrow?")
    # result = get_calendar_or_chat("Where is my next appointment?")
    # result = get_calendar_or_chat("give my calendar events for next two days.")
    # result = get_calendar_or_chat("Create a reminder for Project Submission at 5PM on 2nd February")
    # result = get_calendar_or_chat("Delete my appointment with professor")
    # result = get_calendar_or_chat("Update time for my of my Meeting with professor to 7PM to 8PM")
    # result = get_calendar_or_chat("Change location of my appointment with Professor to University")
    # result = get_calendar_or_chat("Update description of meeting seminar to mandatory attendance")
    # result = get_calendar_or_chat("Delete the previously created appointment")
    # result = get_calendar_or_chat( " add an event for titled Seminar from 1PM to 2PM  for tomorrow in University")
    # result = get_calendar_or_chat( "Set up a meeting for discussion with team at 5PM on 1st February for an hour")
    print("final response")
    print(result)
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds")