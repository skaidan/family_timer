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
        category = self.CATEGORY_MAP.get(summary)
        if category is None:
            category = self.CATEGORY_MAP.get(preferred_type)
        if category is None:
            for term, value in self.CATEGORY_MAP.items():
                if term in summary:
                    category = value
                    break
        if category is None:
            category = {"label": "Actividad", "icon": "📌", "type": "custom"}

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
