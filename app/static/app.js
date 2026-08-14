const BACKGROUNDS = [
  "https://source.unsplash.com/1920x1080/?nature,landscape",
  "https://source.unsplash.com/1920x1080/?architecture,minimal",
  "https://source.unsplash.com/1920x1080/?mountains,sky",
  "https://source.unsplash.com/1920x1080/?forest,morning"
];
let bgIndex = 0;

function setBackground() {
  document.getElementById("background").style.backgroundImage =
    `url('${BACKGROUNDS[bgIndex % BACKGROUNDS.length]}?t=${Date.now()}')`;
  bgIndex++;
}

function updateClock() {
  const now = new Date();
  document.getElementById("time").textContent =
    now.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
  document.getElementById("date").textContent =
    now.toLocaleDateString("de-DE", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
}

async function loadWeather() {
  try {
    const r = await fetch("/api/weather");
    const d = await r.json();
    document.getElementById("weather-temp").textContent = `${d.main?.temp ?? d.temp ?? '–'}°C`;
    document.getElementById("weather-desc").textContent = (d.weather?.[0]?.description ?? d.description ?? '');
    document.getElementById("weather-icon").src =
      `https://openweathermap.org/img/wn/${(d.weather?.[0]?.icon) ?? d.icon}@2x.png`;
    loadForecast();
  } catch(e) { console.error("Wetter Fehler:", e); }
}

async function loadForecast() {
  try {
    const r = await fetch("/api/weather/forecast");
    const d = await r.json();
    const list = document.getElementById("forecast-list");
    if (!list) return;
    list.innerHTML = "";
    (d.forecast || []).forEach(day => {
      const li = document.createElement("li");
      li.style.textAlign = "center";
      li.style.flex = "1";
      const date = new Date(day.date);
      const dStr = date.toLocaleDateString("de-DE", { weekday: "short", day: "numeric", month: "short" });
      const icon = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;
      li.innerHTML = `
        <div>${dStr}</div>
        <img src="${icon}" alt="${day.description}" style="width:40px;height:40px;display:block;margin:8px auto;"/>
        <div>${day.temp_min}° – ${day.temp_max}°</div>`;
      list.appendChild(li);
    });
  } catch(e) { console.error("Forecast Fehler:", e); }
}

async function loadCalendar() {
  try {
    const r = await fetch("/api/calendar");
    const events = await r.json();
    const list = document.getElementById("event-list");
    if (!list) return;
    list.innerHTML = "";
    if (!events.length) {
      list.innerHTML = "<li>Keine Termine</li>";
      return;
    }
    const colors = ["#4caf50","#2196f3","#ff9800","#e91e63","#9c27b0","#00bcd4"];
    const grouped = {};
    events.forEach((ev, i) => {
      const start = new Date(ev.start);
      const dateKey = `${start.getFullYear()}-${String(start.getMonth()+1).padStart(2,"0")}-${String(start.getDate()).padStart(2,"0")}`;
      if (!grouped[dateKey]) grouped[dateKey] = [];
      grouped[dateKey].push({ ev, color: colors[i % colors.length] });
    });
    const dates = Object.keys(grouped).sort();
    dates.forEach(dateStr => {
      const date = new Date(dateStr);
      const dateHeading = document.createElement("h3");
      dateHeading.textContent = date.toLocaleDateString("de-DE", { weekday: "long", day: "numeric", month: "long" });
      list.appendChild(dateHeading);
      grouped[dateStr].forEach(({ ev, color }) => {
        const isAllDay = ev.start.length === 10;
        const timeStr = isAllDay ? "Ganztägig" :
          new Date(ev.start).toLocaleString("de-DE", { weekday: "short", day: "numeric", month: "short",
            hour: "2-digit", minute: "2-digit" });
        const li = document.createElement("li");
        li.style.borderLeftColor = color;
        li.innerHTML = `<strong>${ev.title}</strong><div class="event-time">${timeStr}</div>`;
        list.appendChild(li);
      });
    });
  } catch(e) { console.error("Kalender Fehler:", e); }
}

setBackground();
updateClock();
loadWeather();
loadCalendar();

setInterval(updateClock, 1000);
setInterval(loadWeather, 10 * 60 * 1000);
setInterval(loadForecast, 60 * 60 * 1000);
setInterval(loadCalendar, 5 * 60 * 1000);
setInterval(setBackground, 30 * 60 * 1000);
