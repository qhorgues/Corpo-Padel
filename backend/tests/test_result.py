import pytest
from datetime import date, time

from app.models.models import Match, Event, Player, Team, User
from app.schemas.match import MatchStatus


def create_event(db_session):
    event = Event(
        event_date=date.today(),
        event_time=time(18, 0)
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event



def test_my_results_ok(client, auth_user, db_session, test_user):
    player = db_session.query(Player).filter(Player.user_id == test_user.id).first()

    user2 = User(
        email="other@test.com",
        password_hash="x",
        role="JOUEUR",
        is_active=True
    )
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)

    player2 = Player(
        first_name="Other",
        last_name="Player",
        company="OppCompany",
        license_number="L222222",
        user_id=user2.id
    )
    db_session.add(player2)
    db_session.commit()
    db_session.refresh(player2)

    team_with_user = Team(
        company="UserTeam",
        player1_id=player.id,
        player2_id=player2.id
    )
    db_session.add(team_with_user)

    user3 = User(
        email="other2@test.com",
        password_hash="x",
        role="JOUEUR",
        is_active=True
    )
    db_session.add(user3)
    db_session.commit()
    db_session.refresh(user3)

    player3 = Player(
        first_name="Other2",
        last_name="Player2",
        company="OppCompany2",
        license_number="L333333",
        user_id=user3.id
    )
    db_session.add(player3)
    db_session.commit()
    db_session.refresh(player3)

    team_opponent = Team(
        company="OppTeam",
        player1_id=player2.id,
        player2_id=player3.id
    )
    db_session.add(team_opponent)
    db_session.commit()

    event = create_event(db_session)

    match = Match(
        court_number=1,
        team1_id=team_with_user.id,
        team2_id=team_opponent.id,
        status="TERMINE",
        score_team1=2,
        score_team2=1,
        event_id=event.id
    )
    db_session.add(match)
    db_session.commit()

    response = client.get("/api/v1/results/my-results")
    assert response.status_code == 200

    data = response.json()
    assert data["statistics"]["wins"] == 1
    assert data["statistics"]["losses"] == 0
    assert data["statistics"]["total_matches"] == 1
    assert data["statistics"]["win_rate"] == 100
    assert data["results"][0]["result"] == "VICTOIRE"
    assert data["results"][0]["score"] == "2-1"



def test_my_results_unauthorized(client, auth_none):
    response = client.get("/api/v1/results/my-results")
    assert response.status_code == 401



def test_my_results_player_not_found(client, auth_user, db_session):
    player = db_session.query(Player).filter(Player.user_id == 1).first()
    db_session.delete(player)
    db_session.commit()

    response = client.get("/api/v1/results/my-results")
    assert response.status_code == 404



def test_rankings_ok(client, auth_user, db_session, teams):
    event = create_event(db_session)

    m1 = Match(
        court_number=1,
        team1_id=teams[0].id,
        team2_id=teams[1].id,
        status="TERMINE",
        score_team1=2,
        score_team2=0,
        event_id=event.id
    )
    m2 = Match(
        court_number=2,
        team1_id=teams[2].id,
        team2_id=teams[3].id,
        status="TERMINE",
        score_team1=1,
        score_team2=2,
        event_id=event.id
    )
    db_session.add_all([m1, m2])
    db_session.commit()

    response = client.get("/api/v1/results/rankings")
    assert response.status_code == 200

    data = response.json()["rankings"]
    assert data[0]["points"] >= data[1]["points"]
    assert data[0]["wins"] == 1
    assert data[0]["points"] == 3



def test_rankings_unauthorized(client, auth_none):
    response = client.get("/api/v1/results/rankings")
    assert response.status_code == 401
