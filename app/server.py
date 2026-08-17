import os
import json
import time
import uuid
import threading
import requests
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, session
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from functools import wraps
from zoneinfo import ZoneInfo

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'change-me-in-production')

SETTINGS_FILE = os.environ.get('SETTINGS_FILE', '/data/settings.json')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

DEFAULT_SETTINGS = {
    'font_family': 'Segoe UI',
    'font_size_time': '7.5',
    'font_size_date': '1.5',
    'font_size_events': '1.0',
    'bg_mode': 'picsum',
    'bg_unsplash_query': 'nature,landscape',
    'bg_unsplash_key': '',
    'bg_interval': 30,
    'bg_brightness': 0.45,
    'accent_color': '#4caf50',
    'show_weather': True,
    'show_calendar': True,
    'show_seconds': False,
    'calendar_ids': '',
    'max_events': 8,
    'city': os.environ.get('CITY', 'Pfinztal'),
    'google_client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
    'google_client_secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
    'google_refresh_token': os.environ.get('GOOGLE_REFRESH_TOKEN', ''),
    'openweather_api_key': os.environ.get('OPENWEATHER_API_KEY', ''),
    'custom_bg_images': [],
    'layout': 'default',
    'time_format': '24h',
    'date_format': 'long',
    'overlay_style': 'dark',
    'event_style': 'card',
    'theme': 'classic',
    'timezone': 'Europe/Berlin',
    'theme_time_color': '#ffffff',
    'theme_date_color': 'rgba(255,255,255,0.75)',
    'theme_event_bg': 'rgba(255,255,255,0.10)',
    'theme_accent_opacity': '1.0',
    'theme_padding': '36',
    'theme_event_gap': '8',
    'theme_layout_preset': 'time-top',
    'show_onthisday': True,
    'onthisday_language': os.environ.get('ONTHISDAY_LANGUAGE', 'de'),
    'show_fhem': True,
    'fhem_url': os.environ.get('FHEM_URL', ''),
    'fhem_user': os.environ.get('FHEM_USER', 'fhem'),
    'fhem_password': os.environ.get('FHEM_PASSWORD', ''),
}

_settings_cache = None
_settings_lock = threading.Lock()
_onthisday_cache = {}

def load_settings():
    global _settings_cache
    with _settings_lock:
        if _settings_cache is not None:
            return _settings_cache
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
            merged = {**DEFAULT_SETTINGS, **data}
        except (FileNotFoundError, json.JSONDecodeError):
            merged = dict(DEFAULT_SETTINGS)
        _settings_cache = merged
        return merged

def save_settings(settings):
    global _settings_cache
    with _settings_lock:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        _settings_cache = settings

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('password') == ADMIN_PASSWORD:
        session['authenticated'] = True
        return jsonify({'ok': True})
    return jsonify({'error': 'Wrong password'}), 403

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})

@app.route('/api/onthisday')
def onthisday():
    """Return three daily rotating Wikipedia OnThisDay events."""
    import datetime, json, random
    s = load_settings()
    tz = s.get('timezone') or 'Europe/Berlin'
    try:
        now = datetime.datetime.now(ZoneInfo(tz))
    except Exception:
        now = datetime.datetime.now(datetime.timezone.utc)
    month, day = now.month, now.day

    # Use cache: key = f'{month}-{day}'
    cache_key = f'{month}-{day}'
    with _settings_lock:
        if cache_key not in _onthisday_cache:
            try:
                resp = requests.get(
                    f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}',
                    timeout=5
                )
                resp.raise_for_status()
                data = resp.json()
                events = [
                    {
                        'year': e['year'],
                        'heading': e['title'],
                        'text': e['description']
                    }
                    for e in data.get('events', [])
                ]
                # 3x daily rotation: pick based on 8-hour slot so we show
                # different events in the morning, afternoon and evening.
                slot = now.hour // 8
                start = (slot * 2) % len(events) if events else 0
                _onthisday_cache[cache_key] = [events[(start + i) % len(events)] for i in range(min(3, len(events)))]
            except Exception as e:
                _onthisday_cache[cache_key] = []
    result = {
        'date': f'{month}-{day}',
        'language': s.get('onthisday_language') or 'de',
        'events': _onthisday_cache[cache_key]
    }
    return jsonify(result)

@app.route('/api/fhem')
def fhem():
    """Return a filtered list of FHEM JSON API readings."""
    s = load_settings()
    fhem_url = s.get('fhem_url', '')
    fhem_user = s.get('fhem_user', '')
    fhem_password = s.get('fhem_password', '')
    # No config -> disabled
    if not fhem_url:
        return jsonify({'enabled': False}), 200
    auth = None
    if fhem_user and fhem_password:
        auth = (fhem_user, fhem_password)
    try:
        r = requests.get(f'{fhem_url}?cmd=jsonlist2', auth=auth, timeout=5)
        r.raise_for_status()
        raw = r.json()
    except Exception:
        return jsonify({'enabled': False}), 200
    result = []
    for d in raw.get('Results') or []:
        readings = d.get('Readings', {})
        picked = {}
        for name, meta in readings.items():
            # Keep only sensor/information we want to display
            if any(t in name.lower() for t in ('temperature', 'humidity', 'door', 'weather', 'pressure')):
                picked[name] = meta.get('Value', '')
        if picked:
            result.append({'name': d.get('Name', '?'), 'type': d.get('Type', ''), 'readings': picked})
    ret = {
        'enabled': True,
        'devices': result,
        'url': fhem_url
    }
    return jsonify(ret)

@app.route('/api/settings')
def settings():
    s = load_settings()
    safe_keys = [
        'font_family', 'font_size_time', 'font_size_date', 'font_size_events',
        'bg_mode', 'bg_unsplash_query', 'bg_interval', 'bg_brightness', 'accent_color',
        'show_weather', 'show_calendar', 'show_seconds', 'max_events', 'city',
        'custom_bg_images', 'layout', 'time_format', 'date_format', 'overlay_style',
        'event_style', 'theme', 'timezone',
        'theme_time_color', 'theme_date_color', 'theme_event_bg',
        'theme_accent_opacity', 'theme_padding', 'theme_event_gap',
        'theme_layout_preset',
        'show_onthisday', 'onthisday_language', 'show_fhem',
        'fhem_url', 'fhem_user', 'fhem_password',
    ]
    return jsonify({k: s[k] for k in safe_keys if k in s})

@app.route('/api/admin/settings', methods=['GET'])
@require_auth
def admin_get_settings():
    return jsonify(load_settings())

@app.route('/api/admin/settings', methods=['POST'])
@require_auth
def admin_save_settings():
    data = request.get_json()
    current = load_settings()
    current.update(data)
    save_settings(current)
    return jsonify({'ok': True})

@app.route('/api/admin/upload-bg', methods=['POST'])
@require_auth
def upload_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    ext = f.filename.rsplit('.', 1)[-1].lower()
    if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
        return jsonify({'error': 'Invalid type'}), 400
    filename = str(uuid.uuid4()) + '.' + ext
    upload_dir = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    f.save(os.path.join(upload_dir, filename))
    s = load_settings()
    images = s.get('custom_bg_images', [])
    images.append('/static/uploads/' + filename)
    s['custom_bg_images'] = images
    save_settings(s)
    return jsonify({'ok': True, 'url': '/static/uploads/' + filename})

@app.route('/api/admin/delete-bg', methods=['POST'])
@require_auth
def delete_bg():
    data = request.get_json()
    url = data.get('url', '')
    s = load_settings()
    images = s.get('custom_bg_images', [])
    if url in images:
        images.remove(url)
        s['custom_bg_images'] = images
        save_settings(s)
        try:
            path = url.lstrip('/')
            os.remove(os.path.join(app.root_path, '..', path))
        except Exception:
            pass
    return jsonify({'ok': True})

@app.route('/api/background')
def background_proxy():
    try:
        r = requests.get(
            'https://www.bing.com/HPImageArchive.aspx',
            params={'format': 'js', 'idx': 0, 'n': 1, 'mkt': 'de-DE'},
            timeout=5
        )
        data = r.json()
        url_path = data['images'][0]['url']
        full_url = 'https://www.bing.com' + url_path
        img = requests.get(full_url, timeout=10)
        return img.content, 200, {'Content-Type': 'image/jpeg', 'Cache-Control': 'public, max-age=3600'}
    except Exception as e:
        return jsonify({'error': str(e)}), 502

@app.route('/api/weather')
def weather():
    s = load_settings()
    api_key = s.get('openweather_api_key', '')
    city = s.get('city', 'Berlin')
    if not api_key:
        return jsonify({'error': 'No API key'}), 400
    try:
        r = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'de'},
            timeout=5
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/forecast')
def weather_forecast():
    s = load_settings()
    api_key = s.get('openweather_api_key', '')
    city = s.get('city', 'Berlin')
    if not api_key:
        return jsonify({'error': 'No API key'}), 400
    try:
        r = requests.get(
            'https://api.openweathermap.org/data/2.5/forecast',
            params={'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'de'},
            timeout=5
        )
        data = r.json()
        daily = {}
        for entry in data.get('list', []):
            dt = datetime.fromtimestamp(entry['dt'])
            date = dt.date().isoformat()
            temp = entry['main']['temp']
            if date not in daily:
                daily[date] = {'temp_min': temp, 'temp_max': temp, 'icon': entry['weather'][0]['icon'], 'description': entry['weather'][0]['description']}
            else:
                daily[date]['temp_min'] = min(daily[date]['temp_min'], temp)
                daily[date]['temp_max'] = max(daily[date]['temp_max'], temp)
        sorted_dates = sorted(daily.keys())[:5]
        forecast = [{
            'date': d,
            'temp_min': round(daily[d]['temp_min']),
            'temp_max': round(daily[d]['temp_max']),
            'icon': daily[d]['icon'],
            'description': daily[d]['description']
        } for d in sorted_dates]
        return jsonify({'forecast': forecast})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calendar')
def calendar():
    s = load_settings()
    client_id = s.get('google_client_id', '')
    client_secret = s.get('google_client_secret', '')
    refresh_token = s.get('google_refresh_token', '')
    if not all([client_id, client_secret, refresh_token]):
        return jsonify({'events': [], 'error': 'Google not configured'})
    try:
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri='https://oauth2.googleapis.com/token')
        creds.refresh(GoogleRequest())
        service = build('calendar', 'v3', credentials=creds)
        tz = s.get('timezone', 'Europe/Berlin')
        now = datetime.now(ZoneInfo(tz))
        time_min = now.isoformat()
        time_max = (now + timedelta(days=30)).isoformat()
        calendar_ids = s.get('calendar_ids', '')
        if calendar_ids:
            ids = [x.strip() for x in calendar_ids.split(',') if x.strip()]
        else:
            cal_list = service.calendarList().list().execute()
            ids = [c['id'] for c in cal_list.get('items', [])]
        all_events = []
        for cal_id in ids:
            try:
                result = service.events().list(calendarId=cal_id, timeMin=time_min, timeMax=time_max, maxResults=50, singleEvents=True, orderBy='startTime').execute()
                for ev in result.get('items', []):
                    start = ev.get('start', {})
                    all_events.append({
                        'id': ev.get('id'),
                        'title': ev.get('summary', '(kein Titel)'),
                        'start': start.get('dateTime') or start.get('date'),
                        'allDay': 'date' in start,
                        'color': ev.get('colorId'),
                        'calendarId': cal_id
                    })
            except Exception:
                pass
        all_events.sort(key=lambda e: e['start'] or '')
        max_ev = int(s.get('max_events', 8))
        return jsonify({'events': all_events[:max_ev]})
    except Exception as e:
        return jsonify({'events': [], 'error': str(e)})

@app.route('/api/auth/google')
@require_auth
def google_auth():
    s = load_settings()
    client_id = s.get('google_client_id', '')
    if not client_id:
        return 'Google Client ID fehlt', 400
    redirect_uri = request.host_url.rstrip('/') + '/api/auth/google/callback'
    auth_url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        '&response_type=code'
        '&scope=https://www.googleapis.com/auth/calendar.readonly'
        '&access_type=offline'
        '&prompt=consent'
    )
    return redirect(auth_url)

@app.route('/api/auth/google/callback')
def google_callback():
    code = request.args.get('code')
    if not code:
        return 'Kein Code erhalten', 400
    s = load_settings()
    redirect_uri = request.host_url.rstrip('/') + '/api/auth/google/callback'
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': s.get('google_client_id'),
        'client_secret': s.get('google_client_secret'),
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    })
    tokens = r.json()
    refresh_token = tokens.get('refresh_token')
    if refresh_token:
        s['google_refresh_token'] = refresh_token
        save_settings(s)
        return '<script>window.close();window.opener&&window.opener.location.reload();</script><p>✅ Google verbunden! Du kannst dieses Fenster schließen.</p>'
    return f'Fehler: {tokens}', 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)