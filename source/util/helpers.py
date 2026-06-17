def summarize_calendar_events(events):
    if not events:
        return "No calendar events found."

    # Sort safely by start_time
    def sort_key(e):
        if isinstance(e, dict):
            return e.get("start_time") or ""
        return ""

    events = sorted(events, key=sort_key)

    lines = []

    for e in events:
        if not isinstance(e, dict):
            continue

        event_id = e.get("id", "unknown")
        title = e.get("title") or "Untitled event"

        start = e.get("start_time")
        end = e.get("end_time")

        date_part = ""
        time_part = ""

        start_time = None

        if start and "T" in start:
            date, start_time = start.split("T", 1)
            date_part = f"on {date}"
            time_part = f"at {start_time}"

        if start_time and end and "T" in end:
            end_time = end.split("T", 1)[1]
            time_part = f"from {start_time} to {end_time}"

        location = e.get("location")
        location_part = f"at {location}" if location else ""

        # 🚫 Removed quotes around title
        sentence_parts = [
            f'- Event ID {event_id}: {title}',
            date_part,
            time_part,
            location_part
        ]

        sentence = " ".join(part for part in sentence_parts if part)
        lines.append(sentence.strip() + ".")

    return "\n".join(lines)


def delete_event_by_id(event_id):
    file_path = "../database/conversation_history.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    event_id_str = f"Event ID {event_id}:"
    indices_to_delete = set()

    for i, item in enumerate(data):
        # Find assistant message that mentions this event
        if (
            item.get("role") == "assistant"
            and event_id_str in item.get("content", "")
        ):
            indices_to_delete.add(i)

            # Also delete the immediately previous user message (if any)
            if i - 1 >= 0 and data[i - 1].get("role") == "user":
                indices_to_delete.add(i - 1)

    # Rebuild history excluding marked indices
    new_data = [
        item for idx, item in enumerate(data)
        if idx not in indices_to_delete
    ]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

import json

def update_summary_in_conversation_file(
    event_id,
    new_summary
):
    """
    Replace the assistant summary for a given Event ID
    inside a conversation JSON file.
    """
    file_path = "../database/conversation_history.json"
    with open(file_path, "r") as f:
        conversation = json.load(f)

    event_marker = f"Event ID {event_id}:"
    updated = False

    for item in conversation:
        if (
            item.get("role") == "assistant"
            and event_marker in item.get("content", "")
        ):
            item["content"] = new_summary
            updated = True
            break

    if not updated:
        return False

    with open(file_path, "w") as f:
        json.dump(conversation, f, indent=2)

    return True

DELETE_KEYWORDS = {
    "delete",
    "remove",
    "cancel",
    "discard",
    "erase",
    "change",
    "update",
    "modify"
}

def is_delete_intent(user_text: str) -> bool:
    text = user_text.lower()
    return any(keyword in text for keyword in DELETE_KEYWORDS)