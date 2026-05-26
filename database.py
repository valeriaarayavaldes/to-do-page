import os
from datetime import date

import psycopg
from psycopg.rows import dict_row


def _get_database_url():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required. "
            "Set it to a PostgreSQL connection string, e.g. "
            "postgresql://user:pass@host:5432/dbname"
        )
    # Railway exposes the URL as postgres://..., psycopg expects postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       TEXT    NOT NULL,
    category    TEXT    NOT NULL CHECK (category IN ('personal','domestico','laboral','otro')),
    priority    TEXT    NOT NULL CHECK (priority IN ('altisima','alta','media','baja')),
    status      TEXT    NOT NULL CHECK (status   IN ('pendiente','critico','hoy','progreso','hecho')),
    due         TEXT    NOT NULL DEFAULT '',
    notes       TEXT    NOT NULL DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT ''
);
"""


def get_connection():
    return psycopg.connect(_get_database_url(), row_factory=dict_row)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA)


def is_empty():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM tasks")
            row = cur.fetchone()
            return row["n"] == 0


def task_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "category": row["category"],
        "priority": row["priority"],
        "status": row["status"],
        "due": row["due"],
        "notes": row["notes"],
        "created_at": row["created_at"],
    }


def list_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY id")
            return [task_to_dict(r) for r in cur.fetchall()]


def get_task(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            return task_to_dict(row) if row else None


def create_task(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO tasks (title, category, priority, status, due, notes, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (
                    data["title"],
                    data["category"],
                    data["priority"],
                    data["status"],
                    data.get("due", ""),
                    data.get("notes", ""),
                    date.today().isoformat(),
                ),
            )
            new_id = cur.fetchone()["id"]
    return get_task(new_id)


# created_at is intentionally NOT in this set — it's not user-editable.
ALLOWED_FIELDS = {"title", "category", "priority", "status", "due", "notes"}


def update_task(task_id, data):
    fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    if not fields:
        return get_task(task_id)
    set_clause = ", ".join(f"{k} = %s" for k in fields.keys())
    values = list(fields.values()) + [task_id]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE tasks SET {set_clause} WHERE id = %s", values)
            if cur.rowcount == 0:
                return None
    return get_task(task_id)


def delete_task(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            return cur.rowcount > 0


def delete_completed():
    """Remove every task whose status is 'hecho'. Returns number of rows deleted."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE status = 'hecho'")
            return cur.rowcount


def insert_with_id(task):
    """Used by the seeder to preserve original IDs from the legacy HTML array."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO tasks (id, title, category, priority, status, due, notes, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    task["id"],
                    task["title"],
                    task["category"],
                    task["priority"],
                    task["status"],
                    task.get("due", ""),
                    task.get("notes", ""),
                    task.get("created_at", date.today().isoformat()),
                ),
            )


def reset_id_sequence():
    """Advance the tasks.id sequence past the current MAX(id).

    Needed after bulk inserts with explicit IDs (the seeder) so subsequent
    SERIAL inserts don't collide with pre-seeded IDs.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT setval(pg_get_serial_sequence('tasks', 'id'), "
                "COALESCE((SELECT MAX(id) FROM tasks), 1))"
            )
