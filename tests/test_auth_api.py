import pytest

@pytest.mark.auth
def test_valid_login_returns_token(api_context):
    response = api_context.post(
        "/auth",
        data={"username": "admin", "password": "password123"}
    )
    assert response.status == 200
    body = response.json()
    assert "token" in body
    assert body["token"]

@pytest.mark.auth
@pytest.mark.negative
def test_invalid_login_does_not_return_token(api_context):
    response = api_context.post(
        "/auth",
        data={"username": "wrong_user", "password": "wrong_password"}
    )

    assert response.status in (200, 400, 401)
    body = response.json()
    assert not body.get("token")

@pytest.mark.auth
def test_login_response_is_json(api_context):
    response = api_context.post(
        "/auth",
        data={"username": "admin", "password": "password123"}
    )
    assert "application/json" in response.headers.get("content-type", "")
