from typing import Any


class GoogleEventAssigner:
    MEMBER_KEYWORDS = {
        "Mamá": ["mamá", "mama", "mamá"],
        "Papá": ["papá", "papa", "papá"],
        "Lucía": ["lucía", "lucia"],
        "Leo": ["leo"],
    }

    def assign(self, events: list[dict[str, Any]], members: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        assignment = {member["name"]: [] for member in members}
        assignment["Google Calendar"] = []

        for event in events:
            target = self._find_member_target(event)
            if target and target in assignment:
                assignment[target].append(event)
            else:
                assignment["Google Calendar"].append(event)

        return assignment

    def _find_member_target(self, event: dict[str, Any]) -> str | None:
        text = self._event_text(event)
        for member, terms in self.MEMBER_KEYWORDS.items():
            for term in terms:
                if term in text:
                    return member
        return None

    def _event_text(self, event: dict[str, Any]) -> str:
        fields = [
            event.get("summary", ""),
            event.get("description", ""),
            event.get("location", ""),
        ]
        attendees = event.get("attendees", [])
        organizer = event.get("organizer")
        if isinstance(attendees, list):
            fields.extend(
                str(attendee.get("displayName", ""))
                for attendee in attendees
                if isinstance(attendee, dict)
            )
        if isinstance(organizer, dict):
            fields.append(str(organizer.get("displayName", "")))

        return self._normalize_text(" ".join(fields))

    def _normalize_text(self, value: str) -> str:
        translation = str.maketrans(
            "áéíóúüñÀÁÉÍÓÚÜÑ",
            "aeiouunAAEIOUUN",
        )
        return value.lower().translate(translation)
