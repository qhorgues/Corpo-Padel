import pytest
from app.models.models import User


def test_reset_password_ok(client, auth_admin, db_session, test_user):
    from app.core.security import get_password_hash

    response = client.post(
        f"/api/v1/admin/accounts/{test_user.id}/reset-password",
        headers=auth_admin
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Mot de passe réinitialisé"
    assert len(data["temporary_password"]) == 16
    assert data["warning"] == "Ce mot de passe ne sera affiché qu'une seule fois"

    db_session.refresh(test_user)
    assert test_user.password_hash != get_password_hash("password")



def test_reset_password_forbidden(client, db_session, test_user):

    response = client.post(
        f"/api/v1/admin/accounts/{test_user.id}/reset-password"
    )

    assert response.status_code == 403



def test_reset_password_unauthorized(client, db_session, test_user, auth_none):

    response = client.post(
        f"/api/v1/admin/accounts/{test_user}/reset-password"
    )

    assert response.status_code == 401



def test_reset_password_not_found_player(client, auth_admin, db_session):
    response = client.post(
        f"/api/v1/admin/accounts/2/reset-password",
        headers=auth_admin
    )

    assert response.status_code == 404
