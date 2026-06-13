from flask import Flask, jsonify, send_from_directory, request, session, redirect, url_for
from flask_cors import CORS
import requests, os, json, secrets
from datetime import datetime, timezone
import pytz
from functools import wraps
from werkzeug.utils import secure_filename
import hashlib
import sys

# ─── STARTUP CHECKS ────────────────────────────────────────────
def _require_env(var):
    val = os.environ.get(var, '')
    if not val:
        print(f'[FATAL] Umgebungsvariable {var} ist nicht gesetzt. Server wird nicht gestartet.', flush=True)
        sys.exit(1)
    return val

ADMIN_PASSWORD = _require_env('ADMIN_PASSWORD')
SECRET_KEY     = _require_env('SECRET_KEY')

app = Flask(__name__, static_folder='static')
app.secret_key = SECRET_KEY
CORS(app)

SETTINGS_FILE = '/data/settings.json'
UPLOAD_FOLDER = '/data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

DEFAULT_SETTINGS = {
    'font_family': 'Segoe UI',
    'font_size_time': '7.5',
    'font_size_date': '1.5',
    'font_size_events': '1.0',
    'bg_mode': 'unsplash',
    'bg_unsplash_query': 'nature,landscape',
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
}

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            s = json.load(f)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(s)
            return merged
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(data):
    s = load_settings()
    s.update(data)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)
    return s

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_configured():
    s = load_settings()
    return bool(s.get('google_client_id', '').strip())

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

def get_access_token(settings=None):
    if not settings:
        settings = load_settings()
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': settings['google_client_id'],
        'client_secret': settings['google_client_secret'],
        'refresh_token': settings['google_refresh_token'],
        'grant_type': 'refresh_token'
    })
    return r.json().get('access_token')

def get_calendar_names(token):
    """Gibt ein Dict {kalender_id: lesbarer_name} zurueck."""
    try:
        r = requests.get(
            'https://www.googleapis.com/calendar/v3/users/me/calendarList',
            headers={'Authorization': f'Bearer {token}'}
        )
        return {c['id']: c['summary'] for c in r.json().get('items', [])}
    except:
        return {}

# ─── AUTH ─────────────────────────────────────────────────────
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    pw = data.get('password', '')
    if hashlib.sha256(pw.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
        session['admin'] = True
        return jsonify({'ok': True})
    return jsonify({'error': 'Falsches Passwort'}), 403

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    return jsonify({'ok': True})

@app.route('/api/admin/check')
def admin_check():
    return jsonify({'authenticated': bool(session.get('admin'))})

# ─── SETTINGS ────────────────────────────────────────────
@app.route('/api/admin/settings', methods=['GET'])
@admin_required
def get_settings():
    s = load_settings()
    safe = s.copy()
    for k in ['google_client_secret', 'google_refresh_token', 'openweather_api_key']:
        if safe.get(k): safe[k] = safe[k][:6] + '••••••••'
    return jsonify(safe)

@app.route('/api/admin/settings', methods=['POST'])
@admin_required
def update_settings():
    data = request.json
    for k in ['google_client_secret', 'google_refresh_token', 'openweather_api_key']:
        if data.get(k, '').endswith('••••••••'):
            data.pop(k)
    save_settings(data)
    return jsonify({'ok': True})

# ─── GOOGLE OAUTH ──────────────────────────────────────────
@app.route('/api/admin/oauth/url')
@admin_required
def oauth_url():
    s = load_settings()
    client_id = s.get('google_client_id', '')
    redirect_uri = request.host_url.rstrip('/') + '/api/admin/oauth/callback'
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={client_id}'
        '&redirect_uri=' + requests.utils.quote(redirect_uri) +
        '&response_type=code'
        '&scope=' + requests.utils.quote('https://www.googleapis.com/auth/calendar.readonly') +
        f'&access_type=offline&prompt=consent&state={state}'
    )
    return jsonify({'url': url, 'redirect_uri': redirect_uri})

@app.route('/api/admin/oauth/callback')
def oauth_callback():
    returned_state = request.args.get('state', '')
    expected_state = session.pop('oauth_state', None)
    if not expected_state or not secrets.compare_digest(returned_state, expected_state):
        return redirect('/admin?oauth=csrf_error')
    code = request.args.get('code')
    s = load_settings()
    redirect_uri = request.host_url.rstrip('/') + '/api/admin/oauth/callback'
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': s['google_client_id'],
        'client_secret': s['google_client_secret'],
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    })
    tokens = r.json()
    if 'refresh_token' in tokens:
        save_settings({'google_refresh_token': tokens['refresh_token']})
        return redirect('/admin?oauth=success')
    return redirect('/admin?oauth=error')

@app.route('/api/admin/oauth/test')
@admin_required
def oauth_test():
    try:
        token = get_access_token()
        if token:
            return jsonify({'ok': True, 'message': 'Verbindung erfolgreich ✅'})
        return jsonify({'ok': False, 'message': 'Kein Token erhalten'})
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)})

# ─── KALENDER LISTE ────────────────────────────────────────
@app.route('/api/admin/calendars')
@admin_required
def list_calendars():
    try:
        token = get_access_token()
        r = requests.get('https://www.googleapis.com/calendar/v3/users/me/calendarList',
                         headers={'Authorization': f'Bearer {token}'})
        cals = [{'id': c['id'], 'name': c['summary'],
                  'color': c.get('backgroundColor', '#4caf50'),
                  'primary': c.get('primary', False)}
                for c in r.json().get('items', [])]
        return jsonify(cals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── BILD-UPLOAD ───────────────────────────────────────────
@app.route('/api/admin/upload', methods=['POST'])
@admin_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        s = load_settings()
        imgs = s.get('custom_bg_images', [])
        url = f'/uploads/{filename}'
        if url not in imgs:
            imgs.append(url)
        save_settings({'custom_bg_images': imgs})
        return jsonify({'ok': True, 'url': url})
    return jsonify({'error': 'Dateityp nicht erlaubt'}), 400

@app.route('/api/admin/upload/<filename>', methods=['DELETE'])
@admin_required
def delete_image(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    s = load_settings()
    imgs = [i for i in s.get('custom_bg_images', []) if i != f'/uploads/{filename}']
    save_settings({'custom_bg_images': imgs})
    return jsonify({'ok': True})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ─── PUBLIC API ─────────────────────────────────────────────
@app.route('/api/setup-status')
def setup_status():
    return jsonify({'configured': is_configured()})

@app.route('/api/settings')
def public_settings():
    s = load_settings()
    safe_keys = [
        'font_family', 'font_size_time', 'font_size_date', 'font_size_events',
        'bg_mode', 'bg_unsplash_query', 'bg_interval', 'bg_brightness', 'accent_color',
        'show_weather', 'show_calendar', 'show_seconds', 'max_events', 'city',
        'custom_bg_images', 'layout', 'time_format', 'date_format', 'overlay_style',
        'event_style', 'theme', 'timezone',
    ]
    return jsonify({k: s[k] for k in safe_keys if k in s})

@app.route('/api/calendar')
def calendar():
    s = load_settings()
    cal_ids_str = s.get('calendar_ids', os.environ.get('CALENDAR_IDS', 'primary'))
    cal_ids = [c.strip() for c in cal_ids_str.split(',') if c.strip()]
    if not cal_ids:
        cal_ids = ['primary']

    token = get_access_token(s)

    # Lesbare Kalendernamen laden (einmalig)
    cal_names = get_calendar_names(token)

    events = []
    tz = pytz.timezone(s.get('timezone', 'Europe/Berlin'))
    now = datetime.now(tz).isoformat()
    for cal_id in cal_ids:
        url = f'https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(cal_id)}/events'
        r = requests.get(url, headers={'Authorization': f'Bearer {token}'},
                         params={'timeMin': now, 'maxResults': s.get('max_events', 8),
                                 'singleEvents': True, 'orderBy': 'startTime'})
        # Lesbarer Name: aus calendarList, Fallback auf 'primary' → 'Mein Kalender'
        display_name = cal_names.get(cal_id) or (
            'Mein Kalender' if cal_id == 'primary' else cal_id
        )
        for item in r.json().get('items', []):
            events.append({
                'title':    item.get('summary', '(kein Titel)'),
                'start':    item.get('start', {}).get('dateTime') or item.get('start', {}).get('date'),
                'end':      item.get('end',   {}).get('dateTime') or item.get('end',   {}).get('date'),
                'calendar': display_name,
                'color':    item.get('colorId', '')
            })
    events.sort(key=lambda x: x['start'] or '')
    return jsonify(events)

@app.route('/api/weather')
def weather():
    s = load_settings()
    key  = s.get('openweather_api_key', '')
    city = s.get('city', 'Pfinztal')
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&appid={key}&units=metric&lang=de'
    )
    d = r.json()
    return jsonify({
        'temp':        round(d['main']['temp']),
        'feels_like':  round(d['main']['feels_like']),
        'description': d['weather'][0]['description'],
        'icon':        d['weather'][0]['icon'],
        'city':        d['name']
    })

# ─── STATIC ──────────────────────────────────────────────────
@app.route('/')
def index():
    if not is_configured():
        return redirect('/admin?setup=1')
    return send_from_directory('static', 'index.html')

@app.route('/admin')
@app.route('/admin/')
def admin_page():
    return send_from_directory('static', 'admin.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)
