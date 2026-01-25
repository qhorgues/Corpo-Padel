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
from app.models.models import User
from app.core.security import get_password_hash

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
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

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
        last_name="Test",
        first_name="Test",
        company="Test",
        license_number="Test",
        birth_date=func.now(),
        photo_url="Test",
        email="test@example.com",
        password_hash=get_password_hash("ValidP@ssw0rd123"),
        role="JOUEUR",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin(db_session):
    """Crée un administrateur de test"""
    admin = User(
        last_name="Admin",
        first_name="Admin",
        company="Admin",
        license_number="Admin",
        birth_date=func.now(),
        photo_url="Admin",
        email="admin@example.com",
        password_hash=get_password_hash("AdminP@ssw0rd123"),
        role="ADMINISTRATEUR",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin
