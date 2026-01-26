# ============================================
# FICHIER : backend/tests/conftest.py
# ============================================

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.models import User, Player
from app.core.security import get_password_hash
from app.api.deps import get_current_user, get_current_admin
from fastapi import HTTPException, status

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    """Crée une base de données de test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Fournit une session de base de données pour les tests"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Client de test FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Crée un utilisateur de test"""
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("ValidP@ssw0rd123"),
        role="JOUEUR",
        is_active=True
    )
    db_session.add(user)
    player = Player(
        last_name="Test",
        first_name="Test",
        company="Test",
        license_number="L111111",
        birth_date=func.current_date(),
        photo_url="Test",
        user=user
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin(db_session):
    """Crée un administrateur de test"""
    admin = User(
        email="admin@example.com",
        password_hash=get_password_hash("AdminP@ssw0rd123"),
        role="ADMINISTRATEUR",
        is_active=True
    )
    db_session.add(admin)
    player = Player(
        last_name="Admin",
        first_name="Admin",
        company="Admin",
        license_number="L111111",
        birth_date=func.current_date(),
        photo_url="Admin",
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def auth_user(client, test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def auth_admin(client, test_admin):
    app.dependency_overrides[get_current_user] = lambda: test_admin
    app.dependency_overrides[get_current_admin] = lambda: test_admin
    yield
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_current_admin, None)

@pytest.fixture
def auth_none(client):
    def unauthorized():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    app.dependency_overrides[get_current_user] = unauthorized
    app.dependency_overrides[get_current_admin] = unauthorized
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def auth_user_forbidden(client, test_user):
    def forbidden():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[get_current_admin] = forbidden
    yield
    app.dependency_overrides.clear()
