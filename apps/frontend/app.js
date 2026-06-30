const fallbackFamilyMembers = [
  { name: 'Mamá', color: '#6ad8ff', activities: [
    { start: 6.5, end: 7.2, label: 'Dormir', icon: '🛏️', type: 'sleep' },
    { start: 7.2, end: 8.0, label: 'Desayuno', icon: '🍽️', type: 'eat' },
    { start: 8.0, end: 12.0, label: 'Trabajo', icon: '💼', type: 'work' },
    { start: 12.0, end: 13.0, label: 'Comer', icon: '🥗', type: 'eat' },
    { start: 13.0, end: 16.0, label: 'Cole', icon: '🎒', type: 'school' },
    { start: 16.0, end: 18.0, label: 'Juego', icon: '🎲', type: 'play' },
    { start: 18.0, end: 20.0, label: 'Cena', icon: '🍲', type: 'eat' },
  ]},
  { name: 'Papá', color: '#ff6ea8', activities: [
    { start: 6.0, end: 7.0, label: 'Dormir', icon: '🛏️', type: 'sleep' },
    { start: 7.0, end: 7.5, label: 'Aseo', icon: '🪥', type: 'hygiene' },
    { start: 7.5, end: 13.0, label: 'Trabajo', icon: '💻', type: 'work' },
    { start: 13.0, end: 14.0, label: 'Comer', icon: '🥪', type: 'eat' },
    { start: 14.0, end: 17.0, label: 'Reunión', icon: '📞', type: 'work' },
    { start: 17.0, end: 19.0, label: 'Parque', icon: '🌳', type: 'play' },
  ]},
  { name: 'Lucía', color: '#4bcf92', activities: [
    { start: 6.0, end: 7.0, label: 'Dormir', icon: '🛏️', type: 'sleep' },
    { start: 7.0, end: 7.3, label: 'Aseo', icon: '🪥', type: 'hygiene' },
    { start: 7.3, end: 8.0, label: 'Desayuno', icon: '🥣', type: 'eat' },
    { start: 8.0, end: 12.0, label: 'Cole', icon: '🎒', type: 'school' },
    { start: 12.0, end: 13.0, label: 'Comer', icon: '🍽️', type: 'eat' },
    { start: 13.0, end: 17.0, label: 'Parque', icon: '🛝', type: 'play' },
    { start: 17.0, end: 19.0, label: 'Juego libre', icon: '🧩', type: 'play' },
  ]},
  { name: 'Leo', color: '#ffcf5c', activities: [
    { start: 6.0, end: 7.0, label: 'Dormir', icon: '🛏️', type: 'sleep' },
    { start: 7.0, end: 7.4, label: 'Baño', icon: '🚿', type: 'hygiene' },
    { start: 7.4, end: 8.0, label: 'Desayuno', icon: '🍞', type: 'eat' },
    { start: 8.0, end: 10.0, label: 'Jugar', icon: '🧸', type: 'play' },
    { start: 10.0, end: 12.0, label: 'Pintar', icon: '🎨', type: 'creative' },
    { start: 12.0, end: 13.0, label: 'Comer', icon: '🍽️', type: 'eat' },
    { start: 13.0, end: 16.0, label: 'Siesta', icon: '😴', type: 'sleep' },
  ]}
];

let familyMembers = [...fallbackFamilyMembers];

const startHour = 6;
const endHour = 20;
const visibleHours = endHour - startHour;
const nowCursor = document.getElementById('now-cursor');
const rows = document.getElementById('rows');
const timeAxis = document.getElementById('time-axis');
const currentTitle = document.getElementById('current-title');
const currentDescription = document.getElementById('current-description');
const nextTitle = document.getElementById('next-title');
const freeTime = document.getElementById('free-time');
const modeToggle = document.getElementById('mode-toggle');
const daySelector = document.getElementById('day-selector');
const timeRemaining = document.getElementById('time-remaining');
const googleAuthButton = document.getElementById('google-auth-button');
const googleSyncStatus = document.getElementById('google-sync-status');

const backendBase = 'http://127.0.0.1:8001';
const googleApiBase = `${backendBase}/google-calendar`;
let googleAccessToken = localStorage.getItem('family_timer_google_token');

function getQueryParams() {
  return Object.fromEntries(new URLSearchParams(window.location.search));
}

function setGoogleAccessToken(token) {
  googleAccessToken = token;
  if (token) {
    localStorage.setItem('family_timer_google_token', token);
  } else {
    localStorage.removeItem('family_timer_google_token');
  }
}

function updateGoogleStatus(message) {
  if (googleSyncStatus) {
    googleSyncStatus.textContent = message;
  }
}

function updateGoogleButton() {
  if (googleAuthButton) {
    googleAuthButton.textContent = googleAccessToken ? 'Google Calendar conectado' : 'Conectar Google Calendar';
  }
}

function getTimelineMembers() {
  return [...familyMembers];
}

async function connectGoogleCalendar() {
  try {
    const response = await fetch(`${googleApiBase}/auth-url`);
    if (!response.ok) throw new Error('No se pudo obtener la URL de autorización.');

    const data = await response.json();
    if (data.auth_url) {
      window.location.href = data.auth_url;
    } else {
      throw new Error('La URL de autorización no está disponible.');
    }
  } catch (error) {
    updateGoogleStatus('Error al iniciar conexión con Google Calendar');
    console.error(error);
  }
}

async function exchangeCode(code) {
  try {
    const response = await fetch(`${googleApiBase}/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });

    if (!response.ok) {
      throw new Error('Falló el intercambio de código OAuth.');
    }

    const data = await response.json();
    if (data.access_token) {
      setGoogleAccessToken(data.access_token);
      updateGoogleStatus('Google Calendar conectado');
      updateGoogleButton();
      await loadTimeline();
      await renderRows();
    } else {
      throw new Error('No se recibió access_token de Google.');
    }
  } catch (error) {
    setGoogleAccessToken(null);
    updateGoogleStatus('Error al intercambiar el código de Google.');
    console.error(error);
  }
}

function makeTimeAxis() {
  timeAxis.innerHTML = '';
  for (let hour = startHour; hour <= endHour; hour += 2) {
    const tick = document.createElement('div');
    tick.textContent = `${String(hour).padStart(2, '0')}:00`;
    timeAxis.appendChild(tick);
  }
}

function getCurrentHour() {
  const now = new Date();
  return now.getHours() + now.getMinutes() / 60;
}

function getSelectedDayOffset() {
  return daySelector.value === 'tomorrow' ? 1 : 0;
}

async function loadTimeline() {
  try {
    const token = googleAccessToken || localStorage.getItem('family_timer_google_token');
    const query = token ? `?google_access_token=${encodeURIComponent(token)}` : '';
    const response = await fetch(`${backendBase}/timeline${query}`);
    if (!response.ok) throw new Error('No se pudo cargar la timeline');
    const data = await response.json();

    if (Array.isArray(data.members)) {
      familyMembers = data.members.map((member) => ({
        ...member,
        activities: member.activities || [],
      }));
    }
  } catch (error) {
    familyMembers = [...fallbackFamilyMembers];
  }
}

async function renderRows() {
  rows.innerHTML = '';
  const now = getCurrentHour();
  const selectedDayOffset = getSelectedDayOffset();

  if (selectedDayOffset !== 0) {
    currentDescription.textContent = 'Vista de mañana preparada para la siguiente iteración.';
    currentTitle.textContent = '🗓️ Mañana';
    nextTitle.textContent = '—';
    freeTime.textContent = '—';
    timeRemaining.textContent = 'Tiempo restante: pendiente de sincronizar';
    return;
  }

  const timelineMembers = getTimelineMembers();

  timelineMembers.forEach((member) => {
    const row = document.createElement('div');
    row.className = 'row';

    const label = document.createElement('div');
    label.className = 'row-label';
    label.textContent = member.name;

    const track = document.createElement('div');
    track.className = 'row-track';

    member.activities.forEach((activity) => {
      const left = ((activity.start - startHour) / visibleHours) * 100;
      const width = ((activity.end - activity.start) / visibleHours) * 100;
      const segment = document.createElement('div');
      segment.className = 'segment';
      if (activity.end <= now) segment.classList.add('past');
      else if (activity.start <= now && now < activity.end) segment.classList.add('current');
      else segment.classList.add('future');
      segment.style.left = `${left}%`;
      segment.style.width = `${Math.max(width, 8)}%`;
      segment.style.background = `linear-gradient(135deg, ${member.color}, ${member.color}cc)`;
      segment.innerHTML = `<span class="icon">${activity.icon}</span><span>${activity.label}</span>`;
      track.appendChild(segment);
    });

    row.appendChild(label);
    row.appendChild(track);
    rows.appendChild(row);
  });

  const primaryMember = timelineMembers[0] || { activities: [] };
  const activeIndex = primaryMember.activities.findIndex((activity) => activity.start <= now && now < activity.end);
  const currentActivity = primaryMember.activities[activeIndex] || primaryMember.activities[0] || { icon: '⏳', label: 'Sin actividad', start: now, end: now };
  const nextActivity = primaryMember.activities[activeIndex + 1] || primaryMember.activities[0] || currentActivity;
  const freeMinutes = Math.max(0, Math.round((nextActivity.start - now) * 60));
  const remainingMinutes = Math.max(0, Math.round((currentActivity.end - now) * 60));

  currentTitle.textContent = `${currentActivity.icon} ${currentActivity.label}`;
  currentDescription.textContent = `Ahora mismo la familia está en ${currentActivity.label.toLowerCase()} y el tiempo sigue avanzando.`;
  nextTitle.textContent = `${nextActivity.icon} ${nextActivity.label}`;
  freeTime.textContent = `${freeMinutes} min`;
  timeRemaining.textContent = `Tiempo restante: ${remainingMinutes} min`;
}

function placeNowCursor() {
  const now = getCurrentHour();
  const ratio = (now - startHour) / visibleHours;
  const leftPercent = Math.min(Math.max(ratio * 100, 0), 100);
  nowCursor.style.left = `${leftPercent}%`;
}

function toggleKidsMode() {
  document.body.classList.toggle('kids-mode');
  modeToggle.textContent = document.body.classList.contains('kids-mode') ? 'Modo padres' : 'Modo niños';
}

makeTimeAxis();
(async () => {
  const params = getQueryParams();
  if (params.code) {
    await exchangeCode(params.code);
    const cleanUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, cleanUrl);
  } else {
    updateGoogleStatus(googleAccessToken ? 'Google Calendar conectado' : 'Sin conexión a Google Calendar');
  }

  updateGoogleButton();
  await loadTimeline();
  await renderRows();
  placeNowCursor();
})();

if (googleAuthButton) {
  googleAuthButton.addEventListener('click', connectGoogleCalendar);
}

modeToggle.addEventListener('click', toggleKidsMode);
daySelector.addEventListener('change', renderRows);
setInterval(() => {
  renderRows();
  placeNowCursor();
}, 60000);
