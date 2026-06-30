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

- Conectar el backend con Google Calendar para recuperar eventos reales.
- Ajustar la experiencia visual para modo infantil y modo padres.
- Validar el flujo de datos entre frontend y backend en la vista de timeline.

## ⏭ Próximos pasos prioritarios

1. Establecer integración básica con Google Calendar
   - Autenticación OAuth en el backend.
   - Recuperar eventos del calendario familiar.
   - Mostrar eventos reales en el endpoint de timeline.

2. Normalizar eventos y mapearlos a categorías visuales
   - Crear reglas simples para convertir eventos en bloques de actividad.
   - Incluir categoría, tiempo de inicio/fin y miembro responsable.
   - Validar visualmente el mapeo en la interfaz.

3. Mejorar la interacción de la línea de tiempo
   - Permitir marcar una actividad como "en curso" o "terminada".
   - Mostrar claramente el tiempo libre entre actividades.
   - Resaltar la actividad actual y la siguiente.

4. Añadir personalización básica desde la interfaz
   - Selección de color por miembro de la familia.
   - Iconos y etiquetas para categorías principales.
   - Guardar ajustes de visualización localmente.

> Estas prioridades están alineadas con `docs/product/roadmap.md`, donde la fase 1 apunta a mejorar la utilidad, la fase 2 a personalización y la fase 3 a integrar datos reales.

## 🧭 Replanteamiento de siguientes pasos

- En lugar de un listado genérico de pendientes, trabajar por bloques incrementales: datos reales → normalización → interacción → personalización.
- Priorizar un ciclo rápido de valor: evento real visible en timeline, luego control de estado de tarea, y después ajustes visuales.
- Evitar lanzar varias mejoras al mismo tiempo; avanzar por etapas claras con demos emergentes.

## 🧪 Cómo revisar el estado actual

- Frontend: http://localhost:8080
- Backend health: http://localhost:8001/health
- Backend timeline: http://localhost:8001/api/timeline

## 📌 Nota de enfoque

El objetivo inmediato es validar que la app deja de ser solo un prototipo visual y empieza a funcionar con datos reales y acciones básicas del usuario. Después de eso, la prioridad es que la experiencia sea comprensible y personalizable para una familia.