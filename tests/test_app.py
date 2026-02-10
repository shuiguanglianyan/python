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


def test_api_requires_login():
    unauth_client = TestClient(app)
    resp = unauth_client.get("/api/assets")
    assert resp.status_code == 401


def test_asset_service_change_flow_and_api_updates():
    login_as_admin(client)

    create_asset = client.post(
        "/assets",
        data={"hostname": "node-01", "ip": "10.0.0.11", "environment": "prod", "os": "linux", "owner": "ops"},
        follow_redirects=False,
    )
    assert create_asset.status_code == 303

    assets_resp = client.get("/api/assets")
    assert assets_resp.status_code == 200
    assets = assets_resp.json()
    assert any(a["hostname"] == "node-01" for a in assets)

    asset_id = assets[0]["id"]
    create_service = client.post(
        "/services",
        data={"name": "billing-api", "asset_id": asset_id, "repo_url": "https://github.com/example/billing"},
        follow_redirects=False,
    )
    assert create_service.status_code == 303

    services_resp = client.get("/api/services")
    service_id = services_resp.json()[0]["id"]

    create_change = client.post(
        "/changes",
        data={"title": "deploy billing v1.0.1", "service_id": service_id, "risk_level": "low", "executor": "alice"},
        follow_redirects=False,
    )
    assert create_change.status_code == 303

    update_asset = client.put(f"/api/assets/{asset_id}", json={"owner": "platform"})
    assert update_asset.status_code == 200
    assert update_asset.json()["owner"] == "platform"

    change_id = client.get("/api/changes").json()[0]["id"]
    update_change = client.put(f"/api/changes/{change_id}", json={"status": "approved"})
    assert update_change.status_code == 200
    assert update_change.json()["status"] == "approved"

    overview = client.get("/api/overview")
    assert overview.status_code == 200
    data = overview.json()
    assert data["asset_count"] >= 1
    assert data["service_count"] >= 1
    assert data["change_count"] >= 1


def test_login_redirect_respects_root_path():
    prefixed_client = TestClient(app, root_path="/cmdb")
    resp = prefixed_client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )

    assert resp.status_code == 303
    assert resp.headers["location"].endswith("/cmdb/")
