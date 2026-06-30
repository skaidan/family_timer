from datetime import datetime, date, time, timedelta
from typing import Any


class ActivityNormalizer:
    """Convierte eventos de distintas fuentes a un formato visual consistente."""

    CATEGORY_MAP = {
        "sleep": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "bedtime": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "rest": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "breakfast": {"label": "Desayuno", "icon": "🍽️", "type": "eat"},
        "desayuno": {"label": "Desayuno", "icon": "🍽️", "type": "eat"},
        "lunch": {"label": "Comer", "icon": "🥗", "type": "eat"},
        "almuerzo": {"label": "Comer", "icon": "🥗", "type": "eat"},
        "dinner": {"label": "Cena", "icon": "🍲", "type": "eat"},
        "cena": {"label": "Cena", "icon": "🍲", "type": "eat"},
        "meal": {"label": "Comer", "icon": "🥗", "type": "eat"},
        "school": {"label": "Cole", "icon": "🎒", "type": "school"},
        "cole": {"label": "Cole", "icon": "🎒", "type": "school"},
        "escuela": {"label": "Cole", "icon": "🎒", "type": "school"},
        "class": {"label": "Cole", "icon": "🎒", "type": "school"},
        "bath": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "baño": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "shower": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "play": {"label": "Juego", "icon": "🎲", "type": "play"},
        "juego": {"label": "Juego", "icon": "🎲", "type": "play"},
        "free_time": {"label": "Tiempo libre", "icon": "🌈", "type": "play"},
        "libre": {"label": "Tiempo libre", "icon": "🌈", "type": "play"},
        "work": {"label": "Trabajo", "icon": "💼", "type": "work"},
        "trabajo": {"label": "Trabajo", "icon": "💼", "type": "work"},
        "meeting": {"label": "Reunión", "icon": "📞", "type": "work"},
        "reunión": {"label": "Reunión", "icon": "📞", "type": "work"},
        "siesta": {"label": "Siesta", "icon": "😴", "type": "sleep"},
        "parque": {"label": "Parque", "icon": "🌳", "type": "play"},
    }

    def normalize(self, raw_activity: dict[str, Any]) -> dict[str, Any]:
        summary = str(raw_activity.get("summary", "")).strip().lower()
        preferred_type = str(raw_activity.get("type", "")).strip().lower()
        category = None
        if preferred_type:
            category = self.CATEGORY_MAP.get(preferred_type)
        if category is None:
            category = self.CATEGORY_MAP.get(summary)
        if category is None:
            for term, value in self.CATEGORY_MAP.items():
                if term in summary:
                    category = value
                    break
        if category is None:
            category = {"label": "Actividad", "icon": "📌", "type": "custom"}

        start = raw_activity.get("start")
        end = raw_activity.get("end")
        start_dt = raw_activity.get("start_dt")
        end_dt = raw_activity.get("end_dt")

        if start is None or end is None:
            start, end = self._normalize_datetime_range(start_dt, end_dt)

        return {
            "label": category["label"],
            "icon": category["icon"],
            "type": category["type"],
            "start": start,
            "end": end,
            "source": raw_activity.get("source", "manual"),
        }

    def _normalize_datetime_range(
        self,
        start_dt: datetime | None,
        end_dt: datetime | None,
    ) -> tuple[float | None, float | None]:
        if not isinstance(start_dt, datetime) or not isinstance(end_dt, datetime):
            return None, None

        if start_dt.date() == end_dt.date():
            return self._to_hour(start_dt), self._to_hour(end_dt)

        # All-day events with a midnight end next day should map to full day
        if (
            start_dt.time() == time(0, 0)
            and end_dt.time() == time(0, 0)
            and end_dt.date() == start_dt.date() + timedelta(days=1)
        ):
            return 0.0, 24.0

        return None, None

    def _to_hour(self, value: datetime | date | None) -> float | None:
        if isinstance(value, datetime):
            return value.hour + value.minute / 60 + value.second / 3600
        if isinstance(value, date):
            return 0.0
        return None
