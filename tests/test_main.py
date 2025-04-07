from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_valid_approval():
    response = client.post("/validate-approval", json={
        "approver": "svc-release",
        "author": "dev-a",
        "reassigned": False,
        "pipeline_id": "prod-release",
        "commit_id": "abc123"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_self_approval_blocked():
    response = client.post("/validate-approval", json={
        "approver": "dev-a",
        "author": "dev-a",
        "reassigned": False,
        "pipeline_id": "feature-x",
        "commit_id": "def456"
    })
    assert response.status_code == 403
    assert "Self-approval" in response.json()["detail"]

def test_reassignment_blocked():
    response = client.post("/validate-approval", json={
        "approver": "svc-release",
        "author": "dev-b",
        "reassigned": True,
        "pipeline_id": "release-z",
        "commit_id": "ghi789"
    })
    assert response.status_code == 403
    assert "Reassignment" in response.json()["detail"]

def test_unauthorized_approver_blocked():
    response = client.post("/validate-approval", json={
        "approver": "unauthorized-user",
        "author": "dev-c",
        "reassigned": False,
        "pipeline_id": "hotfix-pipeline",
        "commit_id": "jkl012"
    })
    assert response.status_code == 403
    assert "Approver not in allowed list" in response.json()["detail"]
