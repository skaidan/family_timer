from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .api.v1.google_calendar import router as google_calendar_router
from .api.v1.timeline import router as timeline_router

app = FastAPI(title="Family Timer API")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_calendar_router)
app.include_router(timeline_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/timeline")
def timeline() -> dict[str, object]:
    return {
        "members": [
            {
                "name": "Mamá",
                "color": "#6ad8ff",
                "activities": [
                    {"start": 6.5, "end": 7.2, "label": "Dormir", "icon": "🛏️", "type": "sleep"},
                    {"start": 7.2, "end": 8.0, "label": "Desayuno", "icon": "🍽️", "type": "eat"},
                    {"start": 8.0, "end": 12.0, "label": "Trabajo", "icon": "💼", "type": "work"},
                    {"start": 12.0, "end": 13.0, "label": "Comer", "icon": "🥗", "type": "eat"},
                    {"start": 13.0, "end": 16.0, "label": "Cole", "icon": "🎒", "type": "school"},
                    {"start": 16.0, "end": 18.0, "label": "Juego", "icon": "🎲", "type": "play"},
                    {"start": 18.0, "end": 20.0, "label": "Cena", "icon": "🍲", "type": "eat"},
                ],
            },
            {
                "name": "Papá",
                "color": "#ff6ea8",
                "activities": [
                    {"start": 6.0, "end": 7.0, "label": "Dormir", "icon": "🛏️", "type": "sleep"},
                    {"start": 7.0, "end": 7.5, "label": "Aseo", "icon": "🪥", "type": "hygiene"},
                    {"start": 7.5, "end": 13.0, "label": "Trabajo", "icon": "💻", "type": "work"},
                    {"start": 13.0, "end": 14.0, "label": "Comer", "icon": "🥪", "type": "eat"},
                    {"start": 14.0, "end": 17.0, "label": "Reunión", "icon": "📞", "type": "work"},
                    {"start": 17.0, "end": 19.0, "label": "Parque", "icon": "🌳", "type": "play"},
                ],
            },
            {
                "name": "Lucía",
                "color": "#4bcf92",
                "activities": [
                    {"start": 6.0, "end": 7.0, "label": "Dormir", "icon": "🛏️", "type": "sleep"},
                    {"start": 7.0, "end": 7.3, "label": "Aseo", "icon": "🪥", "type": "hygiene"},
                    {"start": 7.3, "end": 8.0, "label": "Desayuno", "icon": "🥣", "type": "eat"},
                    {"start": 8.0, "end": 12.0, "label": "Cole", "icon": "🎒", "type": "school"},
                    {"start": 12.0, "end": 13.0, "label": "Comer", "icon": "🍽️", "type": "eat"},
                    {"start": 13.0, "end": 17.0, "label": "Parque", "icon": "🛝", "type": "play"},
                    {"start": 17.0, "end": 19.0, "label": "Juego libre", "icon": "🧩", "type": "play"},
                ],
            },
            {
                "name": "Leo",
                "color": "#ffcf5c",
                "activities": [
                    {"start": 6.0, "end": 7.0, "label": "Dormir", "icon": "🛏️", "type": "sleep"},
                    {"start": 7.0, "end": 7.4, "label": "Baño", "icon": "🚿", "type": "hygiene"},
                    {"start": 7.4, "end": 8.0, "label": "Desayuno", "icon": "🍞", "type": "eat"},
                    {"start": 8.0, "end": 10.0, "label": "Jugar", "icon": "🧸", "type": "play"},
                    {"start": 10.0, "end": 12.0, "label": "Pintar", "icon": "🎨", "type": "creative"},
                    {"start": 12.0, "end": 13.0, "label": "Comer", "icon": "🍽️", "type": "eat"},
                    {"start": 13.0, "end": 16.0, "label": "Siesta", "icon": "😴", "type": "sleep"},
                ],
            },
        ]
    }
