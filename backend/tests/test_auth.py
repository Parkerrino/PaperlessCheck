from unittest.mock import patch

import pytest
from werkzeug.security import generate_password_hash


@pytest.fixture
def raw_client(app):
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "method,path",
    [
        ("get", "/api/checklists"),
        ("post", "/api/checklists"),
        ("put", "/api/checklists/1"),
        ("delete", "/api/checklists/1"),
        ("post", "/api/checklists/1/items"),
        ("put", "/api/checklists/items/1"),
        ("delete", "/api/checklists/items/1"),
        ("get", "/api/auth/session"),
    ],
)
def test_anonymous_denied(raw_client, method, path):
    with patch("auth.store.lookup_session", return_value=None), patch(
        "routes.checklist_routes.get_db_connection"
    ) as db:
        response = getattr(raw_client, method)(path, json={"title": "Valid"})
        assert response.status_code == 401
        db.assert_not_called()


@pytest.mark.parametrize("token", ["", "wrong", "ü"])
def test_csrf_blocks_writes(raw_client, token):
    with patch(
        "auth.store.lookup_session", return_value={"csrf_token": "right"}
    ), patch("routes.checklist_routes.get_db_connection") as db:
        response = raw_client.post(
            "/api/checklists", json={"title": "Valid"}, headers={"X-CSRF-Token": token}
        )
        assert response.status_code == 403
        db.assert_not_called()


def test_login_requires_json_custom_header(raw_client):
    assert raw_client.post("/api/auth/login", json={}).status_code == 400


def test_login_cookie_and_logout(raw_client):
    user = {
        "id": 1,
        "username": "admin",
        "active": True,
        "password_hash": generate_password_hash("a long test password"),
    }
    with patch("auth.store.consume_attempt", return_value=True), patch(
        "auth.store.get_user", return_value=user
    ), patch("auth.store.issue_session", return_value=("random-token", "csrf")), patch(
        "auth.store.revoke_session"
    ) as revoke:
        response = raw_client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "a long test password"},
            headers={"X-Paperless-Login": "1"},
        )
        assert response.status_code == 200
        cookie = response.headers["Set-Cookie"]
        assert all(flag in cookie for flag in ["HttpOnly", "Secure", "SameSite=Strict"])
        assert response.headers["Cache-Control"] == "no-store"
        with patch(
            "auth.store.lookup_session",
            return_value={"username": "admin", "csrf_token": "csrf"},
        ):
            response = raw_client.post(
                "/api/auth/logout", headers={"X-CSRF-Token": "csrf"}
            )
            assert response.status_code == 200
            revoke.assert_called_with("random-token")


@pytest.mark.parametrize(
    "user",
    [
        None,
        {"id": 1, "active": False, "password_hash": generate_password_hash("wrong")},
    ],
)
def test_invalid_login_is_generic(raw_client, user):
    with patch("auth.store.consume_attempt", return_value=True), patch(
        "auth.store.get_user", return_value=user
    ), patch("auth.store.issue_session") as issue:
        response = raw_client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "not the password"},
            headers={"X-Paperless-Login": "1"},
        )
        assert response.status_code == 401
        assert response.json["error"] == "Benutzername oder Passwort falsch."
        issue.assert_not_called()


def test_rate_limit(raw_client):
    with patch("auth.store.consume_attempt", return_value=False), patch(
        "auth.store.get_user"
    ) as lookup:
        response = raw_client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "bad"},
            headers={"X-Paperless-Login": "1"},
        )
        assert response.status_code == 429
        lookup.assert_not_called()
