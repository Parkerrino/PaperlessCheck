from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "body",
    [
        pytest.param(
            '{"description": "Missing title"}',
            id="missing-title",
        ),
        pytest.param(
            '{"title": ""}',
            id="empty-title",
        ),
        pytest.param(
            '{"title": "   "}',
            id="whitespace-title",
        ),
        pytest.param(
            '{"title": 123}',
            id="numeric-title",
        ),
        pytest.param(
            '[{"title": "Unexpected array"}]',
            id="array-instead-of-object",
        ),
        pytest.param(
            '{"title":',
            id="malformed-json",
        ),
    ],
)
def test_reject_invalid_checklist_creation(client, body):
    """Reject invalid input before accessing the database."""
    with patch(
        "routes.checklist_routes.get_db_connection",
        side_effect=AssertionError("Invalid input must not access the database"),
    ) as mock_connection:
        response = client.post(
            "/api/checklists",
            data=body,
            content_type="application/json",
        )

        mock_connection.assert_not_called()

    assert response.status_code == 400, response.get_data(as_text=True)
    assert response.is_json

    payload = response.get_json()
    assert isinstance(payload, dict)
    assert payload.get("errors") or payload.get("error"), payload
