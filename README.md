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
[![Self-Hosted](https://img.shields.io/badge/Self--Hosted-%E2%9C%94-brightgreen?style=for-the-badge)](https://github.com/jbkunama1/hAI.CalBoard)
[![Admin Panel](https://img.shields.io/badge/Admin-Panel-9c27b0?style=for-the-badge&logo=googlechrome&logoColor=white)](app/static/admin.html)

🇩🇪 Deutsch | [🇬🇧 English](README_EN.md)

</div>

---

## ⚡ Schnellstart (3 Schritte)

> **Kurze Antwort auf die häufigste Frage:**
> Die `.env` braucht beim ersten Start **nur 2 Einträge**.
> Google, Wetter und Kalender richtest du danach bequem **im Admin-Panel** ein.

### Schritt 1 – Minimale `.env` anlegen

```bash
cp .env.example .env
```

Dann `.env` öffnen und **nur diese zwei Zeilen** mit echten Werten füllen:

```env
ADMIN_PASSWORD=dein_sicheres_passwort
SECRET_KEY=irgendein_langer_zufaelliger_string_mindestens_32_zeichen
```

> Alle anderen Variablen (`GOOGLE_*`, `OPENWEATHER_API_KEY`, `CITY` etc.) **leer lassen oder ganz weglassen** –
> sie werden später im Admin-Panel eingetragen und dort gespeichert.

### Schritt 2 – Container starten

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
docker compose up -d --build
```

### Schritt 3 – Browser öffnen

```
http://deine-ip:4455
```

Da du noch nichts konfiguriert hast, leitet der Server dich **automatisch zu `/admin` weiter**.
Dort loggst du dich mit deinem `ADMIN_PASSWORD` ein und richtest alles ein.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Kalender** | Mehrere Kalender via OAuth2 Refresh Token, alle 5 Min aktualisiert |
| 🌤️ **Wetter** | OpenWeatherMap API, Echtzeit, auf Deutsch |
| 🕐 **Uhrzeit & Datum** | Sekundengenau, deutsche Lokalisierung |
| 🖼️ **Hintergrundwechsel** | Unsplash oder eigene Bilder, Intervall einstellbar |
| 🐳 **Docker-Ready** | Läuft als Container, Port `4455` |
| 🔒 **Sicher** | `.env` nie im Repo, Refresh Token lokal, kein Fallback-Passwort |
| 🏠 **Self-Hosted** | Kein Cloud-Abo, kein Tracking |
| 🛠️ **Admin-Panel** | Passwortgeschütztes Web-UI unter `/admin` |

---

## 🛠️ Admin-Panel

Erreichbar unter **`http://deine-ip:4455/admin`** – passwortgeschützt via `ADMIN_PASSWORD`.

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

## 🔑 Google OAuth einrichten (im Admin-Panel)

> Einmalig nötig – danach läuft alles automatisch über den Refresh Token.
> **Du brauchst keinen OAuth Playground und kein manuelles Token-Kopieren.**

### Vorbereitung: Google Cloud Console (~5 Min)

```
1. https://console.cloud.google.com → Neues Projekt anlegen
2. APIs & Dienste → Bibliothek → „Google Calendar API“ aktivieren
3. APIs & Dienste → Anmeldedaten → „Anmeldedaten erstellen“ → „OAuth-Client-ID“
   └─ Anwendungstyp: Webanwendung
   └─ Autorisierte Weiterleitungs-URI:
      http://deine-ip:4455/api/admin/oauth/callback
4. Client ID und Client Secret kopieren
```

### Im Admin-Panel einrichten

```
1. http://deine-ip:4455/admin → Einloggen
2. Bereich „Google Auth“ öffnen
3. Client ID und Client Secret eintragen → Speichern
4. Schaltfläche „Mit Google anmelden“ klicken
   └─ Google-Fenster öffnet sich
   └─ Dein Google-Konto auswählen + Kalender-Zugriff bestätigen
5. ✅ Fertig – der Refresh Token wird automatisch gespeichert
6. „Verbindung testen“ klicken um zu prüfen ob alles funktioniert
```

> **Wichtig:** Die Redirect URI in der Google Cloud Console muss exakt mit deiner IP/Domain übereinstimmen.
> Für Portainer/NAS: `http://192.168.x.x:4455/api/admin/oauth/callback` verwenden.

---

## 🌤️ Wetter einrichten

```
1. Kostenloser Account auf https://openweathermap.org
2. API → API Keys → Key kopieren
3. Im Admin-Panel → Wetter → API Key + Stadt eintragen → Speichern
```

> Der Gratis-Plan reicht völlig aus (1.000 Anfragen/Tag, Update alle 10 Min).

---

## ⚙️ Alle Umgebungsvariablen

> Vorlage: [`.env.example`](.env.example)

| Variable | Pflicht | Beschreibung |
|---|:---:|---|
| `ADMIN_PASSWORD` | ✅ **Muss gesetzt sein** | Zugang zum Admin-Panel |
| `SECRET_KEY` | ✅ **Muss gesetzt sein** | Flask Session-Key (mind. 32 zufällige Zeichen) |
| `GOOGLE_CLIENT_ID` | ⭕ Optional | Kann auch im Admin-Panel eingetragen werden |
| `GOOGLE_CLIENT_SECRET` | ⭕ Optional | Kann auch im Admin-Panel eingetragen werden |
| `GOOGLE_REFRESH_TOKEN` | ⭕ Optional | Wird automatisch per OAuth generiert |
| `CALENDAR_IDS` | ⭕ Optional | Wird im Admin-Panel überschrieben |
| `OPENWEATHER_API_KEY` | ⭕ Optional | Kann auch im Admin-Panel eingetragen werden |
| `CITY` | ⭕ Optional | Standard: `Pfinztal`, im Admin anpassbar |

> ⚠️ Der Container **startet nicht**, wenn `ADMIN_PASSWORD` oder `SECRET_KEY` fehlen.
> Alle anderen Variablen sind wirklich optional.

---

## 🚀 Weitere Installationswege

### 📦 Portainer (Stack)

1. **Portainer** → `Stacks` → `+ Add Stack`
2. **Name:** `hAI-CalBoard`
3. **Git Repository** → URL: `https://github.com/jbkunama1/hAI.CalBoard` · Compose-Pfad: `docker-compose.yml`
4. **Environment Variables** – mindestens:

   | Variable | Wert |
   |---|---|
   | `ADMIN_PASSWORD` | `dein_sicheres_passwort` |
   | `SECRET_KEY` | `langer_zufaelliger_string` |

5. → **Deploy the stack**
6. Google + Wetter danach im Admin-Panel eintragen.

### 🔧 Bare Metal

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
pip install -r requirements.txt
cp .env.example .env   # ADMIN_PASSWORD + SECRET_KEY setzen
export $(cat .env | xargs)
cd app && gunicorn --bind 0.0.0.0:4455 server:app
```

---

## 🗂️ Projektstruktur

```
hAI.CalBoard/
├── 🐳 docker-compose.yml      # inkl. Healthcheck
├── 🐋 Dockerfile
├── 🔒 .env.example             # Vorlage – nur 2 Pflichtfelder!
├── 📄 requirements.txt         # für Bare-Metal-Installation
├── 📜 CHANGELOG.md
├── 📁 scripts/
│   ├── kiosk.sh                 # Kiosk-Startskript (DietPi/LXDE)
│   └── autostart.desktop        # Autostart-Eintrag
└── 📁 app/
    ├── 🐍 server.py              # Flask-Backend
    └── 📁 static/
        ├── index.html             # Dashboard (DE)
        ├── index_en.html          # Dashboard (EN)
        └── admin.html             # Admin-Panel
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
| Container startet nicht | `docker logs hAI-CalBoard` – fehlt `ADMIN_PASSWORD` oder `SECRET_KEY`? |
| Admin-Login schlägt fehl | `ADMIN_PASSWORD` in `.env` prüfen |
| Kalender leer | Admin → Google Auth → Verbindung testen |
| Wetter lädt nicht | Admin → Wetter → API Key + Stadt prüfen |
| Port 4455 belegt | `docker-compose.yml` → Port anpassen |
| OAuth schlägt fehl | Redirect URI in Google Cloud Console prüfen (exakte IP!) |
| Einstellungen gehen verloren | Docker Volume `calboard_data` prüfen |

---

## 📺 DietPi / Kiosk-Betrieb

```bash
# Skript nutzen:
bash scripts/kiosk.sh

# Oder Autostart einrichten:
mkdir -p ~/.config/autostart
cp scripts/autostart.desktop ~/.config/autostart/
# Pfad in autostart.desktop ggf. anpassen
```

---

## 📝 Lizenz

[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

```
MIT License – © 2026 Daniel Lienhard
```

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
