# Integración con Google Calendar

## Objetivo

Permitir que la aplicación lea eventos desde Google Calendar y los convierta en bloques visuales de la timeline.

## Flujo propuesto

1. El usuario inicia el flujo de autenticación con Google.
2. La app obtiene permisos de lectura del calendario.
3. El backend recupera eventos del calendario configurado.
4. Los eventos se normalizan a categorías visuales como dormir, comer, cole, baño o juego.
5. La timeline se actualiza con esos bloques.

## Variables de entorno esperadas

- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GOOGLE_REDIRECT_URI
- GOOGLE_SCOPES

> Si no se configuran `GOOGLE_CLIENT_ID` y `GOOGLE_REDIRECT_URI`, el endpoint de autorización devuelve un error y no se inicia el flujo OAuth.

## Configuración local recomendada

Crea un archivo `.env` en la raíz del proyecto con los valores de tu app de Google Cloud. Puedes usar el siguiente ejemplo como plantilla:

```env
GOOGLE_CLIENT_ID=<tu-client-id>
GOOGLE_CLIENT_SECRET=<tu-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8080
GOOGLE_SCOPES=https://www.googleapis.com/auth/calendar.readonly
```

Luego vuelve a levantar la app con Docker Compose:

```bash
docker compose up --build
```

## Primer paso del MVP

Implementar un endpoint que devuelva eventos de ejemplo y preparar la estructura para reemplazarlo por datos reales desde la API de Google.

## Endpoints clave

- `GET /google-calendar/auth-url`: devuelve la URL de autorización de Google.
- `POST /google-calendar/token`: intercambia el código de autorización por tokens OAuth.
- `GET /google-calendar/events`: recupera eventos reales del calendario usando `access_token`.
