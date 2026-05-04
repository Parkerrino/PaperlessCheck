import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def app():
    from backend.app import app

    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_db_connection():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = []
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        yield mock_conn
