from app import app, add


def test_add():
    assert add(2, 3) == 5


def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.get_json()["status"] == "ok"
