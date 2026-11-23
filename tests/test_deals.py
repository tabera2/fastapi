import os
os.environ.update(database_hostname="localhost", database_port="5432", database_password="test", database_name="test", database_username="test", secret_key="test-secret", algorithm="HS256", access_token_expire_minutes="30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models, oauth2
from app.database import get_db
from app.main import app


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def sqlite_now(connection, record):
        connection.create_function("now", 0, lambda: "2026-01-01 00:00:00")
    models.User.__table__.create(engine)
    models.Deal.__table__.create(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all([models.User(id=1, email="one@example.com", password="unused"), models.User(id=2, email="two@example.com", password="unused")])
    db.commit()
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[oauth2.get_current_user] = lambda: db.get(models.User, 1)
    with TestClient(app) as client:
        yield client, db
    app.dependency_overrides.clear()
    db.close()
    engine.dispose()


def test_deal_lifecycle_and_isolation(client):
    api, db = client
    payload = {"brand": " Example Brand ", "creator": "Alex", "deliverables": "One video", "amount_cents": 250000}
    result = api.post("/deals/", json=payload)
    assert result.status_code == 201
    deal = result.json()
    assert deal["brand"] == "Example Brand" and deal["stage"] == "pitch"
    deal_id = deal["id"]
    assert api.patch(f"/deals/{deal_id}", json={"stage": "content_review"}).json()["stage"] == "content_review"
    assert len(api.get("/deals/", params={"stage": "content_review"}).json()) == 1
    assert api.get("/deals/", params={"stage": "paid"}).json() == []
    app.dependency_overrides[oauth2.get_current_user] = lambda: db.get(models.User, 2)
    assert api.get("/deals/").json() == []
    for method in ("get", "patch", "delete"):
        kwargs = {"json": {"stage": "paid"}} if method == "patch" else {}
        assert getattr(api, method)(f"/deals/{deal_id}", **kwargs).status_code == 404
    app.dependency_overrides[oauth2.get_current_user] = lambda: db.get(models.User, 1)
    assert api.delete(f"/deals/{deal_id}").status_code == 204
    assert api.get(f"/deals/{deal_id}").status_code == 404


def test_validation_and_authentication(client):
    api, _ = client
    payload = {"brand": "Brand", "creator": "Alex", "deliverables": "One video", "amount_cents": 100}
    for change in ({"brand": "  "}, {"amount_cents": -1}, {"amount_cents": 1.5}, {"stage": "unknown"}):
        assert api.post("/deals/", json={**payload, **change}).status_code == 422
    deal_id = api.post("/deals/", json=payload).json()["id"]
    assert api.patch(f"/deals/{deal_id}", json={"stage": None}).status_code == 422
    del app.dependency_overrides[oauth2.get_current_user]
    assert api.get("/deals/").status_code == 401
