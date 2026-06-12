# Changelog

Alle nennenswerten Änderungen an hAI.CalBoard werden in dieser Datei dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [1.0.0] – 2026-06-12

### Added
- 🎞️ Dashboard mit Echtzeit-Uhrzeit, Datum, Google Kalender & Wetter
- 🇩🇪 Deutsche & 🇬🇧 Englische Dashboard-Version (`index.html` / `index_en.html`)
- 🛠️ Passwortgeschütztes Admin-Panel unter `/admin`
- 🔑 Google OAuth2-Flow direkt im Browser (inkl. CSRF-Schutz via State-Parameter)
- 🗓️ Kalender-Auswahl per Toggle im Admin-Panel
- 🎨 Design-Konfiguration: Schriftart, -größe, Akzentfarbe, Layout, Termin-Stil
- 🖼️ Hintergrund-Verwaltung: Unsplash-Query + eigene Bilder per Drag & Drop
- 🌤️ Wetter-Konfiguration (Stadt + API-Key) im Admin
- 🐳 Docker-Ready mit `docker-compose.yml` inkl. Healthcheck & Volume
- 📊 Status-Übersicht im Admin-Dashboard
- 🔒 Sicherheit: Keine Fallback-Secrets, SHA256-Passwortvergleich, Flask-Session
- 🔍 TruffleHog Secret-Scan Workflow (täglich + bei jedem Push)
- 📄 `requirements.txt` für Bare-Metal-Installation
- 📜 Kiosk-Startskript `scripts/kiosk.sh` für DietPi/LXDE
- 🌍 Erster Start leitet automatisch auf `/admin` weiter wenn Google nicht konfiguriert
- 📄 `README.md` (DE) & `README_EN.md` (EN) mit vollständiger Dokumentation
- 🎨 Logo

### Security
- `ADMIN_PASSWORD` & `SECRET_KEY` sind Pflicht – Server startet nicht ohne sie
- OAuth State-Parameter (CSRF-Schutz) via `secrets.token_urlsafe(32)`
- Secrets im Admin-Panel maskiert (`abc123â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢`)
- `.env` in `.gitignore` – nie im Repo
- TruffleHog Workflow aktiv
