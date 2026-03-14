from sqlalchemy.orm import Session as SASession
from app.models import AuditLog


def insert_audit_log(db_engine, asset_id=1, event_type="asset.created"):
    with SASession(db_engine) as session:
        log = AuditLog(asset_id=asset_id, event_type=event_type, payload={})
        session.add(log)
        session.commit()


def test_get_all_logs(client, auth_headers, db_engine):
    insert_audit_log(db_engine)
    response = client.get(
        "/audit",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_log(client, auth_headers, db_engine):
    insert_audit_log(db_engine)
    response = client.get(
        "/audit/1",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["asset_id"] == 1
    assert data[0]["event_type"] == "asset.created"


def test_get_log_unauthorized(client):
    response = client.get("/audit/1")
    assert response.status_code == 401
