from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests, os
from datetime import datetime, timezone

app = Flask(__name__, static_folder='static')
CORS(app)

def get_access_token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
        "grant_type": "refresh_token"
    })
    return r.json().get("access_token")

@app.route("/api/calendar")
def calendar():
    token = get_access_token()
    cal_ids = os.environ.get("CALENDAR_IDS", "primary").split(",")
    events = []
    now = datetime.now(timezone.utc).isoformat()
    for cal_id in cal_ids:
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_id.strip()}/events"
        params = {
            "timeMin": now,
            "maxResults": 10,
            "singleEvents": True,
            "orderBy": "startTime"
        }
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params)
        data = r.json()
        for item in data.get("items", []):
            events.append({
                "title": item.get("summary", ""),
                "start": item.get("start", {}).get("dateTime") or item.get("start", {}).get("date"),
                "end": item.get("end", {}).get("dateTime") or item.get("end", {}).get("date"),
                "calendar": cal_id.strip()
            })
    events.sort(key=lambda x: x["start"] or "")
    return jsonify(events)

@app.route("/api/weather")
def weather():
    key = os.environ.get("OPENWEATHER_API_KEY")
    city = os.environ.get("CITY", "Karlsruhe")
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric&lang=de")
    d = r.json()
    return jsonify({
        "temp": round(d["main"]["temp"]),
        "feels_like": round(d["main"]["feels_like"]),
        "description": d["weather"][0]["description"],
        "icon": d["weather"][0]["icon"],
        "city": d["name"]
    })

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)
