def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_success(client, registered_user):
    response = client.post(
        "/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_duplicate_username(client, registered_user):
    response = client.post(
        "/auth/register",
        json={
            "username": registered_user["username"],
            "email": "test1@example.com",
            "password": "password234",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "user already exists"


def test_wrong_password(client, registered_user):
    response = client.post(
        "/auth/login",
        data={
            "username": registered_user["username"],
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_user_does_not_exist(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test1user",
            "password": "password123",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"
