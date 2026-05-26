import os
import secrets
from functools import wraps

from authlib.integrations.flask_client import OAuth
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import database
import seed

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# SECRET_KEY signs session cookies. Set it in Railway as a long random string.
# Falling back to a random per-process value keeps local dev functional, but
# means sessions don't survive a restart (acceptable for local).
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
# Comma-separated list, e.g. "valeria.araya.valdes@gmail.com"
ALLOWED_EMAILS = {
    e.strip().lower()
    for e in os.environ.get("ALLOWED_EMAILS", "").split(",")
    if e.strip()
}

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def current_user():
    return session.get("user")


def is_authorized(user):
    if not user:
        return False
    email = (user.get("email") or "").lower()
    return bool(email) and email in ALLOWED_EMAILS


def require_auth(view):
    """Gate a view behind Google login + allow-list check."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not is_authorized(user):
            # API calls get a JSON 401 so the frontend can react; HTML gets a redirect.
            if request.path.startswith("/api/"):
                return jsonify({"error": "unauthorized"}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------
@app.route("/login")
def login():
    user = current_user()
    if is_authorized(user):
        return redirect(url_for("index"))
    error = request.args.get("error")
    return render_template("login.html", error=error)


@app.route("/auth/start")
def auth_start():
    redirect_uri = url_for("auth_callback", _external=True, _scheme="https")
    # When developing locally over http, fall back to the request scheme.
    if request.host.startswith("localhost") or request.host.startswith("127.0.0.1"):
        redirect_uri = url_for("auth_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth/callback")
def auth_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        return redirect(url_for("login", error="auth_failed"))

    userinfo = token.get("userinfo") or {}
    email = (userinfo.get("email") or "").lower()
    if not email or email not in ALLOWED_EMAILS:
        session.clear()
        return redirect(url_for("login", error="not_allowed"))

    session["user"] = {
        "email": email,
        "name": userinfo.get("name", ""),
        "picture": userinfo.get("picture", ""),
    }
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/api/me")
@require_auth
def api_me():
    return jsonify(current_user())


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# App routes (all gated by require_auth)
# ---------------------------------------------------------------------------
@app.route("/")
@require_auth
def index():
    return render_template("index.html", user=current_user())


@app.get("/api/tasks")
@require_auth
def api_list():
    return jsonify(database.list_tasks())


@app.post("/api/tasks")
@require_auth
def api_create():
    cleaned, err = validate_payload(request.get_json(silent=True) or {}, partial=False)
    if err:
        return jsonify({"error": err}), 400
    task = database.create_task(cleaned)
    return jsonify(task), 201


@app.patch("/api/tasks/<int:task_id>")
@require_auth
def api_update(task_id):
    cleaned, err = validate_payload(request.get_json(silent=True) or {}, partial=True)
    if err:
        return jsonify({"error": err}), 400
    task = database.update_task(task_id, cleaned)
    if task is None:
        abort(404)
    return jsonify(task)


@app.delete("/api/tasks/completed")
@require_auth
def api_delete_completed():
    """Remove every task whose status is 'hecho'."""
    n = database.delete_completed()
    return jsonify({"deleted": n})


@app.delete("/api/tasks/<int:task_id>")
@require_auth
def api_delete(task_id):
    if not database.delete_task(task_id):
        abort(404)
    return ("", 204)


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "not found"}), 404
    return ("Not found", 404)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
def bootstrap():
    database.init_db()
    seeded = seed.seed_if_empty()
    if seeded:
        print(f"[seed] Imported {seeded} legacy tasks into the database")
    if not ALLOWED_EMAILS:
        print("[auth] WARNING: ALLOWED_EMAILS is empty — nobody will be able to log in")
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        print("[auth] WARNING: GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET not set")


bootstrap()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
