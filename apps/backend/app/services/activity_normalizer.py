from typing import Any


class ActivityNormalizer:
    """Convierte eventos de distintas fuentes a un formato visual consistente."""

    CATEGORY_MAP = {
        "sleep": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "bedtime": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "breakfast": {"label": "Desayuno", "icon": "🍽️", "type": "eat"},
        "lunch": {"label": "Comer", "icon": "🥗", "type": "eat"},
        "dinner": {"label": "Cena", "icon": "🍲", "type": "eat"},
        "meal": {"label": "Comer", "icon": "🥗", "type": "eat"},
        "school": {"label": "Cole", "icon": "🎒", "type": "school"},
        "class": {"label": "Cole", "icon": "🎒", "type": "school"},
        "bath": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "shower": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "play": {"label": "Juego", "icon": "🎲", "type": "play"},
        "free_time": {"label": "Tiempo libre", "icon": "🌈", "type": "play"},
        "work": {"label": "Trabajo", "icon": "💼", "type": "work"},
        "meeting": {"label": "Reunión", "icon": "📞", "type": "work"},
    }

    def normalize(self, raw_activity: dict[str, Any]) -> dict[str, Any]:
        summary = str(raw_activity.get("summary", "")).strip().lower()
        category = self.CATEGORY_MAP.get(summary, self.CATEGORY_MAP.get(raw_activity.get("type", ""), {"label": "Actividad", "icon": "📌", "type": "custom"}))

        start = raw_activity.get("start")
        end = raw_activity.get("end")

        return {
            "label": category["label"],
            "icon": category["icon"],
            "type": category["type"],
            "start": start,
            "end": end,
            "source": raw_activity.get("source", "manual"),
        }
