# ============================================
# FICHIER : backend/tests/test_creation.py
# ============================================

import pytest
from datetime import datetime
from fastapi import status

def test_create_user_success(client, test_admin):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "bien été créé" in data["message"]

def test_create_user_invalid_credentials(client, test_user):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "ValidP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "être un administateur" in data["detail"]

def test_create_user_invalid_user(client, test_admin):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    _ = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    response = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "existe déjà" in data["detail"]

def test_delete_user_success(client, test_admin):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    _ = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    response = client.post("/api/v1/user/delete-user", headers=headers, json={"email": "test@nouveau.com"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "bien été supprimé" in data["message"]

def test_delete_user_invalid_credentials(client, test_user, test_admin):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    _ = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    _ = client.post("/api/v1/auth/logout", headers=headers)

    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "ValidP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/user/delete-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "être un administateur" in data["detail"]

def test_delete_user_invalid_user(client, test_admin):
    """Test création d'un utilisateur avec credentials valides"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour accéder à une route protégée
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/user/create-user", headers=headers, json={
        "last_name": "Lefrontier",
        "first_name": "Gérard",
        "company": "LeMontBlanc",
        "license_number": "222014-99951",
        "birth_date": f"{datetime.fromisoformat('2011-11-04')}",
        "photo_url": "./url/photo/nouveau",
        "email": "test@nouveau.com",
        "password": "TempP@ssw0rd123",
        "role": "JOUEUR",
        "is_active": f"{True}"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "n'existe pas" in data["detail"]