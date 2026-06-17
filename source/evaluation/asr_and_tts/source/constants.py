WEATHER_KEYWORDS = {
    "weather", "rain", "snow", "sun", "sunny", "cloud", "cloudy",
    "storm", "wind", "windy", "temperature", "hot", "cold", "warm",
    "forecast", "humidity", "mist", "fog", "drizzle", "thunder"
}

DAYS = {
    "today", "tomorrow", "tonight",
    "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday"
}

def extract_day(doc, place):
    for token in doc:
        if token.lemma_.lower() in DAYS:
            return token.lemma_.lower()
    if place == "previous":
        return "previous"
    else:
        return "today"

def extract_place(doc):
    for ent in doc.ents:
        if ent.label_ in {"GPE", "LOC"}:
            return ent.text
    return "previous"

def is_weather_query(doc):
    return any(token.lemma_ in WEATHER_KEYWORDS for token in doc)