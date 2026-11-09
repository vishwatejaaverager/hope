from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.db import engine
from app.main import app
from app.services import imap_service


def test_startup_does_not_connect_to_database(monkeypatch):
    connect = Mock(side_effect=AssertionError('Startup must not access the database'))
    poller = Mock()
    monkeypatch.setattr(engine, 'connect', connect)
    monkeypatch.setattr(imap_service, 'start_poller', poller)

    with TestClient(app) as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.json() == {'status': 'ok', 'app': 'Hope'}

    connect.assert_not_called()
    poller.assert_called_once()
