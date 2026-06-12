# hAI.CalBoard

> Self-hosted DAKboard-Klon mit Google Calendar API, Wetter, Uhrzeit & wechselnden Hintergründen – als Docker-Container auf Port 4455.

## Features

- 🗓️ Google Kalender (mehrere Kalender via OAuth2 Refresh Token)
- 🌤️ Wetter via OpenWeatherMap
- 🕐 Uhrzeit & Datum (Deutsch)
- 🖼️ Hintergrundwechsel alle 30 Minuten (Unsplash)
- 🐳 Docker-Container, Port 4455

## Schnellstart

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
cp .env.example .env
# .env mit echten Werten befüllen
docker compose up -d
```

Dann unter `http://deine-ip:4455` aufrufen.

## Google OAuth Setup

1. [Google Cloud Console](https://console.cloud.google.com) → Neues Projekt
2. Google Calendar API aktivieren
3. OAuth 2.0 Client ID erstellen (Web, Redirect: `https://developers.google.com/oauthplayground`)
4. [OAuth Playground](https://developers.google.com/oauthplayground) → eigene Credentials → Scope: `https://www.googleapis.com/auth/calendar.readonly`
5. Authorize → Exchange → **Refresh Token** in `.env` eintragen

## Umgebungsvariablen

| Variable | Beschreibung |
|---|---|
| `GOOGLE_CLIENT_ID` | OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | OAuth Client Secret |
| `GOOGLE_REFRESH_TOKEN` | Refresh Token |
| `CALENDAR_IDS` | Kommagetrennte Kalender-IDs |
| `OPENWEATHER_API_KEY` | API Key von openweathermap.org |
| `CITY` | Stadt für Wetter (z.B. `Pfinztal`) |

## Lizenz

MIT License – © 2026 Daniel Lienhard
