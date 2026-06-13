# Changelog

Alle nennenswerten Änderungen an hAI.CalBoard werden in dieser Datei dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [1.1.1] – 2026-06-13

### Fixed
- 🐛 `theme`-Feld fehlte in `DEFAULT_SETTINGS` und `public_settings()` → Dashboard zeigte keine Theme-Klasse, nur heller Hintergrund
- 🌗 Bildschirmhelligkeit wird jetzt korrekt als CSS-Variable `--bg-brightness` gesetzt und per `filter: brightness()` angewendet (statt nicht-funktionalem rgba-Overlay)
- 🖼️ Unsplash-Integration: URL auf `source.unsplash.com/featured/1920x1080/?{query}` korrigiert, Cache-Buster `?_={timestamp}` ergänzt
- 📄 `index.html` komplett überarbeitet – alle 6 Themes, Brightness-Fix und Unsplash-Fix integriert
- 📝 `demo.html` – Layout-Switcher (Classic / Zentriert / Minimal) ergänzt
- ⚙️ `.env.example` – Pflichtfelder klar markiert, optionale Felder leer mit Kommentaren

---

## [1.1.0] – 2026-06-13

### Added
- 🎨 Neues Theme-System mit 6 Dashboard-Themes: Classic, Month, Focus, Weather, Compact und Split
- 🧩 Theme-Picker im Admin-Panel mit visuellen SVG-Vorschaukarten
- 📅 Monatsansicht mit vollflächigem Kalender-Raster und farbigen Event-Chips
- ⭐ Neues Split-Layout mit Uhr/Wetter links und Monatsraster rechts
- 📘 README.md und README_EN.md auf aktuellen Funktionsstand gebracht

### Changed
- 🛠️ Design-Bereich im Admin-Panel zu „Design & Theme" erweitert
- 📋 Dokumentation an aktuellen UI- und Feature-Stand angepasst
- 🧱 Dashboard-Frontend strukturell auf mehrere Theme-Layouts erweitert
- 🎯 Compact- und Weather-Theme nutzen themenspezifisch reduzierte Event-Anzahl

---

## [1.0.0] – 2026-06-12

### Added
- 🎞️ Dashboard mit Echtzeit-Uhrzeit, Datum, Google Kalender & Wetter
- 🛠️ Passwortgeschütztes Admin-Panel unter `/admin`
- 🔑 Google OAuth2-Flow direkt im Browser (inkl. CSRF-Schutz via State-Parameter)
- 🗓️ Kalender-Auswahl per Toggle im Admin-Panel
- 🎨 Design-Konfiguration: Schriftart, -größe, Akzentfarbe
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
- Secrets im Admin-Panel maskiert
- `.env` in `.gitignore` – nie im Repo
- TruffleHog Workflow aktiv
