"""Exercise authentication against the same PostgreSQL database as CI."""

from uuid import uuid4

from auth import store


def test_auth_lifecycle(app):
    store.init_schema()
    store.init_schema()  # Migration is safe to rerun against existing data.
    username = "test_" + uuid4().hex
    password = "test password " + uuid4().hex
    store.create_user(username, password)
    headers = {"X-Paperless-Login": "1"}
    try:
        with app.test_client() as client:
            assert client.get("/api/checklists").status_code == 401
            response = client.post(
                "/api/auth/login",
                json={"username": username, "password": password},
                headers=headers,
            )
            assert response.status_code == 200
            csrf = response.json["csrf_token"]
            token = client.get_cookie("paperless_session").value
            assert client.get("/api/checklists").status_code == 200
            assert (
                client.post("/api/checklists", json={"title": "Denied"}).status_code
                == 403
            )
            assert (
                client.post(
                    "/api/auth/logout", headers={"X-CSRF-Token": csrf}
                ).status_code
                == 200
            )
            client.set_cookie("paperless_session", token)
            assert client.get("/api/checklists").status_code == 401
            response = client.post(
                "/api/auth/login",
                json={"username": username, "password": password},
                headers=headers,
            )
            assert response.status_code == 200
            store.reset_password(username, password + "!")
            assert client.get("/api/checklists").status_code == 401
            response = client.post(
                "/api/auth/login",
                json={"username": username, "password": password + "!"},
                headers=headers,
            )
            assert response.status_code == 200
            with store.db_cursor(commit=True) as cur:
                cur.execute(
                    "UPDATE app_sessions SET expires_at = NOW() - INTERVAL '1 second' WHERE token_hash = %s",
                    (store.digest(client.get_cookie("paperless_session").value),),
                )
            assert client.get("/api/checklists").status_code == 401
            for _ in range(7):
                client.post(
                    "/api/auth/login",
                    json={"username": username, "password": "incorrect"},
                    headers=headers,
                )
            assert (
                client.post(
                    "/api/auth/login",
                    json={"username": username, "password": password + "!"},
                    headers=headers,
                ).status_code
                == 429
            )
    finally:
        with store.db_cursor(commit=True) as cur:
            cur.execute("DELETE FROM app_users WHERE username = %s", (username,))
            cur.execute(
                "DELETE FROM auth_attempts WHERE bucket = ANY(%s)",
                ([store.digest("user:" + username), store.digest("ip:127.0.0.1")],),
            )
