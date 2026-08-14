# 🖥️ hAI.CalBoard

[![Buy me a coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/highfish)

<div align="center">

![hAI.CalBoard Logo](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/efe4dd3d-88a7-4f27-ace9-72f4ef2db416.png)

**Self-hosted Smart Home Dashboard** – Google Kalender · Wetter · Uhrzeit · Hintergrundwechsel · Theme-System

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

> Die `.env` braucht beim ersten Start **nur 2 Einträge**.
> Google, Wetter, Kalender und Themes richtest du danach im **Admin-Panel** ein.

### Schritt 1 – Minimale `.env` anlegen

```bash
cp .env.example .env
```

Dann `.env` öffnen und **nur diese zwei Zeilen** mit echten Werten füllen:

```env
ADMIN_PASSWORD=dein_sicheres_passwort
SECRET_KEY=irgendein_langer_zufaelliger_string_mindestens_32_zeichen
```

> Alle anderen Variablen (`GOOGLE_*`, `OPENWEATHER_API_KEY`, `CITY` etc.) können leer bleiben oder ganz weggelassen werden.

### Schritt 2 – Container starten

```bash
# Optional: create the external network if it does not exist
# docker network create highfishNetwork

git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
docker compose up -d
```

> Das fertige Image wird automatisch aus der **GitHub Container Registry** gezogen
> (`ghcr.io/jbkunama1/hai.calboard:latest`) – kein Build vor Ort nötig.
> Für einen lokalen Build: `build: .` in `docker-compose.yml` einkommentieren,
> dann `docker compose up -d --build` nutzen.

### Schritt 3 – Browser öffnen

```
http://deine-ip:4455
```

Wenn noch nichts eingerichtet ist, leitet der Server automatisch auf **`/admin`** weiter.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Kalender** | Mehrere Kalender via OAuth2 Refresh Token, alle 5 Min aktualisiert |
| 🌤️ **Wetter** | OpenWeatherMap API, Echtzeit, auf Deutsch |
| 🕐 **Uhrzeit & Datum** | Sekundengenau, deutsche Lokalisierung |
| 🖼️ **Hintergrundwechsel** | Unsplash oder eigene Bilder, Intervall einstellbar |
| 🎨 **6 Themes** | Classic, Month, Focus, Weather, Compact, Split |
| 📅 **Monatsansicht** | DAKboard-artiger Monatskalender mit farbigen Event-Chips |
| 🐳 **Docker-Ready** | Fertiges GHCR-Image, läuft als Container auf Port `4455` |
| 🌐 **GitHub Pages** | Promotion-Index + Live-Demo automatisch deployt |
| 🔒 **Sicher** | `.env` nie im Repo, Refresh Token lokal, kein Fallback-Passwort |
| 🏠 **Self-Hosted** | Kein Cloud-Abo, kein Tracking |
| 🛠️ **Admin-Panel** | Passwortgeschütztes Web-UI unter `/admin` |

---

## 🛠️ Admin-Panel

Erreichbar unter **`http://deine-ip:4455/admin`** .

| Bereich | Funktion |
|---|---|
| 📊 **Dashboard** | Status-Übersicht aller Konfigurationspunkte |
| 🔑 **Google Auth** | Client ID/Secret eintragen, OAuth-Flow starten, Token testen |
| 🗓️ **Kalender** | Verfügbare Kalender laden, per Toggle auswählen |
| 🎨 **Design & Theme** | Theme-Picker mit Vorschaukarten, Schriftart, Größen, Akzentfarbe |
| 🖼️ **Hintergründe** | Unsplash-Query, eigene Bilder per Drag & Drop, Helligkeit & Intervall |
| ⚙️ **Anzeige** | Wetter / Kalender / Sekunden ein-/ausblenden |
| 🌤️ **Wetter** | Stadt und OpenWeatherMap API Key setzen |

### Verfügbare Themes

| Theme | Beschreibung |
|---|---|
| **Classic** | Uhr links, Wetter rechts, Eventliste unten |
| **Month** | Uhr oben, voller Monatskalender |
| **Focus** | Nur Uhr und Datum, minimalistisch |
| **Weather** | Wetter groß im Zentrum, Termine unten |
| **Compact** | Optimiert für 1024×800, max. 5 Termine |
| **Split** ⭐ | Zweispaltig: Uhr + Wetter links, Monatsraster rechts |

> Alle Einstellungen werden persistent in `/data/settings.json` gespeichert.

---

## 🔑 Google OAuth einrichten

```text
1. https://console.cloud.google.com → Neues Projekt anlegen
2. APIs & Dienste → „Google Calendar API“ aktivieren
3. OAuth-Client-ID erstellen (Typ: Webanwendung)
4. Redirect URI setzen:
   http://deine-ip:4455/api/admin/oauth/callback
5. Client ID + Secret im Admin-Panel eintragen
6. „Mit Google anmelden“ klicken
7. Zugriff erlauben → Refresh Token wird automatisch gespeichert
```

> Die Redirect URI muss exakt mit deiner IP oder Domain übereinstimmen.

---

## 🌤️ Wetter einrichten

```text
1. Kostenlosen Account auf https://openweathermap.org anlegen
2. API Key erzeugen
3. Im Admin-Panel unter „Wetter" eintragen
4. Stadt festlegen → Speichern
```

---

## ⚙️ Umgebungsvariablen

> Vorlage: [`.env.example`](.env.example)

| Variable | Pflicht | Beschreibung |
|---|:---:|---|
| `ADMIN_PASSWORD` | ✅ | Zugang zum Admin-Panel |
| `SECRET_KEY` | ✅ | Flask Session-Key (mind. 32 Zeichen) |
| `GOOGLE_CLIENT_ID` | ⭕ | Optional, kann im Admin gesetzt werden |
| `GOOGLE_CLIENT_SECRET` | ⭕ | Optional, kann im Admin gesetzt werden |
| `GOOGLE_REFRESH_TOKEN` | ⭕ | Wird per OAuth automatisch gespeichert |
| `CALENDAR_IDS` | ⭕ | Optional, wird im Admin überschrieben |
| `OPENWEATHER_API_KEY` | ⭕ | Optional, kann im Admin gesetzt werden |
| `CITY` | ⭕ | Optional, Standardstadt fürs Wetter |

---

## 🚀 Weitere Installationswege

### 📦 Portainer (empfohlen)

Das Container-Image wird bei jedem Push auf `main` automatisch von einem
[GitHub-Actions-Workflow](.github/workflows/docker-publish.yml) gebaut und nach
**`ghcr.io/jbkunama1/hai.calboard:latest`** gepusht. In Portainer brauchst du
deshalb nur das fertige Image – kein Git-Repo und kein Build.

1. **Portainer** → **Stacks** → **Add stack**
2. Name vergeben (z. B. `hAI-CalBoard`)
3. **Web editor** wählen und folgendes einfügen:

```yaml
services:
  calboard:
    image: ghcr.io/jbkunama1/hai.calboard:latest
    container_name: hAI-CalBoard
    ports:
      - "4455:8080"
    environment:
      ADMIN_PASSWORD: "dein_sicheres_passwort"
      SECRET_KEY: "ein_langer_zufaelliger_string_min_32"
      # OPTIONAL:
      # GOOGLE_CLIENT_ID: ""
      # GOOGLE_CLIENT_SECRET: ""
      # GOOGLE_REFRESH_TOKEN: ""
      # CALENDAR_IDS: "primary"
      # OPENWEATHER_API_KEY: ""
      # CITY: "Pfinztal"
    volumes:
      - calboard_data:/data
    networks:
      - highfishNetwork
    restart: unless-stopped

volumes:
  calboard_data:

networks:
  highfishNetwork:
    external: true
```

**⚠️ Netzwerk erstellen, bevor du den Stack startest!**

Da `highfishNetwork` als externes Netzwerk konfiguriert ist, muss es
bereits existieren, bevor `docker compose up -d` ausgeführt wird.

Erstelle das Netzwerk mit diesem Befehl:

```bash
docker network create highfishNetwork
```

4. Mindestens `ADMIN_PASSWORD` und `SECRET_KEY` setzen
5. **Deploy the stack**

> Hinweis: Wenn du das Image selbst bauen willst (z. B. mit Änderungen aus einem
> Fork), setze stattdessen `build: .` im Stack und deploye per Git-Template
> `https://github.com/jbkunama1/hAI.CalBoard`.

### 🔧 Bare Metal

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
pip install -r requirements.txt
cp .env.example .env
export $(cat .env | xargs)
cd app && gunicorn --bind 0.0.0.0:4455 server:app
```

---

## 🗂️ Projektstruktur

```text
hAI.CalBoard/
├── docker-compose.yml
├── Dockerfile
├── index.html            # GitHub-Pages-Promotion-Seite
├── demo.html              # Self-contained Live-Demo
├── .env.example
├── README.md
├── README_EN.md
├── CHANGELOG.md
├── requirements.txt
├── .github/workflows/
│   ├── docker-publish.yml # baut & pusht GHCR-Image
│   └── gh-pages.yml       # deployt GitHub Pages
├── scripts/
│   ├── kiosk.sh
│   └── autostart.desktop
└── app/
    ├── server.py
    └── static/
        ├── index.html
        └── admin.html
```

---

## 🔄 Update-Intervalle

```text
🕐 Uhrzeit        → jede Sekunde
🌤️ Wetter         → alle 10 Minuten
🗓️ Kalender       → alle 5 Minuten
🖼️ Hintergrund    → konfigurierbar (Standard: 30 Min)
```

---

## 🛠️ Troubleshooting

| Problem | Lösung |
|---|---|
| Container startet nicht | `docker logs hAI-CalBoard` prüfen |
| Admin-Login schlägt fehl | `ADMIN_PASSWORD` in `.env` prüfen |
| Kalender leer | Admin → Google Auth → Verbindung testen |
| Wetter lädt nicht | Admin → Wetter → API Key + Stadt prüfen |
| Port 4455 belegt | Port in `docker-compose.yml` anpassen |
| OAuth schlägt fehl | Redirect URI exakt prüfen |
| Einstellungen gehen verloren | Docker Volume `calboard_data` prüfen |

---

## 🤖 CI/CD – Automatischer Image-Build

Bei jedem Push auf `main` baut ein
[GitHub-Actions-Workflow](.github/workflows/docker-publish.yml) das Container-Image
und pusht es automatisch auf **`ghcr.io/jbkunama1/hai.calboard`** .

- **Tags:** `latest` (Branch `main`), `vX.Y.Z` (SemVer-Tags), `sha-<commit>` je Commit
- **Cache:** Buildx GHA-Cache, `pull_request` baut nur (kein Push)
- Portainer kann das Image direkt per `ghcr.io/jbkunama1/hai.calboard:latest` laden (siehe oben)

### 🌐 GitHub Pages

Wie Promotion-Seite ([`index.html`](index.html) samt [`demo.html`](demo.html))
wird automatisch gebaut und nach GitHub Pages deployt. Aktiviere in den
Repo-Einstellungen einmalig:

1. **Settings → Pages → Source:** „GitHub Actions"
2. Der Workflow [`.github/workflows/gh-pages.yml`](.github/workflows/gh-pages.yml) deployt bei jedem relevanten Push automatisch.

---

## 📺 DietPi / Kiosk-Betrieb

```bash
bash scripts/kiosk.sh
```

Oder:

```bash
mkdir -p ~/.config/autostart
cp scripts/autostart.desktop ~/.config/autostart/
```

---

## 📝 Lizenz

MIT License – © 2026 Daniel Lienhard

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
