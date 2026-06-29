# Visión de arquitectura

## Estrategia general

El proyecto se organiza como un monorepo para facilitar el desarrollo conjunto de frontend, backend y sincronización.

## Componentes

- Frontend: interfaz tablet-first y modo infantil.
- Backend: API para familias, miembros, categorías y timeline.
- Worker: sincronización con Google Calendar y normalización de eventos.

## Decisiones iniciales

- Monorepo simple al principio.
- Frontend sin framework pesado para la primera demo.
- Backend preparado para crecer hacia FastAPI.
- Datos de ejemplo para probar la interfaz rápidamente.
