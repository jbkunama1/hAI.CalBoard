# 🖥️ hAI.CalBoard

<div align="center">

![hAI.CalBoard Logo](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/efe4dd3d-88a7-4f27-ace9-72f4ef2db416.png)

**Self-hosted Smart Home Dashboard** – Google Kalender · Wetter · Uhrzeit · Hintergrundwechsel

---

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](Dockerfile)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](app/server.py)
[![Port](https://img.shields.io/badge/Port-4455-FF6B6B?style=for-the-badge&logo=googlechrome&logoColor=white)](docker-compose.yml)
[![Google Calendar](https://img.shields.io/badge/Google%20Calendar-API-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://developers.google.com/calendar)
[![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-EB6E4B?style=for-the-badge&logo=openweathermap&logoColor=white)](https://openweathermap.org)
[![Self-Hosted](https://img.shields.io/badge/Self--Hosted-✔-brightgreen?style=for-the-badge)](https://github.com/jbkunama1/hAI.CalBoard)

</div>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Kalender** | Mehrere Kalender via OAuth2 Refresh Token, alle 5 Min aktualisiert |
| 🌤️ **Wetter** | OpenWeatherMap API, Echtzeit, auf Deutsch |
| 🕐 **Uhrzeit & Datum** | Sekundengenau, deutsche Lokalisierung |
| 🖼️ **Hintergrundwechsel** | Unsplash Random, alle 30 Minuten |
| 🐳 **Docker-Ready** | Läuft als Container, Port `4455` |
| 🔒 **Sicher** | `.env` nie im Repo, Refresh Token lokal |
| 🏠 **Self-Hosted** | Kein Cloud-Abo, kein Tracking |

---

## 🚀 Installation

> Es gibt **drei Wege**, hAI.CalBoard zu installieren – wähle den für dich passenden:

---

### 🐳 Option 1 – Docker CLI (empfohlen)

```bash
# 1. Repo klonen
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard

# 2. Umgebungsvariablen setzen
cp .env.example .env
joe .env   # oder nano / vim

# 3. Container bauen & starten
docker compose up -d --build

# 4. Logs prüfen
docker logs -f hAI-CalBoard
```

> 📍 Aufruf: `http://deine-ip:4455`

---

### 📦 Option 2 – Portainer (Stack)

1. **Portainer öffnen** → `Stacks` → `+ Add Stack`
2. **Name:** `hAI-CalBoard`
3. **Repository-Methode wählen:**
   - → `Git Repository`
   - URL: `https://github.com/jbkunama1/hAI.CalBoard`
   - Compose-Pfad: `docker-compose.yml`
4. **Environment Variables** eintragen (unter "Environment variables" im Stack-Editor):

   | Variable | Wert |
   |---|---|
   | `GOOGLE_CLIENT_ID` | `dein_client_id` |
   | `GOOGLE_CLIENT_SECRET` | `dein_secret` |
   | `GOOGLE_REFRESH_TOKEN` | `dein_refresh_token` |
   | `CALENDAR_IDS` | `primary` |
   | `OPENWEATHER_API_KEY` | `dein_key` |
   | `CITY` | `Pfinztal` |

5. → **Deploy the stack** klicken
6. Unter `Containers` → `hAI-CalBoard` → Port `4455` anklicken oder direkt aufrufen

> 💡 **Alternativ:** Im Portainer Stack-Editor einfach den Inhalt von `docker-compose.yml` einfügen und die Variablen manuell als Env-Vars setzen – kein Git-Zugriff nötig.

---

### 🔧 Option 3 – Manuell ohne Docker (Bare Metal / Entwicklung)

> Nützlich für lokales Testen oder wenn kein Docker verfügbar ist.

```bash
# 1. Repo klonen
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard

# 2. Python-Abhängigkeiten installieren
pip install flask requests flask-cors gunicorn

# 3. Umgebungsvariablen setzen
cp .env.example .env
source .env   # oder export VAR=wert einzeln

# 4. Server starten
cd app
python server.py

# alternativ mit Gunicorn (produktionsreifer):
gunicorn --bind 0.0.0.0:4455 server:app
```

> 📍 Aufruf: `http://localhost:4455`

---

## 🔑 Google OAuth Setup

> Einmalig nötig – danach läuft alles automatisch über den Refresh Token.

```
1. 🌐  Google Cloud Console → Neues Projekt anlegen
       https://console.cloud.google.com

2. 📅  Google Calendar API aktivieren
       APIs & Dienste → Bibliothek → "Google Calendar API"

3. 🔐  OAuth 2.0 Client ID erstellen
       Typ: Web-Anwendung
       Redirect URI: https://developers.google.com/oauthplayground

4. 🎮  OAuth Playground öffnen
       https://developers.google.com/oauthplayground
       ⚙️ Einstellungen → "Use your own OAuth credentials"
       Scope: https://www.googleapis.com/auth/calendar.readonly

5. ✅  Authorize → Exchange → Refresh Token kopieren → in .env eintragen
```

---

## ⚙️ Umgebungsvariablen

> Vorlage: [`.env.example`](.env.example)

| Variable | Pflicht | Beispiel | Beschreibung |
|---|:---:|---|---|
| `GOOGLE_CLIENT_ID` | ✅ | `123...apps.googleusercontent.com` | OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | ✅ | `GOCSPX-...` | OAuth Client Secret |
| `GOOGLE_REFRESH_TOKEN` | ✅ | `1//04...` | Refresh Token (einmalig generiert) |
| `CALENDAR_IDS` | ✅ | `primary,work@gmail.com` | Kommagetrennte Kalender-IDs |
| `OPENWEATHER_API_KEY` | ✅ | `abc123...` | Kostenlos auf openweathermap.org |
| `CITY` | ✅ | `Pfinztal` | Stadt für Wetteranzeige |

---

## 🗂️ Projektstruktur

```
hAI.CalBoard/
├── 🐳 docker-compose.yml      # Container-Definition (Port 4455)
├── 🐋 Dockerfile               # Python 3.11 + Flask + Gunicorn
├── 🔒 .env.example             # Vorlage für Umgebungsvariablen
├── 🚫 .gitignore               # .env wird nicht eingecheckt
└── 📁 app/
    ├── 🐍 server.py            # Flask-Backend (Calendar & Weather API)
    └── 📁 static/
        ├── 🌐 index.html       # Dashboard-Layout
        ├── 🎨 style.css        # Dark Overlay + Glassmorphism
        └── ⚡ app.js           # Frontend-Logik + Polling
```

---

## 🔄 Update-Intervalle

```
🕐 Uhrzeit        →  jede Sekunde
🌤️ Wetter         →  alle 10 Minuten
🗓️ Kalender       →  alle 5 Minuten
🖼️ Hintergrund    →  alle 30 Minuten
```

---

## 🛠️ Troubleshooting

| Problem | Lösung |
|---|---|
| Container startet nicht | `docker logs hAI-CalBoard` prüfen |
| Kalender leer | Refresh Token abgelaufen → neu generieren |
| Wetter lädt nicht | API Key prüfen, `CITY` korrekt schreiben |
| Port 4455 belegt | `docker-compose.yml` → Port ändern |
| Hintergrund lädt nicht | Unsplash-URL im Browser testen |
| Portainer: Build schlägt fehl | Sicherstellen, dass `Dockerfile` im Repo-Root liegt |
| Bare Metal: ImportError | `pip install flask requests flask-cors gunicorn` wiederholen |

---

## 📝 Tipps für DietPi / Kiosk-Betrieb

```bash
# Firefox im Kiosk-Modus auf LXDE-Autostart
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/calboard.desktop << EOF
[Desktop Entry]
Type=Application
Name=hAI.CalBoard
Exec=bash -c "sleep 10 && firefox --kiosk http://localhost:4455"
EOF
```

> 💡 `sleep 10` gibt dem Container Zeit zum Starten bevor der Browser öffnet.

---

## 📄 Lizenz

```
MIT License – © 2026 Daniel Lienhard
```

[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
