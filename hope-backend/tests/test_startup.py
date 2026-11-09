from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.db import engine
from app.main import app
from app.services import imap_service


def test_startup_does_not_connect_to_database(monkeypatch):
    monkeypatch.delenv('RENDER', raising=False)
    monkeypatch.delenv('AUTO_MIGRATE', raising=False)
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


def test_render_migrates_runtime_database_before_starting_poller(monkeypatch):
    monkeypatch.setenv('RENDER', 'true')
    events = []
    migrate = Mock(side_effect=lambda db: events.append(('migrate', db)))
    monkeypatch.setattr('app.migrations.upgrade_database', migrate)
    monkeypatch.setattr(imap_service, 'start_poller', lambda: events.append(('poller', None)))
    with TestClient(app) as client:
        assert client.get('/').status_code == 200
    assert events == [('migrate', engine), ('poller', None)]


def test_failed_migration_prevents_serving_requests(monkeypatch):
    monkeypatch.setenv('RENDER', 'true')
    monkeypatch.setattr('app.migrations.upgrade_database', Mock(side_effect=RuntimeError('Migration failed')))
    poller = Mock()
    monkeypatch.setattr(imap_service, 'start_poller', poller)
    with pytest.raises(RuntimeError, match='Migration failed'):
        with TestClient(app):
            pass
    poller.assert_not_called()
