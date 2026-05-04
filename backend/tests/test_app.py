import pytest
import os
from unittest.mock import patch
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client, mock_db_connection):
    """Test app health (proxied to routes)."""
    with patch('backend.routes.checklist_routes.get_db_connection') as mock_conn:
        mock_conn.return_value = mock_db_connection
        rv = client.get('/health')
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['status'] == 'healthy'

def test_404_handler(client):
    rv = client.get('/nonexistent')
    assert rv.status_code == 404
    assert 'Resource not found' in rv.get_data(as_text=True)

def test_get_checklists(client, mock_db_connection):
    """Test checklists endpoint w/ mock DB."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [{'id': 1, 'title': 'Test', 'items': []}]
    mock_cursor.fetchone.return_value = {'id': 1, 'title': 'Test'}
    
    rv = client.get('/api/checklists')
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data) > 0
    assert data[0]['id'] == 1
