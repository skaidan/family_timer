# Family Timer

Family Timer es una propuesta de producto para ayudar a las familias a entender visualmente cuánto tiempo queda para cada actividad y cuánto tiempo libre hay entre tareas.

## Qué incluye esta primera versión

- Una propuesta de producto clara para MVP.
- Documentación de alcance, flujos y arquitectura.
- Un prototipo visual de interfaz tablet-first con timeline familiar, línea de "ahora" y modo infantil.
- Un sistema mínimo de Docker Compose para correr el frontend y el backend en local.
- Un backlog y estado de trabajo documentados en docs/product/todo.md.

## Enfoque actual del producto

- Priorizar la integración con Google Calendar para mostrar eventos reales.
- Normalizar eventos a categorías visuales simples y consistentes.
- Mostrar una timeline diaria por miembro con la actividad actual destacada.
- Añadir interacción básica para marcar tareas como "en curso" o "terminadas".
- Incorporar personalización inicial de colores, iconos y reglas desde el modo padres.
- Mantener un modo infantil sencillo y enfocado en el siguiente paso.

## Estructura del repositorio

- docs/product: alcance, flujos y wireframes.
- docs/architecture: visión de arquitectura y modelo de datos.
- apps/frontend: prototipo visual inicial en HTML, CSS y JavaScript.
- apps/backend: API mínima en FastAPI para servir la timeline.

## Cómo arrancarlo con Docker

1. Crea un archivo `.env` en la raíz del proyecto con los valores de Google Calendar. Usa `.env.example` como referencia.

```bash
cp .env.example .env
# editar .env y completar las variables de Google
```

2. Desde la raíz del proyecto:

```bash
docker compose up --build
```

2. Abrir en el navegador:

- Frontend: http://localhost:8080
- Backend health: http://localhost:8001/health
- Backend timeline: http://localhost:8001/api/timeline

## Cómo detenerlo

```bash
docker compose down
```
