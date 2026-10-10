from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "method,path,field",
    [
        ("post", "/api/checklists", "title"),
        ("post", "/api/checklists", "description"),
        ("put", "/api/checklists/1", "title"),
        ("put", "/api/checklists/1", "description"),
        ("post", "/api/checklists/1/items", "title"),
        ("put", "/api/checklists/items/1", "title"),
    ],
)
def test_null_characters_rejected_before_database(client, method, path, field):
    payload = {"title": "Valid title", field: "invalid\x00text"}
    with patch("routes.checklist_routes.get_db_connection") as connection:
        response = getattr(client, method)(path, json=payload)
        connection.assert_not_called()
    assert response.status_code == 400
    assert response.is_json
    assert response.get_json()["errors"]


@pytest.mark.parametrize(
    "path,status",
    [
        ("/health", 200),
        ("/nonexistent", 404),
        ("/api/checklists/items/1", 405),
    ],
)
def test_json_and_security_headers(client, path, status):
    response = client.get(path, headers={"Origin": "https://untrusted.example"})
    assert response.status_code == status
    assert response.is_json
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Access-Control-Allow-Origin" not in response.headers
    if status == 405:
        assert "PUT" in response.headers["Allow"]
        assert "DELETE" in response.headers["Allow"]


def test_cross_origin_preflight_not_granted(client):
    response = client.options(
        "/api/checklists",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert "Access-Control-Allow-Origin" not in response.headers
