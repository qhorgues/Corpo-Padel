import pytest
from fastapi import status

def test_list_teams_ok(client, auth_user, teams):
    res = client.get("/api/v1/teams")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json()["teams"], list)



def test_list_teams_unauthorized(client, auth_none):
    res = client.get("/api/v1/teams")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



def test_get_team_ok(client, auth_user, teams):
    team = teams[0]
    res = client.get(f"/api/v1/teams/{team.id}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == team.id


def test_get_team_not_found(client, auth_admin):
    res = client.get("/api/v1/teams/99999", headers=auth_admin)
    assert res.status_code == status.HTTP_404_NOT_FOUND



def test_get_team_unauthorized(client, teams, auth_none):
    res = client.get(f"/api/v1/teams/{teams[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



def test_create_team_ok(client, auth_admin, players, pool_in_db):
    payload = {
        "company": "TeamTest",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["company"] == "TeamTest"



def test_create_team_ok_pool_null(client, auth_admin, players):
    payload = {
        "company": "TeamTest",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": None
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_201_CREATED



def test_create_team_unauthorized(client, players, pool_in_db, auth_none):
    payload = {
        "company": "TeamTest",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



def test_create_team_forbidden(client, auth_user, players, pool_in_db):
    payload = {
        "company": "TeamTest",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_user)
    assert res.status_code == status.HTTP_403_FORBIDDEN



def test_create_team_bad_request_company_empty(client, auth_admin, players, pool_in_db):
    payload = {
        "company": "",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_create_team_bad_request_player_missing(client, auth_admin, players, pool_in_db):
    payload = {
        "company": "TeamTest",
        "player1_id": players[0].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_create_team_bad_request_player_null(client, auth_admin, players, pool_in_db):
    payload = {
        "company": "TeamTest",
        "player1_id": None,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.post("/api/v1/teams", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_update_team_ok(client, auth_admin, teams, players, pool_in_db):
    team = teams[0]
    payload = {
        "company": "TeamUpdated",
        "player1_id": players[1].id,
        "player2_id": players[0].id,
        "pool_id": pool_in_db.id
    }
    res = client.put(f"/api/v1/teams/{team.id}", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["company"] == "TeamUpdated"



def test_update_team_not_found(client, auth_admin, players, pool_in_db):
    payload = {
        "company": "TeamUpdated",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.put("/api/v1/teams/99999", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_404_NOT_FOUND



def test_update_team_unauthorized(client, teams, players, pool_in_db, auth_none):
    payload = {
        "company": "TeamUpdated",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.put(f"/api/v1/teams/{teams[0].id}", json=payload)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



def test_update_team_forbidden(client, auth_user, teams, players, pool_in_db):
    payload = {
        "company": "TeamUpdated",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.put(f"/api/v1/teams/{teams[0].id}", json=payload, headers=auth_user)
    assert res.status_code == status.HTTP_403_FORBIDDEN



def test_update_team_bad_request_company_empty(client, auth_admin, teams, players, pool_in_db):
    payload = {
        "company": "",
        "player1_id": players[0].id,
        "player2_id": players[1].id,
        "pool_id": pool_in_db.id
    }
    res = client.put(f"/api/v1/teams/{teams[0].id}", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_update_team_bad_request_player_missing(client, auth_admin, teams, pool_in_db):
    payload = {
        "company": "TeamUpdated",
        "player2_id": teams[0].player2_id,
        "pool_id": pool_in_db.id
    }
    res = client.put(f"/api/v1/teams/{teams[0].id}", json=payload, headers=auth_admin)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_delete_team_ok(client, auth_admin, teams):
    team = teams[0]
    res = client.delete(f"/api/v1/teams/{team.id}", headers=auth_admin)
    assert res.status_code == status.HTTP_204_NO_CONTENT



def test_delete_team_not_found(client, auth_admin):
    res = client.delete("/api/v1/teams/99999", headers=auth_admin)
    assert res.status_code == status.HTTP_404_NOT_FOUND



def test_delete_team_unauthorized(client, teams, auth_none):
    res = client.delete(f"/api/v1/teams/{teams[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



def test_delete_team_forbidden(client, auth_user, teams):
    res = client.delete(f"/api/v1/teams/{teams[0].id}", headers=auth_user)
    assert res.status_code == status.HTTP_403_FORBIDDEN
