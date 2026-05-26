# Mi TODO — App web

Backend Flask + PostgreSQL, frontend separado. Diseño del `todo.html` original con persistencia real, lista para desplegar en Railway.

## Arrancar (modo Docker, recomendado)

Levanta Postgres + la app:

```bash
docker compose up --build
```

Abrir [http://localhost:5000](http://localhost:5000).

La primera vez se importan automáticamente las ~130 tareas del HTML original.

## Arrancar (Python local)

Necesitas un Postgres corriendo. Lo más fácil es levantarlo con Docker:

```bash
docker compose up -d db
```

Luego:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://todo:todo@localhost:5432/todo"
python app.py
```

Abrir [http://127.0.0.1:5000](http://127.0.0.1:5000).

> **Importante en macOS:** usa `http://127.0.0.1:5000`, no `http://localhost:5000`. macOS tiene *AirPlay Receiver* escuchando en `*:5000` y resuelve `localhost` por IPv6, devolviendo 403. Alternativa: desactivar *AirPlay Receiver* en *Configuración del Sistema → General → AirDrop y Handoff*.

## Despliegue en Railway

1. Crear proyecto en Railway y conectar este repo (`valeriaarayavaldes/to-do-page`).
2. Añadir un servicio **PostgreSQL** desde el catálogo de Railway (genera la variable `DATABASE_URL` automáticamente).
3. En el servicio de la app, asegurar que `DATABASE_URL` esté seteada (Railway la inyecta si referencias la del servicio Postgres con `${{Postgres.DATABASE_URL}}`).
4. Railway detecta `Dockerfile` y despliega; expone la app en el puerto definido por la variable `PORT`.

## Estructura

```
todo-app/
├── app.py              # Flask + endpoints REST
├── database.py         # esquema y helpers Postgres (psycopg)
├── seed.py             # tareas iniciales del HTML original
├── requirements.txt    # Flask, psycopg, gunicorn
├── Dockerfile
├── docker-compose.yml  # web + db (Postgres 16)
├── Procfile            # gunicorn start command
├── railway.json        # configuración Railway
├── static/
│   ├── app.js          # frontend (consume /api/tasks)
│   └── style.css
└── templates/
    └── index.html
```

## API

| Método | Ruta                       | Descripción                       |
| ------ | -------------------------- | --------------------------------- |
| GET    | `/api/tasks`               | Lista todas las tareas            |
| POST   | `/api/tasks`               | Crea una tarea                    |
| PATCH  | `/api/tasks/<id>`          | Actualiza campos (parcial)        |
| DELETE | `/api/tasks/<id>`          | Elimina la tarea                  |
| DELETE | `/api/tasks/completed`     | Elimina todas con status `hecho`  |

Body de POST/PATCH:

```json
{
  "title": "...",
  "category": "personal | domestico | laboral | otro",
  "priority": "altisima | alta | media | baja",
  "status":   "pendiente | critico | hoy | progreso | hecho",
  "due": "YYYY-MM-DD",
  "notes": "..."
}
```

## Reset de la base

```bash
docker compose down -v   # borra el volumen pgdata
docker compose up --build
```
