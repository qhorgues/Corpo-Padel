import pytest
from datetime import date

from app.models.models import Player


def test_get_profile_ok(client, auth_user, test_user):
    response = client.get("/api/v1/profile/me")
    assert response.status_code == 200

    json = response.json()
    assert json["user"]["email"] == "test@example.com"
    assert json["player"]["first_name"] == "Test"



def test_get_profile_unauthorized(client, auth_none):
    response = client.get("/api/v1/profile/me")
    assert response.status_code == 401



def test_get_profile_player_not_found(client, auth_user, db_session):
    # Remove the player linked to the user
    player = db_session.query(Player).filter(Player.user_id).first()
    db_session.delete(player)
    db_session.commit()

    response = client.get("/api/v1/profile/me")
    assert response.status_code == 404



def test_update_profile_ok(client, auth_user):
    data = {
        "first_name": "NewFirst",
        "last_name": "NewLast",
        "company": "NewCompany",
        "license_number": "L999999",
        "birth_date": str(date.today()),
        "photo_url": "http://newphoto.url"
    }

    response = client.put("/api/v1/profile/me", json=data)
    assert response.status_code == 200

    json = response.json()
    assert json["player"]["first_name"] == "NewFirst"
    assert json["player"]["license_number"] == "L999999"



def test_update_profile_unauthorized(client, auth_none):
    data = {
        "first_name": "NewFirst",
        "last_name": "NewLast",
        "company": "NewCompany",
        "license_number": "L999999",
        "birth_date": str(date.today()),
        "photo_url": "http://newphoto.url"
    }
    response = client.put("/api/v1/profile/me", json=data)
    assert response.status_code == 401



def test_update_profile_player_not_found(client, auth_user, db_session):
    player = db_session.query(Player).filter(Player.user_id == 1).first()
    db_session.delete(player)
    db_session.commit()

    data = {
        "first_name": "NewFirst",
        "last_name": "NewLast",
        "company": "NewCompany",
        "license_number": "L999999",
        "birth_date": str(date.today()),
        "photo_url": "http://newphoto.url"
    }
    response = client.put("/api/v1/profile/me", json=data)
    assert response.status_code == 404



def test_upload_profile_photo_ok(client, auth_user):
    data = {
        "photo_url": "http://photo.url"
    }

    response = client.put("/api/v1/profile/me/photo", json=data)
    assert response.status_code == 201
    assert response.json()["photo_url"] == "http://photo.url"



def test_upload_profile_photo_unauthorized(client, auth_none):
    data = {
        "photo_url": "http://photo.url"
    }

    response = client.put("/api/v1/profile/me/photo", json=data)
    assert response.status_code == 401



def test_upload_profile_photo_player_not_found(client, auth_user, db_session):
    player = db_session.query(Player).filter(Player.user_id == 1).first()
    db_session.delete(player)
    db_session.commit()

    data = {
        "photo_url": "http://photo.url"
    }

    response = client.put("/api/v1/profile/me/photo", json=data)
    assert response.status_code == 404



def test_delete_profile_photo_ok(client, auth_user):
    response = client.delete("/api/v1/profile/me/photo")
    assert response.status_code == 204



def test_delete_profile_photo_unauthorized(client, auth_none):
    response = client.delete("/api/v1/profile/me/photo")
    assert response.status_code == 401



def test_delete_profile_photo_player_not_found(client, auth_user, db_session):
    player = db_session.query(Player).filter(Player.user_id == 1).first()
    db_session.delete(player)
    db_session.commit()

    response = client.delete("/api/v1/profile/me/photo")
    assert response.status_code == 404
