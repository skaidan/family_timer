# Todo y estado del proyecto

## Estado general

Family Timer ya cuenta con una base funcional para mostrar una línea de tiempo familiar visual y comprensible en una pantalla tipo tablet.

## ✅ Completado

- Definición de producto y alcance MVP.
- Documentación inicial de visión, arquitectura y roadmap.
- Prototipo visual de interfaz con timeline, cursor "ahora" y selector de día.
- Backend mínimo con FastAPI.
- Endpoint de timeline para servir datos estructurados.
- Normalización de actividades a un modelo visual común.
- Modelo de timeline organizado por miembro de la familia.
- Reglas básicas de visualización por miembro y tipo de actividad.
- Ejecución local con Docker Compose.

## 🔄 En progreso

- Integración con Google Calendar usando un flujo preparado, pero aún sin sincronización real.
- Afinado visual de la experiencia infantil y del modo padres.

## ⏳ Pendiente

- Conectar eventos reales de Google Calendar.
- Mapear automáticamente eventos a categorías visuales.
- Permitir personalizar colores, iconos y reglas desde la interfaz.
- Añadir más interacción para marcar tareas como en curso o completadas.
- Mejorar la vista de tiempo libre entre actividades.

## 🔎 Cómo revisar el estado actual

- Frontend: http://localhost:8080
- Backend health: http://localhost:8001/health
- Backend timeline: http://localhost:8001/api/timeline
