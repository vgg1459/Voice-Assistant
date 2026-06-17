import requests

URL = "https://api.responsible-nlp.net/calendar.php"
calenderid = "sps123"


def create_calendar_event(payload):
    try:
        params = {"calenderid": calenderid}
        response = requests.post(
            URL,
            params=params,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def list_calendar_events():
    try:
        params = {"calenderid": calenderid}
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_calendar_event(event_id):
    try:
        params = {
            "calenderid": calenderid,
            "id": event_id
        }
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def update_calendar_event(payload):
    try:
        entry_id = payload.pop("id")
        params = {
            "calenderid": calenderid,
            "id": entry_id
        }
        response = requests.put(
            URL,
            params=params,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def delete_calendar_event(payload):
    try:
        entry_id = payload.pop("id")
        params = {
            "calenderid": calenderid,
            "id": entry_id
        }
        response = requests.delete(URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
