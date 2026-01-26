from datetime import time
import pytest
from sqlalchemy import func

@pytest.fixture
def players(db_session):
    from app.models.models import Player, User

    players = []
    for i in range(12):
        user = User(
            email=f"p{i}@test.com",
            password_hash="x",
            role="JOUEUR"
        )
        player = Player(
            first_name=f"P{i}",
            last_name="Test",
            company="ACME",
            license_number=f"L{100000+i}",
            user=user
        )
        db_session.add(player)
        players.append(player)

    db_session.commit()
    return players



@pytest.fixture
def teams(db_session, players):
    from app.models.models import Team

    teams = []
    for i in range(6):
        team = Team(
            company=f"Team {i}",
            player1_id=players[i*2].id,
            player2_id=players[i*2+1].id,
        )
        db_session.add(team)
        teams.append(team)

    db_session.commit()
    return teams



@pytest.fixture
def pool_in_db(db_session, teams):
    from app.models.models import Pool

    pool = Pool(name="Pool DB")
    pool.teams = teams
    db_session.add(pool)
    db_session.commit()
    db_session.refresh(pool)
    return pool



def test_create_pool_not_authenticated(client, teams, auth_none):
    payload = {
        "name": "Pool X",
        "team_ids": [t.id for t in teams],
    }

    response = client.post("/api/v1/pools", json=payload)
    assert response.status_code == 401



def test_create_pool_ok(client, auth_admin, teams):
    payload = {
        "name": "Pool A",
        "team_ids": [t.id for t in teams],
    }

    response = client.post("/api/v1/pools", json=payload)
    assert response.status_code == 201
    assert response.json()["teams_count"] == 6



def test_create_pool_not_admin(client, auth_user, teams):
    payload = {
        "name": "Pool X",
        "team_ids": [t.id for t in teams],
    }

    response = client.post("/api/v1/pools", json=payload)
    assert response.status_code == 403



def test_create_pool_invalid_team_count(client, auth_admin, teams):
    payload = {
        "name": "Bad Pool",
        "team_ids": [teams[0].id, teams[1].id],
    }

    response = client.post("/api/v1/pools", json=payload)
    assert response.status_code == 400



def test_update_pool_admin_ok(
    client,
    auth_admin,
    pool_in_db,
    teams
):
    payload = {
        "name": "Updated Pool",
        "team_ids": [t.id for t in teams],
    }

    response = client.put(f"/api/v1/pools/{pool_in_db.id}", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Pool"



def test_update_pool_invalid_team_count(
    client,
    auth_admin,
    pool_in_db,
    teams
):
    payload = {
        "name": "Broken Pool",
        "team_ids": [teams[0].id],
    }

    response = client.put(f"/api/v1/pools/{pool_in_db.id}", json=payload)
    assert response.status_code == 400



def test_update_pool_with_finished_match_forbidden(
    client,
    auth_admin,
    pool_in_db,
    finished_match,
    teams
):
    payload = {
        "name": "Nope",
        "team_ids": [t.id for t in teams],
    }

    response = client.put(f"/api/v1/pools/{pool_in_db.id}", json=payload)
    assert response.status_code == 400



@pytest.fixture
def finished_match(db_session, pool_in_db):
    from app.models.models import Match, Event

    event = Event(event_date=func.current_date(), event_time=time())
    db_session.add(event)
    db_session.commit()

    match = Match(
        event_id=event.id,
        team1_id=pool_in_db.teams[0].id,
        team2_id=pool_in_db.teams[1].id,
        status="TERMINE",
        court_number=1
    )
    db_session.add(match)
    db_session.commit()
    return match



def test_delete_pool_with_finished_match(
    client,
    auth_admin,
    pool_in_db,
    finished_match,
):
    response = client.delete(f"/api/v1/pools/{pool_in_db.id}")
    assert response.status_code == 400
