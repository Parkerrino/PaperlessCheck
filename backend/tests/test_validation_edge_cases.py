from unittest.mock import patch

import pytest

from services.validation_service import (
    validate_checklist_data,
    validate_checklist_item_data,
)


@pytest.mark.parametrize(
    "description",
    [0, 123, False, True, [], {}, None],
)
def test_reject_invalid_description(client, description):
    """Reject non-string descriptions before accessing the database."""
    with patch(
        "routes.checklist_routes.get_db_connection",
        side_effect=AssertionError("Invalid input must not access the database"),
    ) as mock_connection:
        response = client.post(
            "/api/checklists",
            json={
                "title": "Valid checklist",
                "description": description,
            },
        )

        mock_connection.assert_not_called()

    assert response.status_code == 400, response.get_data(as_text=True)
    assert response.get_json().get("errors")


@pytest.mark.parametrize(
    "order_index",
    [-1, 1.5, "1", True, False, None, [], {}],
)
def test_reject_invalid_order_index(client, order_index):
    """Reject invalid item positions before accessing the database."""
    with patch(
        "routes.checklist_routes.get_db_connection",
        side_effect=AssertionError("Invalid input must not access the database"),
    ) as mock_connection:
        response = client.post(
            "/api/checklists/1/items",
            json={
                "title": "Valid item",
                "order_index": order_index,
            },
        )

        mock_connection.assert_not_called()

    assert response.status_code == 400, response.get_data(as_text=True)
    assert response.get_json().get("errors")


@pytest.mark.parametrize(
    "optional_fields",
    [{}, {"description": ""}, {"description": "Useful description"}],
)
def test_accept_valid_description(optional_fields):
    data = {"title": "Valid checklist", **optional_fields}

    assert validate_checklist_data(data) == []


@pytest.mark.parametrize(
    "optional_fields",
    [{}, {"order_index": 0}, {"order_index": 1}, {"order_index": 100}],
)
def test_accept_valid_order_index(optional_fields):
    data = {"title": "Valid item", **optional_fields}

    assert validate_checklist_item_data(data) == []
