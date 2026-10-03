"""Validation service for checklist operations."""

from typing import Any, Dict, List


def _validate_title(data: Dict[str, Any], errors: List[str]) -> None:
    """Append title validation errors to ``errors`` in place."""
    title = data.get("title")

    if not title or not isinstance(title, str):
        errors.append("Title is required and must be a string")
    elif len(title) > 255:
        errors.append("Title must not exceed 255 characters")


def validate_checklist_data(data: Dict[str, Any]) -> List[str]:
    """Validate checklist creation/update data."""
    errors: List[str] = []

    _validate_title(data, errors)

    if data.get("description") and not isinstance(data.get("description"), str):
        errors.append("Description must be a string")

    return errors


def validate_checklist_item_data(data: Dict[str, Any]) -> List[str]:
    """Validate checklist item creation/update data."""
    errors: List[str] = []

    _validate_title(data, errors)

    if "completed" in data and not isinstance(data.get("completed"), bool):
        errors.append("Completed must be a boolean")

    if "order_index" in data and not isinstance(data.get("order_index"), int):
        errors.append("Order index must be an integer")

    return errors
