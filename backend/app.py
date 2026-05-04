from flask import Flask, jsonify
from flask_cors import CORS
from routes.checklist_routes import checklist_bp
import os

app = Flask(__name__)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(checklist_bp, url_prefix="/api/checklists")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Docker."""
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv('FLASK_ENV') == 'development')