const familyMembers = [
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

function renderRows() {
  rows.innerHTML = '';
  const now = getCurrentHour();

  familyMembers.forEach((member) => {
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

  const activeIndex = familyMembers[2].activities.findIndex((activity) => activity.start <= now && now < activity.end);
  const currentActivity = familyMembers[2].activities[activeIndex] || familyMembers[2].activities[0];
  const nextActivity = familyMembers[2].activities[activeIndex + 1] || familyMembers[2].activities[0];
  const freeMinutes = Math.max(0, Math.round((nextActivity.start - now) * 60));

  currentTitle.textContent = `${currentActivity.icon} ${currentActivity.label}`;
  currentDescription.textContent = `Ahora mismo la familia está en ${currentActivity.label.toLowerCase()} y el tiempo sigue avanzando.`;
  nextTitle.textContent = `${nextActivity.icon} ${nextActivity.label}`;
  freeTime.textContent = `${freeMinutes} min`;
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
renderRows();
placeNowCursor();
modeToggle.addEventListener('click', toggleKidsMode);
setInterval(() => {
  renderRows();
  placeNowCursor();
}, 60000);
