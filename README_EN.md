# 🖥️ hAI.CalBoard

<div align="center">

![hAI.CalBoard Logo](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/efe4dd3d-88a7-4f27-ace9-72f4ef2db416.png)

**Self-hosted Smart Home Dashboard** – Google Calendar · Weather · Clock · Background Slideshow · Theme System

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

[🇩🇪 Deutsch](README.md) | 🇬🇧 English

</div>

---

## ⚡ Quick Start (3 steps)

> On first launch, `.env` only needs **2 entries**.
> Google, weather, calendars and themes can be configured later in the **admin panel**.

### Step 1 – Create minimal `.env`

```bash
cp .env.example .env
```

Then edit `.env` and only set these two values:

```env
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=some_long_random_string_at_least_32_characters
```

### Step 2 – Start container

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
docker compose up -d --build
```

### Step 3 – Open browser

```text
http://your-ip:4455
```

If nothing is configured yet, the server redirects automatically to **`/admin`**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Calendar** | Multiple calendars via OAuth2 refresh token, updated every 5 minutes |
| 🌤️ **Weather** | OpenWeatherMap API, real-time |
| 🕐 **Clock & Date** | Second-precise, localized display |
| 🖼️ **Background Slideshow** | Unsplash or custom images, configurable interval |
| 🎨 **6 Themes** | Classic, Month, Focus, Weather, Compact, Split |
| 📅 **Month View** | DAKboard-style full month calendar with event chips |
| 🐳 **Docker-Ready** | Runs as container on port `4455` |
| 🔒 **Secure** | `.env` never in repo, refresh token stored locally |
| 🏠 **Self-Hosted** | No cloud subscription, no tracking |
| 🛠️ **Admin Panel** | Password-protected web UI at `/admin` |

---

## 🛠️ Admin Panel

Available at **`http://your-ip:4455/admin`**.

| Section | Function |
|---|---|
| 📊 **Dashboard** | Status overview of all config items |
| 🔑 **Google Auth** | Enter client ID/secret, start OAuth flow, test token |
| 🗓️ **Calendars** | Load available calendars and select them |
| 🎨 **Design & Theme** | Theme picker with previews, fonts, sizes, accent color |
| 🖼️ **Backgrounds** | Unsplash query, drag & drop image upload, brightness & interval |
| ⚙️ **Display** | Toggle weather / calendar / seconds |
| 🌤️ **Weather** | Set city and OpenWeatherMap API key |

### Available themes

| Theme | Description |
|---|---|
| **Classic** | Clock left, weather right, event list below |
| **Month** | Clock top, full month calendar |
| **Focus** | Clock and date only, minimal layout |
| **Weather** | Large centered weather, events below |
| **Compact** | Optimized for 1024×800, max. 5 events |
| **Split** ⭐ | Two-column layout: clock + weather left, month grid right |

---

## 🔑 Google OAuth setup

```text
1. Open https://console.cloud.google.com
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth client ID (Web application)
5. Set redirect URI:
   http://your-ip:4455/api/admin/oauth/callback
6. Enter client ID and secret in admin panel
7. Click “Sign in with Google”
8. Grant access → refresh token is stored automatically
```

---

## 🌤️ Weather setup

```text
1. Create free account at https://openweathermap.org
2. Generate API key
3. Enter it in Admin → Weather
4. Set city → Save
```

---

## ⚙️ Environment variables

> Template: [`.env.example`](.env.example)

| Variable | Required | Description |
|---|:---:|---|
| `ADMIN_PASSWORD` | ✅ | Access to admin panel |
| `SECRET_KEY` | ✅ | Flask session key |
| `GOOGLE_CLIENT_ID` | ⭕ | Optional, can be set in admin |
| `GOOGLE_CLIENT_SECRET` | ⭕ | Optional, can be set in admin |
| `GOOGLE_REFRESH_TOKEN` | ⭕ | Stored automatically via OAuth |
| `CALENDAR_IDS` | ⭕ | Optional fallback, overwritten by admin |
| `OPENWEATHER_API_KEY` | ⭕ | Optional, can be set in admin |
| `CITY` | ⭕ | Optional default city |

---

## 🚀 Other installation methods

### 📦 Portainer

1. Create a new stack
2. Repo: `https://github.com/jbkunama1/hAI.CalBoard`
3. Compose path: `docker-compose.yml`
4. Set at least `ADMIN_PASSWORD` and `SECRET_KEY`
5. Deploy

### 🔧 Bare metal

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
pip install -r requirements.txt
cp .env.example .env
export $(cat .env | xargs)
cd app && gunicorn --bind 0.0.0.0:4455 server:app
```

---

## 🗂️ Project structure

```text
hAI.CalBoard/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
├── README_EN.md
├── CHANGELOG.md
├── demo.html
├── requirements.txt
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

## 🔄 Update intervals

```text
🕐 Clock         → every second
🌤️ Weather       → every 10 minutes
🗓️ Calendar      → every 5 minutes
🖼️ Background    → configurable (default: 30 min)
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Container won't start | Check `docker logs hAI-CalBoard` |
| Admin login fails | Check `ADMIN_PASSWORD` in `.env` |
| Calendar is empty | Admin → Google Auth → Test connection |
| Weather not loading | Admin → Weather → Check API key + city |
| Port 4455 already in use | Change port in `docker-compose.yml` |
| OAuth fails | Verify redirect URI exactly |
| Settings are lost | Check Docker volume `calboard_data` |

---

## 📺 DietPi / Kiosk mode

```bash
bash scripts/kiosk.sh
```

Or:

```bash
mkdir -p ~/.config/autostart
cp scripts/autostart.desktop ~/.config/autostart/
```

---

## 📝 License

MIT License – © 2026 Daniel Lienhard

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
