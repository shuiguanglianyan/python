import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_cmdb.db"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def teardown_module():
    test_db = Path("test_cmdb.db")
    if test_db.exists():
        test_db.unlink()


def login_as_admin(test_client: TestClient):
    resp = test_client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )
    assert resp.status_code == 303


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_root_requires_login():
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/login"


def test_asset_service_change_flow():
    login_as_admin(client)

    create_asset = client.post(
        "/assets",
        data={"hostname": "node-01", "ip": "10.0.0.11", "environment": "prod", "os": "linux", "owner": "ops"},
        follow_redirects=False,
    )
    assert create_asset.status_code == 303

    assets = client.get("/api/assets")
    assert assets.status_code == 200
    data = assets.json()
    assert any(a["hostname"] == "node-01" for a in data)

    asset_id = data[0]["id"]
    create_service = client.post(
        "/services",
        data={"name": "billing-api", "asset_id": asset_id, "repo_url": "https://github.com/example/billing"},
        follow_redirects=False,
    )
    assert create_service.status_code == 303

    create_change = client.post(
        "/changes",
        data={"title": "deploy billing v1.0.1", "service_id": 1, "risk_level": "low", "executor": "alice"},
        follow_redirects=False,
    )
    assert create_change.status_code == 303


def test_login_redirect_respects_root_path():
    prefixed_client = TestClient(app, root_path="/cmdb")
    resp = prefixed_client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )

    assert resp.status_code == 303
    assert resp.headers["location"].endswith("/cmdb/")
