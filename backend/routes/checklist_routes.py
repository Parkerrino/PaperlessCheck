"""Routes for checklist management API."""

from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from services.validation_service import (
    validate_checklist_data,
    validate_checklist_item_data,
)

checklist_bp = Blueprint("checklists", __name__)


def get_db_connection():
    """Establish database connection."""
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")


@checklist_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500


@checklist_bp.route("", methods=["GET"])
def get_checklists():
    """Get all checklists."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM checklists ORDER BY created_at DESC")
        checklists = cur.fetchall()

        # Fetch items for each checklist
        for checklist in checklists:
            cur.execute(
                "SELECT * FROM checklist_items WHERE checklist_id = %s ORDER BY order_index",
                (checklist["id"],),
            )
            checklist["items"] = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(checklists), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/<int:checklist_id>", methods=["GET"])
def get_checklist(checklist_id):
    """Get a specific checklist with items."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM checklists WHERE id = %s", (checklist_id,))
        checklist = cur.fetchone()

        if not checklist:
            cur.close()
            conn.close()
            return jsonify({"error": "Checklist not found"}), 404

        cur.execute(
            "SELECT * FROM checklist_items WHERE checklist_id = %s ORDER BY order_index",
            (checklist_id,),
        )
        checklist["items"] = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(checklist), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("", methods=["POST"])
def create_checklist():
    """Create a new checklist."""
    try:
        data = request.get_json()

        # Validate data
        errors = validate_checklist_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "INSERT INTO checklists (title, description) VALUES (%s, %s) RETURNING *",
            (data["title"], data.get("description", "")),
        )
        checklist = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(checklist), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/<int:checklist_id>", methods=["PUT"])
def update_checklist(checklist_id):
    """Update a checklist."""
    try:
        data = request.get_json()

        # Validate data
        errors = validate_checklist_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "UPDATE checklists SET title = %s, description = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
            (data["title"], data.get("description", ""), checklist_id),
        )
        checklist = cur.fetchone()

        if not checklist:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Checklist not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(checklist), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/<int:checklist_id>", methods=["DELETE"])
def delete_checklist(checklist_id):
    """Delete a checklist."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM checklists WHERE id = %s", (checklist_id,))

        if cur.rowcount == 0:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Checklist not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Checklist deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/<int:checklist_id>/items", methods=["POST"])
def add_item(checklist_id):
    """Add an item to a checklist."""
    try:
        data = request.get_json()

        # Validate data
        errors = validate_checklist_item_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check if checklist exists
        cur.execute("SELECT id FROM checklists WHERE id = %s", (checklist_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Checklist not found"}), 404

        cur.execute(
            "INSERT INTO checklist_items (checklist_id, title, order_index) VALUES (%s, %s, %s) RETURNING *",
            (checklist_id, data["title"], data.get("order_index", 0)),
        )
        item = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(item), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """Update a checklist item."""
    try:
        data = request.get_json()

        # Validate data
        errors = validate_checklist_item_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "UPDATE checklist_items SET title = %s, completed = %s, order_index = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
            (
                data.get("title"),
                data.get("completed", False),
                data.get("order_index", 0),
                item_id,
            ),
        )
        item = cur.fetchone()

        if not item:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Item not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(item), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@checklist_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete a checklist item."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM checklist_items WHERE id = %s", (item_id,))

        if cur.rowcount == 0:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Item not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
