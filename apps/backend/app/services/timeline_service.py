from typing import Any

from ..integrations.google_calendar import GoogleCalendarClient
from .activity_normalizer import ActivityNormalizer
from .google_event_assigner import GoogleEventAssigner
from .visualization_rules import VisualizationRules


class TimelineService:
    def __init__(
        self,
        google_client: GoogleCalendarClient | None = None,
        assigner: GoogleEventAssigner | None = None,
    ) -> None:
        self.normalizer = ActivityNormalizer()
        self.visualization_rules = VisualizationRules()
        self.google_client = google_client or GoogleCalendarClient()
        self.assigner = assigner or GoogleEventAssigner()

    def build_timeline_by_member(
        self,
        google_access_token: str | None = None,
    ) -> dict[str, Any]:
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
            assignment = self.assigner.assign(google_events, members)
            for member in members:
                member_events = assignment.pop(member["name"], [])
                if member_events:
                    member["activities"].extend(member_events)
            if assignment.get("Google Calendar"):
                members.append(
                    {
                        "name": "Google Calendar",
                        "color": "#ff6ea8",
                        "activities": assignment["Google Calendar"],
                    }
                )

        normalized_members = []
        for member in members:
            normalized_activities = [
                activity
                for activity in (
                    self.normalizer.normalize(activity) for activity in member["activities"]
                )
                if activity.get("start") is not None and activity.get("end") is not None
            ]
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
