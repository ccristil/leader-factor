"""LeaderFactor manager dashboard — Flask app.

Routes:
    GET /                          -> dashboard
    GET /dashboard[?manager_id=N]  -> the manager's engagement dashboard
    GET /manager/<id>/email        -> the weekly Monday email (rendered preview)

`resolve_current_manager` is the auth seam: it reads `session` first and falls
back to the query-param switcher / a default. A real login later just needs to
set `session["manager_id"]`; nothing downstream changes.
"""

import os

from dotenv import load_dotenv
from flask import Flask, abort, g, redirect, render_template, request, session, url_for

import links
import metrics
from models import get_session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-for-prod")

# Link/identity helpers are used directly in templates (dashboard + email share them).
app.jinja_env.globals["schedule_1on1_url"] = links.schedule_1on1_url


@app.template_filter("pct")
def pct(ratio):
    """0.309 -> '31%'."""
    return f"{round((ratio or 0) * 100)}%"


def db():
    """One SQLAlchemy session per request, closed on teardown."""
    if "db" not in g:
        g.db = get_session()
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    s = g.pop("db", None)
    if s is not None:
        s.close()


def resolve_current_manager():
    """Return (manager_id, managers). The seam a real login would plug into.

    Precedence: an explicit ?manager_id= switch (remembered in session) >
    whatever's already in session > the first manager as a default.
    """
    managers = metrics.list_managers(db())
    valid_ids = {m["id"] for m in managers}

    switched = request.args.get("manager_id", type=int)
    if switched in valid_ids:
        session["manager_id"] = switched

    manager_id = session.get("manager_id")
    if manager_id not in valid_ids:
        session.pop("manager_id", None)
        manager_id = managers[0]["id"] if managers else None

    return manager_id, managers


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    manager_id, managers = resolve_current_manager()
    data = metrics.dashboard_data(db(), manager_id) if manager_id else None
    if data is None:
        abort(404, "No manager data found — is the database seeded?")
    return render_template(
        "dashboard.html", data=data, managers=managers, current_id=manager_id
    )


@app.route("/manager/<int:manager_id>/email")
def email(manager_id):
    data = metrics.dashboard_data(db(), manager_id)
    if data is None:
        abort(404)
    return render_template("email.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
