import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from routes.checklist_routes import checklist_bp

app = Flask(__name__)

# Browser clients use the same-origin /api proxy; no wildcard CORS access.

# Register blueprints
app.register_blueprint(checklist_bp, url_prefix="/api/checklists")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Docker."""
    return jsonify({"status": "healthy"}), 200


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.errorhandler(HTTPException)
def http_error(error):
    """Return JSON while retaining status and protocol headers such as Allow."""
    response = error.get_response()
    messages = {404: "Resource not found", 500: "Internal server error"}
    response.data = app.json.dumps({"error": messages.get(error.code, error.name)})
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "development")
