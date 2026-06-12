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
[![Admin Panel](https://img.shields.io/badge/Admin-Panel-9c27b0?style=for-the-badge&logo=googlechrome&logoColor=white)](app/static/admin.html)

🇩🇪 Deutsch | [🇬🇧 English](README_EN.md)

</div>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Kalender** | Mehrere Kalender via OAuth2 Refresh Token, alle 5 Min aktualisiert |
| 🌤️ **Wetter** | OpenWeatherMap API, Echtzeit, auf Deutsch |
| 🕐 **Uhrzeit & Datum** | Sekundengenau, deutsche Lokalisierung |
| 🖼️ **Hintergrundwechsel** | Unsplash oder eigene Bilder, Intervall einstellbar |
| 🐳 **Docker-Ready** | Läuft als Container, Port `4455` |
| 🔒 **Sicher** | `.env` nie im Repo, Refresh Token lokal |
| 🏠 **Self-Hosted** | Kein Cloud-Abo, kein Tracking |
| 🛠️ **Admin-Panel** | Passwortgeschütztes Web-UI unter `/admin` |

---

## 🛠️ Admin-Panel

Erreichbar unter **`http://deine-ip:4455/admin`** – passwortgeschützt via `ADMIN_PASSWORD` in der `.env`.

| Bereich | Funktion |
|---|---|
| 📊 **Dashboard** | Status-Übersicht aller Konfigurationspunkte |
| 🔑 **Google Auth** | Client ID/Secret eintragen, OAuth-Flow starten, Token testen |
| 🗓️ **Kalender** | Verfügbare Kalender laden, per Toggle auswählen |
| 🎨 **Design** | Schriftart, -größe, Akzentfarbe, Layout, Termin-Stil |
| 🖼️ **Hintergründe** | Unsplash-Query, eigene Bilder per Drag & Drop, Helligkeit & Intervall |
| ⚙️ **Anzeige** | Wetter / Kalender / Sekunden ein-/ausblenden |
| 🌤️ **Wetter** | Stadt und OpenWeatherMap API Key setzen |

> Alle Einstellungen werden in `/data/settings.json` (Docker Volume) persistent gespeichert.

---

## 🚀 Installation

> Es gibt **drei Wege** – wähle den für dich passenden:

### 🐳 Option 1 – Docker CLI (empfohlen)

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
cp .env.example .env
joe .env                        # echte Werte eintragen
docker compose up -d --build
docker logs -f hAI-CalBoard
```

> 📍 Dashboard: `http://deine-ip:4455` · Admin: `http://deine-ip:4455/admin`

---

### 📦 Option 2 – Portainer (Stack)

1. **Portainer** → `Stacks` → `+ Add Stack`
2. **Name:** `hAI-CalBoard`
3. **Git Repository** → URL: `https://github.com/jbkunama1/hAI.CalBoard` · Compose-Pfad: `docker-compose.yml`
4. **Environment Variables** eintragen:

   | Variable | Wert |
   |---|---|
   | `GOOGLE_CLIENT_ID` | `dein_client_id` |
   | `GOOGLE_CLIENT_SECRET` | `dein_secret` |
   | `GOOGLE_REFRESH_TOKEN` | `dein_refresh_token` |
   | `CALENDAR_IDS` | `primary` |
   | `OPENWEATHER_API_KEY` | `dein_key` |
   | `CITY` | `Pfinztal` |
   | `ADMIN_PASSWORD` | `dein_sicheres_passwort` |
   | `SECRET_KEY` | `zufaelliger_langer_string` |

5. → **Deploy the stack**

> 💡 Alternativ: Inhalt von `docker-compose.yml` direkt einfügen, kein Git-Zugriff nötig.

---

### 🔧 Option 3 – Manuell / Bare Metal

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
pip install flask requests flask-cors gunicorn werkzeug
cp .env.example .env && source .env
cd app && gunicorn --bind 0.0.0.0:4455 server:app
```

---

## 🔑 Google OAuth Setup

> Einmalig nötig – danach automatisch via Refresh Token. **Empfohlen: direkt im Admin-Panel unter `/admin` → Google Auth.**

```
1. 🌐  https://console.cloud.google.com → Neues Projekt
2. 📅  Google Calendar API aktivieren
3. 🔐  OAuth 2.0 Client ID (Web) erstellen
       Redirect URI: http://deine-ip:4455/api/admin/oauth/callback
4. 🛠️  Im Admin-Panel: Client ID & Secret eintragen → "Mit Google anmelden"
5. ✅  Refresh Token wird automatisch gespeichert
```

> Alternativ manuell über [OAuth Playground](https://developers.google.com/oauthplayground) mit Scope `https://www.googleapis.com/auth/calendar.readonly`.

---

## ⚙️ Umgebungsvariablen

> Vorlage: [`.env.example`](.env.example)

| Variable | Pflicht | Beispiel | Beschreibung |
|---|:---:|---|---|
| `GOOGLE_CLIENT_ID` | ✅ | `123...apps.googleusercontent.com` | OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | ✅ | `GOCSPX-...` | OAuth Client Secret |
| `GOOGLE_REFRESH_TOKEN` | ⚠️ | `1//04...` | Refresh Token (via Admin-Panel oder manuell) |
| `CALENDAR_IDS` | ⚠️ | `primary,work@gmail.com` | Fallback, wird im Admin überschrieben |
| `OPENWEATHER_API_KEY` | ✅ | `abc123...` | Kostenlos auf openweathermap.org |
| `CITY` | ✅ | `Pfinztal` | Stadt für Wetteranzeige |
| `ADMIN_PASSWORD` | ✅ | `sicheres_passwort` | Zugang zum Admin-Panel |
| `SECRET_KEY` | ✅ | `langer_zufaelliger_string` | Flask Session-Key |

---

## 🗂️ Projektstruktur

```
hAI.CalBoard/
├── 🐳 docker-compose.yml
├── 🐋 Dockerfile
├── 🔒 .env.example
├── 🚫 .gitignore
├── 📄 demo.html                # Offline-Demo mit Beispieldaten
└── 📁 app/
    ├── 🐍 server.py            # Flask-Backend (API + Admin-Routen)
    └── 📁 static/
        ├── 🌐 index.html       # Dashboard (DE)
        ├── 🌐 index_en.html    # Dashboard (EN)
        ├── 🛠️ admin.html       # Admin-Panel
        └── 📄 demo.html        # Demo
```

---

## 🔄 Update-Intervalle

```
🕐 Uhrzeit        →  jede Sekunde
🌤️ Wetter         →  alle 10 Minuten
🗓️ Kalender       →  alle 5 Minuten
🖼️ Hintergrund    →  konfigurierbar (Standard: 30 Min)
```

---

## 🛠️ Troubleshooting

| Problem | Lösung |
|---|---|
| Container startet nicht | `docker logs hAI-CalBoard` prüfen |
| Admin-Login schlägt fehl | `ADMIN_PASSWORD` in `.env` prüfen |
| Kalender leer | Im Admin → Google Auth → Verbindung testen |
| Wetter lädt nicht | API Key im Admin → Wetter eintragen |
| Port 4455 belegt | `docker-compose.yml` → Port anpassen |
| Portainer: Build schlägt fehl | `Dockerfile` muss im Repo-Root liegen |
| Einstellungen gehen verloren | Docker Volume `calboard_data` prüfen |

---

## 📝 DietPi / Kiosk-Betrieb

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/calboard.desktop << EOF
[Desktop Entry]
Type=Application
Name=hAI.CalBoard
Exec=bash -c "sleep 10 && firefox --kiosk http://localhost:4455"
EOF
```

---

## 📄 Lizenz

[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

```
MIT License – © 2026 Daniel Lienhard
```

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
