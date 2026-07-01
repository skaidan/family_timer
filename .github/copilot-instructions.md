Family Timer is a small full-stack prototype focused on a family timeline experience.

The backend is a FastAPI service in `apps/backend/app`. The frontend is a simple HTML/CSS/JavaScript prototype in `apps/frontend`.

Key areas:
- `docs/product`: product vision, MVP scope, roadmap and backlog.
- `docs/architecture`: Google Calendar integration and architecture notes.
- `apps/backend`: FastAPI API routes, Google Calendar client, timeline service, and normalization rules.
- `apps/frontend`: UI prototype, data fetching, and Google Calendar OAuth flow.

Important endpoints:
- `GET /health`
- `GET /api/timeline` optionally accepts `google_access_token`
- `GET /google-calendar/auth-url`
- `POST /google-calendar/token`
- `GET /google-calendar/events`

Environment and running:
- Uses Docker Compose from the repo root: `docker compose up --build`.
- Backend listens on port `8001` and frontend on port `8080`.
- Google Calendar config is loaded from `.env` via `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REDIRECT_URI`.

Testing:
- Use `pytest -q` from the repository root.

Agent guidance:
- Prefer small, minimal changes that preserve the current prototype structure.
- Avoid changing generated or runtime artifacts like `__pycache__` files.
- Focus backend work in `apps/backend` and frontend integration in `apps/frontend`.
- Use `docs/product` and `docs/architecture` for product/architecture context and to align with the current plan.

Existing custom agents:
- `python-senior-developer`: backend architecture, tests, refactoring.
- `product-owner`: product scope, user stories, and UX requirements.

If a change involves Google Calendar, keep the flow simple: OAuth auth URL -> token exchange -> fetch events -> timeline rendering.