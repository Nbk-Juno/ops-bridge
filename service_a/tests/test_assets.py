asset_payload = {
    "name": "B-52",
    "asset_type": "equipment",
    "status": "active",
    "location": "Whiteman Air Force Base, MO",
    "asset_metadata": {"meta": "extra information"},
}


def test_create_asset_success(client, auth_headers):
    response = client.post(
        "/assets",
        json=asset_payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "B-52"
    assert data["asset_type"] == "equipment"
    assert data["location"] == "Whiteman Air Force Base, MO"
    assert "id" in data
    assert "owner_id" in data


def test_create_asset_unauthenticated(client):
    response = client.post(
        "/assets",
        json=asset_payload,
    )
    assert response.status_code == 401


def test_list_all_assets(client, auth_headers):
    client.post("/assets", json=asset_payload, headers=auth_headers)
    response = client.get(
        "/assets",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_asset(client, auth_headers):
    created = client.post("/assets", json=asset_payload, headers=auth_headers)
    asset_id = created.json()["id"]

    response = client.get(
        f"/assets/{asset_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == asset_id
    assert data["name"] == asset_payload["name"]


def test_get_asset_nonexistent(client, auth_headers):
    response = client.get(
        "/assets/777",
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"


def test_update_asset(client, auth_headers):
    created = client.post("/assets", json=asset_payload, headers=auth_headers)
    asset_id = created.json()["id"]

    response = client.patch(
        f"/assets/{asset_id}",
        json={"asset_metadata": {"updated": "even more information"}},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["asset_metadata"] == {"updated": "even more information"}


def test_delete_asset(client, auth_headers):
    created = client.post("/assets", json=asset_payload, headers=auth_headers)
    asset_id = created.json()["id"]

    response = client.delete(
        f"/assets/{asset_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"{asset_payload['name']} deleted successfully"


def test_delete_asset_nonexistent(client, auth_headers):
    response = client.delete(
        "/assets/777",
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"
