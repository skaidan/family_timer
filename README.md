# Family Timer

Agenda diaria estática que muestra las tareas de varios calendarios en una línea de tiempo. Los datos se cargan desde [`data/calendars.json`](data/calendars.json).

## Requisitos

- Docker Engine con Docker Compose v2 (`docker compose`)

## Levantar con Docker Compose

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Abre [http://localhost:8080](http://localhost:8080) en el navegador. Para detener el contenedor:

```bash
docker compose down
```

## Levantar con Docker directamente

```bash
docker build -t family-timer .
docker run --rm -p 8080:80 family-timer
```

Después, visita [http://localhost:8080](http://localhost:8080).

## Personalizar el calendario

Edita [`data/calendars.json`](data/calendars.json) para cambiar:

- `dayStart` y `dayEnd`: horas visibles.
- `slotMinutes`: duración del bloque de referencia.
- `calendars`: nombres, colores y descripciones.
- `days`: tareas agrupadas por fecha (`YYYY-MM-DD`), con hora de inicio y fin.

Al modificar el JSON con el contenedor en ejecución, reconstruye la imagen para aplicar los cambios:

```bash
docker compose up --build
```

## Ejecución local sin Docker

Como la aplicación usa `fetch` para cargar el JSON, debe servirse mediante HTTP. Por ejemplo, con Python:

```bash
python3 -m http.server 8000
```

Visita [http://localhost:8000/family_timer.html](http://localhost:8000/family_timer.html).