"""Routes for checklist management API."""

import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg2
from flask import Blueprint, Response, jsonify, request
from psycopg2.extras import RealDictCursor
from services.validation_service import (
    validate_checklist_data,
    validate_checklist_item_data,
)

logger = logging.getLogger(__name__)

checklist_bp = Blueprint("checklists", __name__)


class DatabaseError(Exception):
    """Raised when a database connection or query fails."""


def _server_error() -> tuple[Response, int]:
    """Return a generic 500 response without leaking internal details."""
    return jsonify({"error": "Internal server error"}), 500


def _json_body() -> dict:
    """Return the request JSON body, or an empty dict if absent/invalid."""
    return request.get_json(silent=True) or {}


def get_db_connection():
    """Establish database connection."""
    try:
        return psycopg2.connect(os.getenv("DATABASE_URL"))
    except Exception as e:
        logger.exception("Database connection failed")
        raise DatabaseError("Database connection error") from e


@contextmanager
def db_cursor(commit: bool = False) -> Iterator[Any]:
    """Yield a cursor and always close the cursor and connection.

    Commits when ``commit`` is True and the block succeeds; rolls back on any
    exception. The connection and cursor are closed in a ``finally`` block so
    they are never leaked, even when an error is raised mid-handler.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


@checklist_bp.route("/health", methods=["GET"])
def health() -> tuple[Response, int]:
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        logger.exception("Health check failed")
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500


@checklist_bp.route("", methods=["GET"])
def get_checklists() -> tuple[Response, int]:
    """Get all checklists with their items (single grouped query)."""
    try:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM checklists ORDER BY created_at DESC")
            checklists = cur.fetchall()

            checklist_ids = [checklist["id"] for checklist in checklists]
            items_by_checklist: dict = {cid: [] for cid in checklist_ids}
            if checklist_ids:
                cur.execute(
                    "SELECT * FROM checklist_items WHERE checklist_id = ANY(%s) "
                    "ORDER BY order_index",
                    (checklist_ids,),
                )
                for item in cur.fetchall():
                    items_by_checklist[item["checklist_id"]].append(item)

            for checklist in checklists:
                checklist["items"] = items_by_checklist[checklist["id"]]

        return jsonify(checklists), 200
    except Exception:
        logger.exception("Failed to list checklists")
        return _server_error()


@checklist_bp.route("/<int:checklist_id>", methods=["GET"])
def get_checklist(checklist_id: int) -> tuple[Response, int]:
    """Get a specific checklist with items."""
    try:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM checklists WHERE id = %s", (checklist_id,))
            checklist = cur.fetchone()

            if not checklist:
                return jsonify({"error": "Checklist not found"}), 404

            cur.execute(
                "SELECT * FROM checklist_items WHERE checklist_id = %s "
                "ORDER BY order_index",
                (checklist_id,),
            )
            checklist["items"] = cur.fetchall()

        return jsonify(checklist), 200
    except Exception:
        logger.exception("Failed to fetch checklist %s", checklist_id)
        return _server_error()


@checklist_bp.route("", methods=["POST"])
def create_checklist() -> tuple[Response, int]:
    """Create a new checklist."""
    try:
        data = _json_body()

        errors = validate_checklist_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        with db_cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO checklists (title, description) VALUES (%s, %s) "
                "RETURNING *",
                (data["title"], data.get("description", "")),
            )
            checklist = cur.fetchone()

        return jsonify(checklist), 201
    except Exception:
        logger.exception("Failed to create checklist")
        return _server_error()


@checklist_bp.route("/<int:checklist_id>", methods=["PUT"])
def update_checklist(checklist_id: int) -> tuple[Response, int]:
    """Update a checklist."""
    try:
        data = _json_body()

        errors = validate_checklist_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        with db_cursor(commit=True) as cur:
            cur.execute(
                "UPDATE checklists SET title = %s, description = %s, "
                "updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
                (data["title"], data.get("description", ""), checklist_id),
            )
            checklist = cur.fetchone()

            if not checklist:
                return jsonify({"error": "Checklist not found"}), 404

        return jsonify(checklist), 200
    except Exception:
        logger.exception("Failed to update checklist %s", checklist_id)
        return _server_error()


@checklist_bp.route("/<int:checklist_id>", methods=["DELETE"])
def delete_checklist(checklist_id: int) -> tuple[Response, int]:
    """Delete a checklist."""
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("DELETE FROM checklists WHERE id = %s", (checklist_id,))

            if cur.rowcount == 0:
                return jsonify({"error": "Checklist not found"}), 404

        return jsonify({"message": "Checklist deleted successfully"}), 200
    except Exception:
        logger.exception("Failed to delete checklist %s", checklist_id)
        return _server_error()


@checklist_bp.route("/<int:checklist_id>/items", methods=["POST"])
def add_item(checklist_id: int) -> tuple[Response, int]:
    """Add an item to a checklist."""
    try:
        data = _json_body()

        errors = validate_checklist_item_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        with db_cursor(commit=True) as cur:
            cur.execute("SELECT id FROM checklists WHERE id = %s", (checklist_id,))
            if not cur.fetchone():
                return jsonify({"error": "Checklist not found"}), 404

            cur.execute(
                "INSERT INTO checklist_items (checklist_id, title, order_index) "
                "VALUES (%s, %s, %s) RETURNING *",
                (checklist_id, data["title"], data.get("order_index", 0)),
            )
            item = cur.fetchone()

        return jsonify(item), 201
    except Exception:
        logger.exception("Failed to add item to checklist %s", checklist_id)
        return _server_error()


@checklist_bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id: int) -> tuple[Response, int]:
    """Update a checklist item."""
    try:
        data = _json_body()

        errors = validate_checklist_item_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        with db_cursor(commit=True) as cur:
            cur.execute(
                "UPDATE checklist_items SET title = %s, completed = %s, "
                "order_index = %s, updated_at = CURRENT_TIMESTAMP "
                "WHERE id = %s RETURNING *",
                (
                    data.get("title"),
                    data.get("completed", False),
                    data.get("order_index", 0),
                    item_id,
                ),
            )
            item = cur.fetchone()

            if not item:
                return jsonify({"error": "Item not found"}), 404

        return jsonify(item), 200
    except Exception:
        logger.exception("Failed to update item %s", item_id)
        return _server_error()


@checklist_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id: int) -> tuple[Response, int]:
    """Delete a checklist item."""
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("DELETE FROM checklist_items WHERE id = %s", (item_id,))

            if cur.rowcount == 0:
                return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception:
        logger.exception("Failed to delete item %s", item_id)
        return _server_error()
