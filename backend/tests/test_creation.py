# ============================================
# FICHIER : backend/tests/test_creation.py
# ============================================

import pytest
from datetime import datetime
from fastapi import status
from app.schemas.auth import UserCreationRequest

def test_create_user_success(client, test_admin):
    """Test connexion avec credentials valides pour un utilisateur"""
    request = UserCreationRequest(
        last_name="Lefrontier",
        first_name="Gérard",
        company="LeMontBlanc",
        license_number="222014-99951",
        birth_date=datetime.fromisoformat('2011-11-04'),
        photo_url="./url/photo/nouveau",
        email="test@nouveau.com",
        password="TempP@ssw0rd123",
        role="JOUEUR",
        is_active=True
    )
    response = client.post("/api/v1/create/create-user", json={
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