from typing import Any


class VisualizationRules:
    """Reglas simples de visualización para adaptar la UI a cada miembro y actividad."""

    MEMBER_STYLES = {
        "Mamá": {"color": "#6ad8ff", "icon": "👩"},
        "Papá": {"color": "#ff6ea8", "icon": "👨"},
        "Lucía": {"color": "#4bcf92", "icon": "👧"},
        "Leo": {"color": "#ffcf5c", "icon": "🧒"},
    }

    ACTIVITY_STYLES = {
        "sleep": {"label": "Dormir", "icon": "🛏️", "type": "sleep"},
        "eat": {"label": "Comer", "icon": "🍽️", "type": "eat"},
        "school": {"label": "Cole", "icon": "🎒", "type": "school"},
        "play": {"label": "Juego", "icon": "🎲", "type": "play"},
        "work": {"label": "Trabajo", "icon": "💼", "type": "work"},
        "hygiene": {"label": "Baño", "icon": "🚿", "type": "hygiene"},
        "custom": {"label": "Actividad", "icon": "📌", "type": "custom"},
    }

    def get_member_style(self, member_name: str) -> dict[str, Any]:
        return self.MEMBER_STYLES.get(member_name, {"color": "#7c8cff", "icon": "👤"})

    def get_activity_style(self, activity_type: str) -> dict[str, Any]:
        return self.ACTIVITY_STYLES.get(activity_type, self.ACTIVITY_STYLES["custom"])
