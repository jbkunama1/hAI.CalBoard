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
    document.getElementById("weather-temp").textContent = `${d.temp}°C`;
    document.getElementById("weather-desc").textContent = d.description;
    document.getElementById("weather-icon").src =
      `https://openweathermap.org/img/wn/${d.icon}@2x.png`;
  } catch(e) { console.error("Wetter Fehler:", e); }
}

async function loadCalendar() {
  try {
    const r = await fetch("/api/calendar");
    const events = await r.json();
    const list = document.getElementById("event-list");
    list.innerHTML = "";
    if (!events.length) {
      list.innerHTML = "<li>Keine Termine</li>"; return;
    }
    const colors = ["#4caf50","#2196f3","#ff9800","#e91e63","#9c27b0"];
    events.slice(0, 8).forEach((ev, i) => {
      const start = new Date(ev.start);
      const isAllDay = ev.start.length === 10;
      const timeStr = isAllDay ? "Ganztägig" :
        start.toLocaleString("de-DE", { weekday: "short", day: "numeric", month: "short",
          hour: "2-digit", minute: "2-digit" });
      const li = document.createElement("li");
      li.style.borderLeftColor = colors[i % colors.length];
      li.innerHTML = `<strong>${ev.title}</strong><div class="event-time">${timeStr}</div>`;
      list.appendChild(li);
    });
  } catch(e) { console.error("Kalender Fehler:", e); }
}

setBackground();
updateClock();
loadWeather();
loadCalendar();

setInterval(updateClock, 1000);
setInterval(loadWeather, 10 * 60 * 1000);
setInterval(loadCalendar, 5 * 60 * 1000);
setInterval(setBackground, 30 * 60 * 1000);
