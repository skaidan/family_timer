from typing import Any

from app.services.activity_normalizer import ActivityNormalizer
from app.services.visualization_rules import VisualizationRules


class TimelineService:
    def __init__(self) -> None:
        self.normalizer = ActivityNormalizer()
        self.visualization_rules = VisualizationRules()

    def build_timeline_by_member(self) -> dict[str, Any]:
        members = [
            {
                "name": "Mamá",
                "color": "#6ad8ff",
                "activities": [
                    {"summary": "sleep", "start": 6.0, "end": 7.0, "source": "demo"},
                    {"summary": "breakfast", "start": 7.0, "end": 8.0, "source": "demo"},
                    {"summary": "school", "start": 8.0, "end": 12.0, "source": "demo"},
                    {"summary": "lunch", "start": 12.0, "end": 13.0, "source": "demo"},
                    {"summary": "play", "start": 13.0, "end": 17.0, "source": "demo"},
                ],
            },
            {
                "name": "Papá",
                "color": "#ff6ea8",
                "activities": [
                    {"summary": "sleep", "start": 6.0, "end": 7.0, "source": "demo"},
                    {"summary": "bath", "start": 7.0, "end": 7.5, "source": "demo"},
                    {"summary": "work", "start": 7.5, "end": 13.0, "source": "demo"},
                    {"summary": "lunch", "start": 13.0, "end": 14.0, "source": "demo"},
                    {"summary": "meeting", "start": 14.0, "end": 17.0, "source": "demo"},
                ],
            },
            {
                "name": "Lucía",
                "color": "#4bcf92",
                "activities": [
                    {"summary": "sleep", "start": 6.0, "end": 7.0, "source": "demo"},
                    {"summary": "bath", "start": 7.0, "end": 7.3, "source": "demo"},
                    {"summary": "breakfast", "start": 7.3, "end": 8.0, "source": "demo"},
                    {"summary": "school", "start": 8.0, "end": 12.0, "source": "demo"},
                    {"summary": "lunch", "start": 12.0, "end": 13.0, "source": "demo"},
                    {"summary": "play", "start": 13.0, "end": 17.0, "source": "demo"},
                ],
            },
            {
                "name": "Leo",
                "color": "#ffcf5c",
                "activities": [
                    {"summary": "sleep", "start": 6.0, "end": 7.0, "source": "demo"},
                    {"summary": "bath", "start": 7.0, "end": 7.4, "source": "demo"},
                    {"summary": "breakfast", "start": 7.4, "end": 8.0, "source": "demo"},
                    {"summary": "play", "start": 8.0, "end": 10.0, "source": "demo"},
                    {"summary": "free_time", "start": 10.0, "end": 12.0, "source": "demo"},
                ],
            },
        ]

        normalized_members = []
        for member in members:
            normalized_activities = [self.normalizer.normalize(activity) for activity in member["activities"]]
            member_style = self.visualization_rules.get_member_style(member["name"])
            for activity in normalized_activities:
                activity_type = activity.get("type", "custom")
                style = self.visualization_rules.get_activity_style(activity_type)
                activity["label"] = style.get("label", activity.get("label", "Actividad"))
                activity["icon"] = style.get("icon", activity.get("icon", "📌"))
                activity["visual"] = {
                    "color": member_style["color"],
                    "member_icon": member_style["icon"],
                }

            normalized_members.append({
                "name": member["name"],
                "color": member_style["color"],
                "activities": normalized_activities,
            })

        return {"members": normalized_members}
