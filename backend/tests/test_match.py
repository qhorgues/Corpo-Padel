import pytest
from app.schemas.match import MatchStatus


def test_list_matches_ok(client, auth_user, event):
    response = client.get("/api/v1/matches")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["matches"][0]["status"] == "A_VENIR"



def test_list_matches_unauthorized(client, auth_none):
    response = client.get("/api/v1/matches")
    assert response.status_code == 401



def test_get_match_ok(client, auth_user, event):
    match_id = event.matches[0].id
    response = client.get(f"/api/v1/matches/{match_id}")
    assert response.status_code == 200
    assert response.json()["id"] == match_id



def test_get_match_not_found(client, auth_user):
    response = client.get("/api/v1/matches/999")
    assert response.status_code == 404



def test_get_match_unauthorized(client, auth_none):
    response = client.get("/api/v1/matches/1")
    assert response.status_code == 401



def test_create_match_ok(client, auth_admin, teams):
    data = {
        "court_number": 2,
        "status": "A_VENIR",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.post("/api/v1/matches", json=data)
    assert response.status_code == 201
    assert response.json()["court_number"] == 2
    assert response.json()["status"] == "A_VENIR"



def test_create_match_forbidden_user(client, auth_user, teams):
    data = {
        "court_number": 2,
        "status": "A_VENIR",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.post("/api/v1/matches", json=data)
    assert response.status_code == 403



def test_create_match_unauthorized(client, auth_none, teams):
    data = {
        "court_number": 2,
        "status": "A_VENIR",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.post("/api/v1/matches", json=data)
    assert response.status_code == 401



def test_create_match_invalid_court(client, auth_admin, teams):
    data = {
        "court_number": 11,
        "status": "A_VENIR",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.post("/api/v1/matches", json=data)
    assert response.status_code == 400



def test_create_match_same_team(client, auth_admin, teams):
    data = {
        "court_number": 1,
        "status": "A_VENIR",
        "team1_id": teams[0].id,
        "team2_id": teams[0].id
    }
    response = client.post("/api/v1/matches", json=data)
    assert response.status_code == 400



def test_update_match_ok(client, auth_admin, event, teams):
    match_id = event.matches[0].id
    data = {
        "court_number": 3,
        "status": "ANNULE",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.put(f"/api/v1/matches/{match_id}", json=data)
    assert response.status_code == 200
    assert response.json()["court_number"] == 3
    assert response.json()["status"] == "ANNULE"



def test_update_match_forbidden_user(client, auth_user, event, teams):
    match_id = event.matches[0].id
    data = {
        "court_number": 3,
        "status": "EN_COURS",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.put(f"/api/v1/matches/{match_id}", json=data)
    assert response.status_code == 403



def test_update_match_not_found(client, auth_admin):
    data = {
        "court_number": 1,
        "status": "A_VENIR",
        "team1_id": 1,
        "team2_id": 2
    }
    response = client.put("/api/v1/matches/999", json=data)
    assert response.status_code == 404



def test_update_match_unauthorized(client, auth_none, event, teams):
    match_id = event.matches[0].id
    data = {
        "court_number": 3,
        "status": "EN_COURS",
        "team1_id": teams[0].id,
        "team2_id": teams[1].id
    }
    response = client.put(f"/api/v1/matches/{match_id}", json=data)
    assert response.status_code == 401



def test_delete_match_ok(client, auth_admin, event):
    match_id = event.matches[0].id
    response = client.delete(f"/api/v1/matches/{match_id}")
    assert response.status_code == 204



def test_delete_match_forbidden_user(client, auth_user, event):
    match_id = event.matches[0].id
    response = client.delete(f"/api/v1/matches/{match_id}")
    assert response.status_code == 403



def test_delete_match_unauthorized(client, auth_none, event):
    match_id = event.matches[0].id
    response = client.delete(f"/api/v1/matches/{match_id}")
    assert response.status_code == 401



def test_delete_match_not_found(client, auth_admin):
    response = client.delete("/api/v1/matches/999")
    assert response.status_code == 404



def test_delete_match_only_if_avenir(client, auth_admin, event_with_finished_match):
    match_id = event_with_finished_match.matches[0].id
    response = client.delete(f"/api/v1/matches/{match_id}")
    assert response.status_code == 400
