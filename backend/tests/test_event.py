import pytest
from datetime import date, timedelta
from app.models.models import Event

def valid_match(team1_id, team2_id, court=1):
    return {
        "court_number": court,
        "team1_id": team1_id,
        "team2_id": team2_id,
        "status": "A_VENIR"
    }



def valid_event_payload(team_ids):
    return {
        "event_date": date.today().isoformat(),
        "event_time": "18:30",
        "matches": [
            valid_match(team_ids[0], team_ids[1], 1),
            valid_match(team_ids[2], team_ids[3], 2),
        ]
    }



def test_list_events_ok(client, auth_user):
    res = client.get("/api/v1/events")
    assert res.status_code == 200
    assert "events" in res.json()
    assert "total" in res.json()



def test_list_events_unauthorized(client, auth_none):
    res = client.get("/api/v1/events")
    assert res.status_code == 401



def test_get_event_ok(client, auth_user, event):
    res = client.get(f"/api/v1/events/{event.id}")
    assert res.status_code == 200
    assert res.json()["event_date"] == event.event_date.isoformat()
    assert len(res.json()["matches"]) == len(event.matches)



def test_get_event_not_found(client, auth_user):
    res = client.get("/api/v1/events/9999")
    assert res.status_code == 404



def test_create_event_ok(client, auth_admin, teams):
    payload = valid_event_payload([t.id for t in teams])
    res = client.post("/api/v1/events", json=payload)

    assert res.status_code == 201
    assert res.json()["event_date"] == payload["event_date"]
    assert len(res.json()["matches"]) == 2



def test_create_event_unauthorized(client, auth_none):
    res = client.post("/api/v1/events", json={})
    assert res.status_code == 401



def test_create_event_forbidden_for_user(client, auth_user):
    res = client.post("/api/v1/events", json={})
    assert res.status_code == 403



def test_create_event_invalid_date(client, auth_admin, teams):
    payload = valid_event_payload([t.id for t in teams])
    payload["event_date"] = (date.today() - timedelta(days=1)).isoformat()

    res = client.post("/api/v1/events", json=payload)
    assert res.status_code == 400



def test_create_event_invalid_time(client, auth_admin, teams):
    payload = valid_event_payload([t.id for t in teams])
    payload["event_time"] = "25:99"

    res = client.post("/api/v1/events", json=payload)
    assert res.status_code == 422



def test_create_event_invalid_matches_count(client, auth_admin, teams):
    payload = valid_event_payload([t.id for t in teams])
    payload["matches"] = []

    res = client.post("/api/v1/events", json=payload)
    assert res.status_code == 400



def test_create_event_same_team_twice(client, auth_admin, teams):
    payload = {
        "event_date": date.today().isoformat(),
        "event_time": "18:30",
        "matches": [
            valid_match(teams[0].id, teams[0].id, 1)
        ]
    }

    res = client.post("/api/v1/events", json=payload)
    assert res.status_code == 400



def test_update_event_ok(client, auth_admin, event, teams):
    payload = valid_event_payload([t.id for t in teams])

    res = client.put(f"/api/v1/events/{event.id}", json=payload)
    assert res.status_code == 200
    assert len(res.json()["matches"]) == 2



def test_update_event_not_found(client, auth_admin, teams):
    payload = valid_event_payload([t.id for t in teams])

    res = client.put("/api/v1/events/9999", json=payload)
    assert res.status_code == 404



def test_update_event_forbidden(client, auth_user, event):
    res = client.put(f"/api/v1/events/{event.id}", json={})
    assert res.status_code == 403



def test_update_event_unauthorized(client, event, auth_none):
    res = client.put(f"/api/v1/events/{event.id}", json={})
    assert res.status_code == 401



def test_delete_event_ok(client, auth_admin, event):
    res = client.delete(f"/api/v1/events/{event.id}")
    assert res.status_code == 204



def test_delete_event_not_found(client, auth_admin):
    res = client.delete("/api/v1/events/9999")
    assert res.status_code == 404



def test_delete_event_forbidden(client, auth_user, event):
    res = client.delete(f"/api/v1/events/{event.id}")
    assert res.status_code == 403



def test_delete_event_with_finished_match(client, auth_admin, event_with_finished_match):
    res = client.delete(f"/api/v1/events/{event_with_finished_match.id}")
    assert res.status_code == 400
