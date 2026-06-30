from typing import Any

from ..integrations.google_calendar import GoogleCalendarClient
from .activity_normalizer import ActivityNormalizer
from .visualization_rules import VisualizationRules


class TimelineService:
    def __init__(self) -> None:
        self.normalizer = ActivityNormalizer()
        self.visualization_rules = VisualizationRules()
        self.google_client = GoogleCalendarClient()

    def build_timeline_by_member(self, google_access_token: str | None = None) -> dict[str, Any]:
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

        google_events: list[dict[str, Any]] = []
        if google_access_token:
            try:
                google_events = self.google_client.fetch_events(google_access_token)
            except Exception:
                google_events = []

        if google_events:
            assignment = self._assign_google_events_to_members(google_events)
            for member in members:
                member_events = assignment.pop(member["name"], [])
                if member_events:
                    member["activities"].extend(member_events)
            if assignment.get("Google Calendar"):
                members.append({
                    "name": "Google Calendar",
                    "color": "#ffcf5c",
                    "activities": assignment["Google Calendar"],
                })

        normalized_members = []
        for member in members:
            normalized_activities = [self.normalizer.normalize(activity) for activity in member["activities"]]
            member_style = self.visualization_rules.get_member_style(
                member["name"],
                default_color=member.get("color", "#7c8cff"),
                default_icon=member.get("icon", "👤"),
            )
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

    def _normalize_text(self, value: str) -> str:
        translation = str.maketrans(
            "áéíóúüñÀÁÉÍÓÚÜÑ",
            "aeiouunAAEIOUUN",
        )
        return value.lower().translate(translation)

    def _assign_google_events_to_members(self, events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        assignment = {
            "Mamá": [],
            "Papá": [],
            "Lucía": [],
            "Leo": [],
            "Google Calendar": [],
        }
        keywords = {
            "Mamá": ["mamá", "mama", "mamá"],
            "Papá": ["papá", "papa", "papá"],
            "Lucía": ["lucía", "lucia"],
            "Leo": ["leo"],
        }

        for event in events:
            text = self._normalize_text(
                " ".join(
                    str(event.get(field, "")) for field in ["summary", "description", "location"]
                )
            )
            target = None
            for member, terms in keywords.items():
                normalized_terms = [self._normalize_text(term) for term in terms]
                if any(term in text for term in normalized_terms):
                    target = member
                    break

            if target:
                assignment[target].append(event)
            else:
                assignment["Google Calendar"].append(event)

        return assignment
