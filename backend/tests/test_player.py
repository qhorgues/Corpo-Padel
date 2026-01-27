import pytest

def test_list_players_ok(client, auth_user):
    response = client.get("/api/v1/players")
    assert response.status_code == 200
    assert "players" in response.json()
    assert "total" in response.json()



def test_get_player_ok(client, db_session, auth_user):
    from app.models.models import Player, User

    user = User(email="p@test.com", password_hash="x", role="JOUEUR")
    player = Player(
        first_name="John",
        last_name="Doe",
        company="ACME",
        license_number="L123456",
        user=user
    )
    db_session.add(player)
    db_session.commit()

    response = client.get(f"/api/v1/players/{player.id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"



def test_get_player_not_found(client, db_session, auth_user):
    response = client.get(f"/api/v1/players/2")
    assert response.status_code == 404



def test_create_player_ok(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L654321",
        "email": "jane@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code == 201
    assert response.json()["first_name"] == "Jane"



def test_create_player_duplicate_email(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L654321",
        "email": "jane@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    response = client.post("/api/v1/players", json=payload)
    assert response.status_code == 400



def test_list_players_unauthorized(client, auth_none):
    response = client.get("/api/v1/players")
    assert response.status_code == 401



def test_create_player_forbidden(client, auth_user_forbidden):
    response = client.post("/api/v1/players", json={})
    assert response.status_code == 403



def test_invalid_license_format(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "123456",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_first_name(client, auth_admin):
    payload = {
        "first_name": "",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L123456",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_last_name(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "",
        "company": "ACME",
        "license_number": "L123456",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_company(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "",
        "license_number": "L123456",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_license(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_email(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L123456",
        "email": "",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_missing_required_role(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L123456",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": ""
    }

    response = client.post("/api/v1/players", json=payload)
    assert response.status_code in (400, 422)



def test_update_player_ok(client, db_session, auth_admin, test_user):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L654321",
        "email": "jane@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    from app.models.models import Player
    player = db_session.query(Player).filter(Player.user_id == test_user.id).first()

    response = client.put(f"/api/v1/players/{player.id}", json=payload)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"



def test_update_player_duplicate_email_and_license(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L654321",
        "email": "jane@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    payload2 = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L654322",
        "email": "jane@test2.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.post("/api/v1/players", json=payload)
    response = client.post("/api/v1/players", json=payload2)
    response = client.put(f"/api/v1/players/{response.json()["id"]}", json=payload)
    assert response.status_code == 400



def test_update_player_not_found(client, auth_admin):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "ACME",
        "license_number": "L111111",
        "email": "x@test.com",
        "password": "ValidP@ssw0rd123",
        "role": "JOUEUR"
    }

    response = client.put(f"/api/v1/players/2", json=payload)
    assert response.status_code == 404



def test_delete_user_ok(client, db_session, auth_admin, test_user):
    from app.models.models import Player
    player = db_session.query(Player).filter(Player.user_id == test_user.id).first()

    response = client.delete(f"/api/v1/players/{player.id}")
    assert response.status_code == 204



def test_delete_user_non_found(client, auth_admin):
    response = client.delete(f"/api/v1/players/2")
    assert response.status_code == 404
