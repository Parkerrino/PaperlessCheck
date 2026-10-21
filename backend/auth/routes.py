"""Cookie authentication and CSRF enforcement. No registration or bypass mode."""

import hmac
import os
import secrets

import click
from auth import store
from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)
COOKIE = "paperless_session"
DUMMY_HASH = generate_password_hash(secrets.token_urlsafe(32))


def protect_request():
    if request.endpoint in {"health", "checklists.health", "auth.login"}:
        return None
    if request.endpoint is None:
        return None  # Flask retains JSON 404/405 handling; no handler executes.
    user = store.lookup_session(request.cookies.get(COOKIE))
    if not user:
        return jsonify(error="Bitte melde dich an."), 401
    g.user = user
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        supplied = request.headers.get("X-CSRF-Token", "")
        if not hmac.compare_digest(supplied.encode(), user["csrf_token"].encode()):
            return jsonify(error="Ungültiger CSRF-Token. Bitte erneut anmelden."), 403
    return None


@bp.post("/login")
def login():
    # JSON plus a custom header prevents cross-site form/login CSRF. No CORS grant.
    if not request.is_json or request.headers.get("X-Paperless-Login") != "1":
        return jsonify(error="JSON-Anmeldung erforderlich."), 400
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Ungültige Anmeldung."), 400
    try:
        username = store.normalize_username(data.get("username"))
    except ValueError:
        return jsonify(error="Benutzername oder Passwort falsch."), 401
    password = data.get("password")
    if not isinstance(password, str) or len(password) > 128:
        return jsonify(error="Benutzername oder Passwort falsch."), 401
    if not store.consume_attempt(username, request.remote_addr or "unknown"):
        return (
            jsonify(error="Zu viele Anmeldeversuche. Bitte später erneut versuchen."),
            429,
        )
    user = store.get_user(username)
    valid = check_password_hash(user["password_hash"] if user else DUMMY_HASH, password)
    if not user or not user["active"] or not valid:
        return jsonify(error="Benutzername oder Passwort falsch."), 401
    store.revoke_session(request.cookies.get(COOKIE))
    token, csrf = store.issue_session(user["id"])
    response = jsonify(user={"username": user["username"]}, csrf_token=csrf)
    response.set_cookie(
        COOKIE,
        token,
        max_age=8 * 60 * 60,
        secure=current_app.config["AUTH_COOKIE_SECURE"],
        httponly=True,
        samesite="Strict",
        path="/",
    )
    return response


@bp.get("/session")
def session_info():
    return jsonify(
        user={"username": g.user["username"]}, csrf_token=g.user["csrf_token"]
    )


@bp.post("/logout")
def logout():
    store.revoke_session(request.cookies.get(COOKIE))
    response = jsonify(message="Abgemeldet.")
    response.delete_cookie(
        COOKIE,
        path="/",
        secure=current_app.config["AUTH_COOKIE_SECURE"],
        httponly=True,
        samesite="Strict",
    )
    return response


def register_auth(app):
    app.config["AUTH_COOKIE_SECURE"] = (
        os.getenv("AUTH_COOKIE_SECURE", "true").lower() != "false"
    )
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
    app.register_blueprint(bp, url_prefix="/api/auth")
    app.before_request(protect_request)

    @app.cli.command("init-auth")
    def init_auth():
        """Add auth tables without modifying existing checklist data."""
        store.init_schema()
        click.echo("Auth-Tabellen bereit.")

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.password_option(confirmation_prompt=True)
    def create_admin(username, password):
        """Create an account with access to the shared workspace."""
        try:
            store.create_user(username, password)
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(
            "Konto angelegt. Alle Konten verwalten den gemeinsamen Arbeitsbereich."
        )

    @app.cli.command("reset-password")
    @click.argument("username")
    @click.password_option(confirmation_prompt=True)
    def reset_password(username, password):
        """Reset password and revoke every existing session for this account."""
        try:
            store.reset_password(username, password)
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo("Passwort geändert; Sitzungen widerrufen.")
