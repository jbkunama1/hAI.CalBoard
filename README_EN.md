# 🖥️ hAI.CalBoard

<div align="center">

![hAI.CalBoard Logo](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/efe4dd3d-88a7-4f27-ace9-72f4ef2db416.png)

**Self-hosted Smart Home Dashboard** – Google Calendar · Weather · Clock · Background Slideshow

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

## ✨ Features

| Feature | Details |
|---|---|
| 🗓️ **Google Calendar** | Multiple calendars via OAuth2 Refresh Token, updated every 5 min |
| 🌤️ **Weather** | OpenWeatherMap API, real-time |
| 🕐 **Clock & Date** | Second-precise, fully localizable |
| 🖼️ **Background Slideshow** | Unsplash or custom images, configurable interval |
| 🐳 **Docker-Ready** | Runs as a container on port `4455` |
| 🔒 **Secure** | `.env` never in repo, refresh token stored locally |
| 🏠 **Self-Hosted** | No cloud subscription, no tracking |
| 🛠️ **Admin Panel** | Password-protected web UI at `/admin` |

---

## 🛠️ Admin Panel

Accessible at **`http://your-ip:4455/admin`** – protected by `ADMIN_PASSWORD` in your `.env`.

| Section | Function |
|---|---|
| 📊 **Dashboard** | Status overview of all configuration items |
| 🔑 **Google Auth** | Enter Client ID/Secret, run OAuth flow, test connection |
| 🗓️ **Calendars** | Load available calendars, select via toggle |
| 🎨 **Design** | Font family, size, accent color, layout, event style |
| 🖼️ **Backgrounds** | Unsplash query, custom image upload (drag & drop), brightness & interval |
| ⚙️ **Display** | Toggle weather / calendar / seconds on/off |
| 🌤️ **Weather** | Set city and OpenWeatherMap API key |

> All settings are stored persistently in `/data/settings.json` (Docker volume).

---

## 🚀 Installation

> Three ways to install – choose what fits your setup:

### 🐳 Option 1 – Docker CLI (recommended)

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
cp .env.example .env
nano .env                       # fill in real values
docker compose up -d --build
docker logs -f hAI-CalBoard
```

> 📍 Dashboard: `http://your-ip:4455` · Admin: `http://your-ip:4455/admin`

---

### 📦 Option 2 – Portainer (Stack)

1. **Portainer** → `Stacks` → `+ Add Stack`
2. **Name:** `hAI-CalBoard`
3. **Git Repository** → URL: `https://github.com/jbkunama1/hAI.CalBoard` · Compose path: `docker-compose.yml`
4. **Environment Variables:**

   | Variable | Value |
   |---|---|
   | `GOOGLE_CLIENT_ID` | `your_client_id` |
   | `GOOGLE_CLIENT_SECRET` | `your_secret` |
   | `GOOGLE_REFRESH_TOKEN` | `your_refresh_token` |
   | `CALENDAR_IDS` | `primary` |
   | `OPENWEATHER_API_KEY` | `your_key` |
   | `CITY` | `Berlin` |
   | `ADMIN_PASSWORD` | `your_secure_password` |
   | `SECRET_KEY` | `random_long_string` |

5. → **Deploy the stack**

> 💡 Alternatively: paste the content of `docker-compose.yml` directly into the editor – no Git access required.

---

### 🔧 Option 3 – Manual / Bare Metal

```bash
git clone https://github.com/jbkunama1/hAI.CalBoard.git
cd hAI.CalBoard
pip install flask requests flask-cors gunicorn werkzeug
cp .env.example .env && source .env
cd app && gunicorn --bind 0.0.0.0:4455 server:app
```

---

## 🔑 Google OAuth Setup

> Only needed once – afterwards everything runs automatically via the refresh token.
> **Recommended: use the Admin Panel at `/admin` → Google Auth.**

```
1. 🌐  https://console.cloud.google.com → Create new project
2. 📅  Enable Google Calendar API
3. 🔐  Create OAuth 2.0 Client ID (Web application)
       Redirect URI: http://your-ip:4455/api/admin/oauth/callback
4. 🛠️  In Admin Panel: enter Client ID & Secret → click "Sign in with Google"
5. ✅  Refresh token is saved automatically
```

> Alternatively use the [OAuth Playground](https://developers.google.com/oauthplayground) with scope `https://www.googleapis.com/auth/calendar.readonly`.

---

## ⚙️ Environment Variables

> Template: [`.env.example`](.env.example)

| Variable | Required | Example | Description |
|---|:---:|---|---|
| `GOOGLE_CLIENT_ID` | ✅ | `123...apps.googleusercontent.com` | OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | ✅ | `GOCSPX-...` | OAuth Client Secret |
| `GOOGLE_REFRESH_TOKEN` | ⚠️ | `1//04...` | Refresh token (via Admin Panel or manually) |
| `CALENDAR_IDS` | ⚠️ | `primary,work@gmail.com` | Fallback, overridden by Admin Panel |
| `OPENWEATHER_API_KEY` | ✅ | `abc123...` | Free at openweathermap.org |
| `CITY` | ✅ | `Berlin` | City for weather display |
| `ADMIN_PASSWORD` | ✅ | `secure_password` | Access to Admin Panel |
| `SECRET_KEY` | ✅ | `random_long_string` | Flask session key |

---

## 🗂️ Project Structure

```
hAI.CalBoard/
├── 🐳 docker-compose.yml
├── 🐋 Dockerfile
├── 🔒 .env.example
├── 🚫 .gitignore
├── 📄 demo.html                # Offline demo with sample data
└── 📁 app/
    ├── 🐍 server.py            # Flask backend (API + admin routes)
    └── 📁 static/
        ├── 🌐 index.html       # Dashboard (DE)
        ├── 🌐 index_en.html    # Dashboard (EN)
        ├── 🛠️ admin.html       # Admin Panel
        └── 📄 demo.html        # Demo
```

---

## 🔄 Update Intervals

```
🕐 Clock         →  every second
🌤️ Weather       →  every 10 minutes
🗓️ Calendar      →  every 5 minutes
🖼️ Background    →  configurable (default: 30 min)
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Container won't start | Check `docker logs hAI-CalBoard` |
| Admin login fails | Check `ADMIN_PASSWORD` in `.env` |
| Calendar empty | Admin → Google Auth → Test connection |
| Weather not loading | Enter API key in Admin → Weather |
| Port 4455 in use | Change port in `docker-compose.yml` |
| Portainer build fails | Make sure `Dockerfile` is in repo root |
| Settings lost after restart | Check Docker volume `calboard_data` |

---

## 📝 DietPi / Kiosk Mode

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

## 📄 License

[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

```
MIT License – © 2026 Daniel Lienhard
```

<div align="center">
Made with ❤️ in Pfinztal · Powered by Flask, Docker & Google Calendar API
</div>
