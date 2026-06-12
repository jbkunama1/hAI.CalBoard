#!/bin/bash
# hAI.CalBoard – Kiosk-Startskript für DietPi / LXDE
# Verwendung: bash scripts/kiosk.sh
# Autostart: ~/.config/autostart/calboard.desktop

HOST="${CALBOARD_HOST:-localhost}"
PORT="${CALBOARD_PORT:-4455}"
URL="http://${HOST}:${PORT}"
WAIT="${CALBOARD_WAIT:-15}"
BROWSER="${CALBOARD_BROWSER:-firefox}"

echo "[hAI.CalBoard] Warte ${WAIT}s auf Container..."
sleep "$WAIT"

echo "[hAI.CalBoard] Starte Kiosk: $URL"
exec "$BROWSER" \
  --kiosk \
  --no-first-run \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-restore-session-state \
  "$URL"
