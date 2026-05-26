import os

from flask import Flask, jsonify, render_template, request, abort

import database
import seed

app = Flask(__name__)

VALID_CATEGORIES = {"personal", "domestico", "laboral", "otro"}
VALID_PRIORITIES = {"altisima", "alta", "media", "baja"}
VALID_STATUSES = {"pendiente", "critico", "hoy", "progreso", "hecho"}


def validate_payload(data, partial=False):
    """Returns (cleaned_dict, error_msg). Validates types and allowed values."""
    if not isinstance(data, dict):
        return None, "JSON object expected"

    cleaned = {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return None, "title is required"
        cleaned["title"] = title
    elif not partial:
        return None, "title is required"

    if "category" in data:
        if data["category"] not in VALID_CATEGORIES:
            return None, f"category must be one of {sorted(VALID_CATEGORIES)}"
        cleaned["category"] = data["category"]
    elif not partial:
        cleaned["category"] = "personal"

    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return None, f"priority must be one of {sorted(VALID_PRIORITIES)}"
        cleaned["priority"] = data["priority"]
    elif not partial:
        cleaned["priority"] = "media"

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return None, f"status must be one of {sorted(VALID_STATUSES)}"
        cleaned["status"] = data["status"]
    elif not partial:
        cleaned["status"] = "pendiente"

    if "due" in data:
        cleaned["due"] = data.get("due") or ""
    elif not partial:
        cleaned["due"] = ""

    if "notes" in data:
        cleaned["notes"] = data.get("notes") or ""
    elif not partial:
        cleaned["notes"] = ""

    return cleaned, None


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/tasks")
def api_list():
    return jsonify(database.list_tasks())


@app.post("/api/tasks")
def api_create():
    cleaned, err = validate_payload(request.get_json(silent=True) or {}, partial=False)
    if err:
        return jsonify({"error": err}), 400
    task = database.create_task(cleaned)
    return jsonify(task), 201


@app.patch("/api/tasks/<int:task_id>")
def api_update(task_id):
    cleaned, err = validate_payload(request.get_json(silent=True) or {}, partial=True)
    if err:
        return jsonify({"error": err}), 400
    task = database.update_task(task_id, cleaned)
    if task is None:
        abort(404)
    return jsonify(task)


@app.delete("/api/tasks/completed")
def api_delete_completed():
    """Remove every task whose status is 'hecho'."""
    n = database.delete_completed()
    return jsonify({"deleted": n})


@app.delete("/api/tasks/<int:task_id>")
def api_delete(task_id):
    if not database.delete_task(task_id):
        abort(404)
    return ("", 204)


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "not found"}), 404
    return ("Not found", 404)


def bootstrap():
    database.init_db()
    seeded = seed.seed_if_empty()
    if seeded:
        print(f"[seed] Imported {seeded} legacy tasks into todo.db")


bootstrap()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
