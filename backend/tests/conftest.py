import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def app():
    from backend.app import app as flask_app

    previous_testing = flask_app.config["TESTING"]
    flask_app.config["TESTING"] = True
    yield flask_app
    flask_app.config["TESTING"] = previous_testing


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_db_connection():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = []
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        yield mock_conn
