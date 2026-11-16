"""Database-backed users, revocable sessions and login throttling."""

import hashlib
import re
import secrets
from pathlib import Path

from werkzeug.security import generate_password_hash

from routes.checklist_routes import db_cursor


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def normalize_username(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{3,64}", value):
        raise ValueError(
            "Benutzername: 3–64 Zeichen (Buchstaben, Zahlen, _, . oder -)."
        )
    return value.lower()


def init_schema():
    with db_cursor(commit=True) as cur:
        cur.execute(Path(__file__).with_name("schema.sql").read_text())


def create_user(username, password):
    username = normalize_username(username)
    if not isinstance(password, str) or not 15 <= len(password) <= 128:
        raise ValueError("Das Passwort muss 15–128 Zeichen lang sein.")
    with db_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO app_users (username, password_hash) VALUES (%s, %s)",
            (username, generate_password_hash(password)),
        )


def reset_password(username, password):
    username = normalize_username(username)
    if not 15 <= len(password) <= 128:
        raise ValueError("Das Passwort muss 15–128 Zeichen lang sein.")
    with db_cursor(commit=True) as cur:
        cur.execute(
            "UPDATE app_users SET password_hash = %s WHERE username = %s RETURNING id",
            (generate_password_hash(password), username),
        )
        user = cur.fetchone()
        if not user:
            raise ValueError("Benutzer nicht gefunden.")
        cur.execute("DELETE FROM app_sessions WHERE user_id = %s", (user["id"],))


def get_user(username):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM app_users WHERE username = %s", (username,))
        return cur.fetchone()


def consume_attempt(username, address):
    # Atomic shared counters: effective across workers, no trusted proxy headers.
    allowed = True
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM auth_attempts WHERE expires_at < NOW()")
        for key, limit in [("user:" + username, 10), ("ip:" + address, 50)]:
            cur.execute(
                "INSERT INTO auth_attempts (bucket, attempts, expires_at) "
                "VALUES (%s, 1, NOW() + INTERVAL '15 minutes') "
                "ON CONFLICT (bucket) DO UPDATE SET attempts = auth_attempts.attempts + 1 "
                "RETURNING attempts",
                (digest(key),),
            )
            allowed = cur.fetchone()["attempts"] <= limit and allowed
    return allowed


def issue_session(user_id):
    token = secrets.token_urlsafe(32)
    csrf = secrets.token_urlsafe(32)
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM app_sessions WHERE expires_at < NOW()")
        cur.execute(
            "INSERT INTO app_sessions (token_hash, user_id, csrf_token, expires_at) "
            "VALUES (%s, %s, %s, NOW() + INTERVAL '8 hours')",
            (digest(token), user_id, csrf),
        )
    return token, csrf


def lookup_session(token):
    if not token or len(token) > 128:
        return None
    with db_cursor() as cur:
        cur.execute(
            "SELECT u.id, u.username, s.csrf_token FROM app_sessions s "
            "JOIN app_users u ON u.id = s.user_id "
            "WHERE s.token_hash = %s AND s.expires_at > NOW() AND u.active",
            (digest(token),),
        )
        return cur.fetchone()


def revoke_session(token):
    if token:
        with db_cursor(commit=True) as cur:
            cur.execute(
                "DELETE FROM app_sessions WHERE token_hash = %s", (digest(token),)
            )
