from apps.backend.app.services.google_event_assigner import GoogleEventAssigner


def test_assign_event_by_summary_keyword():
    assigner = GoogleEventAssigner()
    events = [
        {"summary": "Reunión Papá", "description": "", "location": "", "attendees": []}
    ]

    assignment = assigner.assign(events, [{"name": "Papá"}])

    assert assignment["Papá"][0]["summary"] == "Reunión Papá"


def test_assign_event_by_description_keyword():
    assigner = GoogleEventAssigner()
    events = [
        {"summary": "Evento", "description": "Clase de Lucía", "location": "", "attendees": []}
    ]

    assignment = assigner.assign(events, [{"name": "Lucía"}])

    assert assignment["Lucía"]


def test_assign_event_by_attendee():
    assigner = GoogleEventAssigner()
    events = [
        {
            "summary": "Juego",
            "description": "",
            "location": "",
            "attendees": [{"displayName": "Mamá"}],
        }
    ]

    assignment = assigner.assign(events, [{"name": "Mamá"}])

    assert assignment["Mamá"]


def test_unmatched_event_goes_to_google_calendar():
    assigner = GoogleEventAssigner()
    events = [
        {"summary": "Evento general", "description": "", "location": "", "attendees": []}
    ]

    assignment = assigner.assign(events, [{"name": "Papá"}])

    assert assignment["Google Calendar"]
