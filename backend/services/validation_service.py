"""Validation service for checklist operations."""

from typing import Any


def _validate_title(data: dict[str, Any], errors: list[str]) -> None:
    """Append title validation errors."""
    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        errors.append("Title is required and must be a non-empty string")
    elif len(title) > 255:
        errors.append("Title must not exceed 255 characters")


def validate_checklist_data(data: Any) -> list[str]:
    """Validate checklist creation/update data."""
    if not isinstance(data, dict):
        return ["Request body must be a JSON object"]

    errors: list[str] = []
    _validate_title(data, errors)

    if "description" in data and not isinstance(data["description"], str):
        errors.append("Description must be a string")

    return errors


def validate_checklist_item_data(data: Any) -> list[str]:
    """Validate checklist item creation/update data."""
    if not isinstance(data, dict):
        return ["Request body must be a JSON object"]

    errors: list[str] = []
    _validate_title(data, errors)

    if "completed" in data and not isinstance(data["completed"], bool):
        errors.append("Completed must be a boolean")

    if "order_index" in data:
        order_index = data["order_index"]

        if isinstance(order_index, bool) or not isinstance(order_index, int):
            errors.append("Order index must be an integer")
        elif order_index < 0:
            errors.append("Order index must be zero or greater")

    return errors
